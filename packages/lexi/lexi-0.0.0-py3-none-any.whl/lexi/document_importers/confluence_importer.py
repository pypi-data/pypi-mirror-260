from typing import List

from langchain_community.document_loaders import ConfluenceLoader
from settings import (
    CONFLUENCE_EMAIL_ADDRESS,
    CONFLUENCE_PRIVATE_API_KEY,
    CONFLUENCE_SPACE_URL,
)
from verba_interface.document import Document as VerbaDocument

from .document_importer import DocumentImporter


class ConfluenceImporter(DocumentImporter):
    def __init__(self):
        self.loader = ConfluenceLoader(
            url=CONFLUENCE_SPACE_URL,
            username=CONFLUENCE_EMAIL_ADDRESS,
            api_key=CONFLUENCE_PRIVATE_API_KEY,
        )

    def import_documents(self, space_key: str, limit: int = 50) -> List[VerbaDocument]:
        documents = self.loader.load(
            space_key=space_key, include_attachments=False, limit=limit
        )
        # Convert loaded documents to VerbaDocuments here
        return [self._convert_to_verba_document(doc) for doc in documents]

    def _convert_to_verba_document(self, document) -> VerbaDocument:
        # Conversion logic
        pass
