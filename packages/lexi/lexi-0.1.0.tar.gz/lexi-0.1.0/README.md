
# Lexi

Lexi is a local LLM-based solution - includes Chat UI, RAG, LLM Proxy, and Document importing

Currently supports Atlasian's Cloud Confluence.

## Pre-requistes

- Python 3.8 upwards
- Docker (with Docker Compose)

## Installation

`pip install lexi`

## Configuration

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

## Start the system

`lexi system up`

## Stop the system

`lexi system down`
