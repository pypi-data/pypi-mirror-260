import os
import re
import time
from datetime import datetime

import typer
import weaviate
from langchain_community.document_loaders import ConfluenceLoader
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from tqdm import tqdm
from weaviate.classes.config import DataType, Property

import lexi.settings as settings
from lexi.tui.system import system_app
from lexi.utils.rich_logger import RichLogger
from lexi.verba_interface.chunker import TokenChunker
from lexi.verba_interface.document import Document as VerbaDocument

logger = RichLogger("application.log")

app = typer.Typer()

schema_app = typer.Typer()

app.add_typer(schema_app, name="schema")
app.add_typer(system_app, name="system")


def strip_non_letters(s: str):
    return re.sub(r"[^a-zA-Z0-9]", "_", s)


def import_data(
    documents: list[VerbaDocument],
) -> bool:
    """Import verba documents and its chunks to Weaviate
    @parameter: documents : list[Document] - List of Verba documents
    @parameter: client : Client - Weaviate Client
    @parameter: batch_size : int - Batch Size of Input
    @returns bool - Bool whether the embedding what successful.
    """
    client = _get_weaviate_client()

    # vectorizer = "text2vec-openai"

    Document_collection = client.collections.get("Document_MiniLM")
    Chunk_collection = client.collections.get("Chunk_MiniLM")

    for i, document in enumerate(documents):
        batches = []
        uuid = ""
        temp_batch = []
        token_counter = 0
        for chunk in document.chunks:
            print(chunk.to_dict())
            print(chunk.tokens)
            if token_counter + chunk.tokens <= 4000:
                token_counter += chunk.tokens
                temp_batch.append(chunk)
            else:
                batches.append(temp_batch.copy())
                token_counter = chunk.tokens
                temp_batch = [chunk]
        if len(temp_batch) > 0:
            batches.append(temp_batch.copy())
            token_counter = 0
            temp_batch = []

        typer.echo(
            f"({i+1}/{len(documents)}) Importing document {document.name} with {len(batches)} batches"
        )

        with Document_collection.batch.dynamic() as batch:
            batch.batch_size = 1
            properties = {
                "text": str(document.text),
                "doc_name": str(document.name),
                "doc_type": str(document.type),
                "doc_link": str(document.link),
                "chunk_count": len(document.chunks),
                "timestamp": str(document.timestamp),
            }

            uuid = batch.add_object(properties)

            for chunk in document.chunks:
                chunk.set_uuid(uuid)

        chunk_count = 0
        for _batch_id, chunk_batch in tqdm(
            enumerate(batches), total=len(batches), desc="Importing batches"
        ):
            with Chunk_collection.batch.dynamic() as batch:
                batch.batch_size = len(chunk_batch)
                for i, chunk in enumerate(chunk_batch):
                    chunk_count += 1

                    properties = {
                        "text": chunk.text,
                        "doc_name": str(document.name),
                        "doc_uuid": chunk.doc_uuid,
                        "doc_type": chunk.doc_type,
                        "chunk_id": chunk.chunk_id,
                    }

                    # Check if vector already exists
                    if chunk.vector is None:
                        batch.add_object(properties=properties)
                    else:
                        batch.add_object(properties=properties, vector=chunk.vector)

                    wait_time_ms = int(
                        os.getenv("WAIT_TIME_BETWEEN_INGESTION_QUERIES_MS", "0")
                    )
                    if wait_time_ms > 0:
                        time.sleep(float(wait_time_ms) / 1000)

    return True


def load_data(
    documents,
):
    """
    Load data into the system.
    """
    # Convert each document into VerbaDocument
    verba_documents = []
    for document in documents:
        verba_document = VerbaDocument(
            text=document.page_content,
            type="Documentation",
            name=document.metadata.get("title", ""),
            link=document.metadata.get("source", ""),
            timestamp=str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            reader="bespoke",
        )
        verba_documents.append(verba_document)

    if verba_documents is None:
        typer.echo("No documents imported")
        return

    chunker = TokenChunker()

    print("Before chunking:")
    for doc in verba_documents:
        print(f"Document Name: {doc.name}, Text Length: {len(doc.text)}")

    modified_documents = chunker.chunk(verba_documents, units=250, overlap=50)

    print("After chunking:")
    for doc in modified_documents:
        print(f"Document Name: {doc.name}, Num Chunks: {len(doc.chunks)}")

    import_data(modified_documents)

    document_count = len(modified_documents)
    chunks_count = sum([len(document.chunks) for document in modified_documents])

    typer.echo(
        f"Succesfully imported {document_count} documents and {chunks_count} chunks"
    )


