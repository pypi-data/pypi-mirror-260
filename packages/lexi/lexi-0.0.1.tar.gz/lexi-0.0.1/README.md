
# Lexi

Lexi is a local LLM-based solution - includes Chat UI, RAG, LLM Proxy, and Document importing

Currently supports Atlasian's Cloud Confluence.

## System Overview

![System Overview](docs/Lexi_overview.png)

## Getting started

### Pre-requistes

- Python 3.8 upwards
- Docker (with Docker Compose)

### Installation

`pip install lexi`

### Configuration

```bash
lexi system create_envrc \
    --confluence-url "https://some-company.atlassian.net/wiki" \
    --confluence-space-key "some-company" \
    --confluence-email "user@some-company.com" \
    --confluence-space-name "" \
    --compose-project-name "lexi-system" \
    --litellm-log "INFO"
```

It will ask for your Confluence and OpenAIs API Keys

### Start the system

`lexi system up`

### Stop the system

`lexi system down`

## Loading documents

After installing and setting up the environment with `lexi system create_envrc` run the following to import the Confluence documents:

`lexi load`

You'll see the text from confluence being processed. It should end something like this:

```bash
Succesfully imported 172 documents and 759 chunks
Imported 172 documents into Weaviate.
```
