# ALEXVALE Gmail MCP

A FastMCP-based server that exposes Gmail operations as Model Context Protocol (MCP) tools. It enables AI clients to search, review, and send email through a user's Gmail account using OAuth credentials and secure server-side authentication.

## Overview

This project provides a lightweight integration layer between an MCP-compatible client and Gmail. It exposes a small, focused set of tools for:

- Searching recent or filtered emails
- Fetching unread messages
- Listing recent messages
- Sending emails on behalf of the authenticated user
- Health checking the service

The server is built with Python and uses FastMCP, Google Gmail API, and WorkOS-based authentication for secure access.

## Features

- Gmail search via Gmail query syntax
- Recent email retrieval
- Unread email retrieval
- Email sending with Gmail API
- OAuth-based authentication using refresh token credentials
- Redis-backed persistence for OAuth client storage
- HTTP transport for MCP server deployment
- Docker support for containerized deployment

## Architecture

```text
MCP Client
   |
   v
FastMCP Server (server.py)
   |
   +--> gmail_client.py  -> Gmail API
   |
   +--> auth.py          -> OAuth credential loading
   |
   +--> WorkOS auth      -> secure user auth/session handling
   |
   +--> Redis store      -> persistent OAuth client storage
```

## Tools Exposed

The server registers the following MCP tools:

### `health_check()`
Returns service status information.

### `search_gmail(query="newer_than:7d", max_results=10)`
Searches the authenticated Gmail inbox using standard Gmail search syntax.

Examples:
- `newer_than:7d`
- `is:unread`
- `from:google.com`
- `subject:interview`

### `get_recent_emails(max_results=10)`
Returns recent Gmail messages from the last 7 days.

### `get_unread_emails(max_results=10)`
Returns unread Gmail messages.

### `send_gmail(to, subject, body)`
Sends an email through the authenticated Gmail account.

## Prerequisites

Before running this project, make sure you have:

- Python 3.12+
- A Google Cloud project with Gmail API enabled
- OAuth 2.0 credentials for a Gmail user
- A refresh token for the Gmail account
- Redis configured for persistent OAuth storage
- A WorkOS project and AuthKit configuration if you plan to use the hosted auth provider

## Environment Variables

Create a `.env` file or set these environment variables before running the app:

```bash
GMAIL_CLIENT_ID=your_google_client_id
GMAIL_CLIENT_SECRET=your_google_client_secret
GMAIL_REFRESH_TOKEN=your_google_refresh_token

WORKOS_CLIENT_ID=your_workos_client_id
WORKOS_CLIENT_SECRET=your_workos_client_secret
WORKOS_AUTHKIT_DOMAIN=https://your-authkit-domain
REDIS_URL=redis://localhost:6379/0

PORT=8080
```

### Required Gmail OAuth values

The app uses these environment variables in `auth.py`:

- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`
- `GMAIL_REFRESH_TOKEN`

These are used to create a Google OAuth credential and refresh access tokens automatically.

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/Mukeshram-07/alexvale-gmail-mcp.git
cd alexvale-gmail-mcp
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add your environment variables.

5. Run the server:

```bash
python server.py
```

The server will start using the configured port, defaulting to `8000` unless `PORT` is set.

## Docker Setup

This repository includes a Dockerfile for containerized deployment.

Build the image:

```bash
docker build -t alexvale-gmail-mcp .
```

Run the container:

```bash
docker run -p 8080:8080 --env-file .env alexvale-gmail-mcp
```

## Deployment Notes

The service is configured to run over HTTP transport, with a `BASE_URL` set to:

```text
https://alexvale-gmail-mcp.onrender.com
```

This is suited for deployments on Render, Azure, Fly.io, Railway, or similar hosting platforms.

## Gmail API Setup

To use Gmail integration, ensure the following:

1. Enable the Gmail API in your Google Cloud project.
2. Create OAuth 2.0 credentials.
3. Obtain a refresh token for the Gmail account you want to access.
4. Grant the required scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.send`

## Security Considerations

- OAuth credentials and refresh tokens should be stored as secrets, never committed to source control.
- Redis-backed OAuth storage is used for persistence and resilience.
- Email-sending operations are intentionally exposed as write actions that should require user approval before execution in the client layer.

## Project Structure

```text
.
├── auth.py
├── gmail_client.py
├── server.py
├── requirements.txt
├── Dockerfile
├── .gitignore
└── README.md
```

## Notes

This project is primarily intended for AI-powered integrations, where an MCP client can use Gmail tools in a constrained, user-approved workflow. The design favors explicit tool boundaries and secure authentication handling.

## Contributing

Contributions are welcome. If you plan to make changes, keep the project focused on secure Gmail access, maintain clear tool contracts, and validate any new environment variables or deployment requirements.

## Support

For issues related to project setup, Gmail OAuth, or deployment configuration, review the environment variable configuration and confirm your Google/WorkOS settings are correct before debugging the application code.