def _get_weaviate_client(host: str = "localhost"):
    # Connect with default parameters for a local Weaviate instance
    client = weaviate.connect_to_local(host=host)
    # client = weaviate.Client("http://localhost:8080")
    return client


def download_confluence_documents():
    # Initialize the ConfluenceLoader with the settings from settings.py
    loader = ConfluenceLoader(
        url=settings.CONFLUENCE_SPACE_URL,
        username=settings.CONFLUENCE_EMAIL_ADDRESS,  # Assuming the email address is used as the username
        api_key=settings.CONFLUENCE_PRIVATE_API_KEY,
    )

    # Download documents
    documents = loader.load(
        space_key=settings.CONFLUENCE_SPACE_KEY, include_attachments=False, limit=50
    )

    return documents


def import_documents_to_weaviate(documents):
    client = (
        weaviate.connect_to_local()
    )  # Ensure this matches your Weaviate instance configuration

    collection = client.collections.get("Documents")

    with Progress() as progress, collection.batch.dynamic() as batch:
        task = progress.add_task("[cyan]Importing documents...", total=len(documents))

        for document in documents:
            # Assuming 'document' is a dict with the correct structure for your schema
            batch.add_object(
                properties=document.dict(),
                # uuid=document.get("uuid", weaviate.util.generate_uuid5(document))  # Generate UUID for each document
            )
            progress.advance(task)


@schema_app.command("create")
def create_schema(schema_name: str = "Documents"):
    client = _get_weaviate_client()

    try:
        collection = client.collections.get(schema_name)
        collection_config = collection.config.get()
        if collection_config:
            typer.echo(f"Collection '{schema_name}' already exists.")
            return
    except Exception:
        typer.echo(f"Collection '{schema_name}' does not exist, creating.")

    try:
        client.collections.create(
            "Documents",
            properties=[
                Property(name="page_content", data_type=DataType.TEXT),
                Property(name="metadata", data_type=DataType.TEXT),
            ],
        )

        typer.echo(f"Schema '{schema_name}' created successfully.")
    except Exception as e:
        typer.echo(f"Failed to check or create schema: {e}")


@schema_app.command("details")
def schema_details(schema_name: str):
    client = _get_weaviate_client()
    try:
        collection = client.collections.get(schema_name)
        collection_config = collection.config.get()
    except Exception:
        typer.echo(f"Collection '{schema_name}' does not exist.")
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Collection Name", style="cyan")
    table.add_column("Property Name", style="magenta", justify="right")
    table.add_column("Data Type", style="green", justify="right")

    for prop in collection_config.properties:
        table.add_row(
            schema_name,
            prop.name,
            prop.data_type.value,  # Adjust based on actual attribute names
        )

    console = Console()
    console.print(table)


@schema_app.command("list")
def list_schema():
    client = _get_weaviate_client()
    try:
        response = client.collections.list_all()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Collection Name", style="cyan")
        table.add_column("Property Name", style="magenta", justify="right")
        table.add_column("Data Type", style="green", justify="right")

        last_collection_name = ""
        for collection_name, collection_details in response.items():
            for prop in collection_details.properties:
                display_name = (
                    collection_name if collection_name != last_collection_name else ""
                )
                table.add_row(
                    display_name,
                    prop.name,
                    prop.data_type.value,  # Adjust based on actual attribute names
                )
                last_collection_name = collection_name

        console = Console()
        console.print(table)

    except Exception as e:
        typer.echo(f"Failed to list schemas: {e}")


@app.command("load")
def load_confluence_data():
    documents = download_confluence_documents()
    typer.echo(f"Downloaded {len(documents)} documents.")
    # Import documents to Weaviate
    load_data(documents)
    typer.echo(f"Imported {len(documents)} documents into Weaviate.")


@schema_app.command("top_documents")
def list_top_documents(schema_name: str):
    client = _get_weaviate_client()
    try:
        # Query to retrieve top 5 documents based on your criteria, e.g., most recent
        collection = client.collections.get(schema_name)

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Document Name", style="cyan")
        table.add_column("Link", style="magenta", justify="right")
        # Add more columns as needed based on the properties of your documents

        for item in collection.iterator():
            table.add_row(item.properties["doc_name"], item.properties["doc_link"])

        console = Console()
        console.print(table)
    except Exception as e:
        typer.echo(f"Failed to list top documents for '{schema_name}': {str(e)}")


if __name__ == "__main__":
    app()
