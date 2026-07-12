import os

from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import WorkOSProvider

from gmail_client import search_emails, send_email


# --------------------------------------------------
# Initialize MCP Server
# --------------------------------------------------

BASE_URL = "https://alexvale-gmail-mcp.onrender.com"

auth = WorkOSProvider(
    client_id=os.environ["WORKOS_CLIENT_ID"],
    client_secret=os.environ["WORKOS_CLIENT_SECRET"],
    authkit_domain=os.environ.get(
        "WORKOS_AUTHKIT_DOMAIN",
        "https://studious-sweetness-40-staging.authkit.app"
    ),
    base_url=BASE_URL,
    resource_base_url=BASE_URL,
    require_authorization_consent="external",
)

mcp = FastMCP(
    "ALEXVALE Gmail MCP",
    auth=auth,
)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@mcp.tool()
def health_check() -> dict:
    """Check whether the Gmail MCP server is online."""

    return {
        "status": "online",
        "service": "ALEXVALE Gmail MCP",
    }


# --------------------------------------------------
# Search Gmail
# --------------------------------------------------

@mcp.tool()
def search_gmail(
    query: str = "newer_than:7d",
    max_results: int = 10,
) -> list[dict]:
    """
    Search the user's Gmail mailbox.

    Supports Gmail search syntax.

    Examples:
    - newer_than:7d
    - is:unread
    - from:google.com
    - subject:interview
    """

    max_results = max(1, min(max_results, 50))

    return search_emails(
        query=query,
        max_results=max_results,
    )


# --------------------------------------------------
# Get Recent Emails
# --------------------------------------------------

@mcp.tool()
def get_recent_emails(
    max_results: int = 10,
) -> list[dict]:
    """Get recent Gmail messages."""

    max_results = max(1, min(max_results, 50))

    return search_emails(
        query="newer_than:7d",
        max_results=max_results,
    )


# --------------------------------------------------
# Get Unread Emails
# --------------------------------------------------

@mcp.tool()
def get_unread_emails(
    max_results: int = 10,
) -> list[dict]:
    """Get unread Gmail messages."""

    max_results = max(1, min(max_results, 50))

    return search_emails(
        query="is:unread",
        max_results=max_results,
    )


# --------------------------------------------------
# Send Gmail
# --------------------------------------------------

@mcp.tool()
def send_gmail(
    to: str,
    subject: str,
    body: str,
) -> dict:
    """
    Send an email using the user's Gmail account.

    This is a write action.
    The MCP client should request user approval before execution.
    """

    return send_email(
        to=to,
        subject=subject,
        body=body,
    )


# --------------------------------------------------
# Start MCP Server
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))

    print(f"Starting ALEXVALE Gmail MCP on port {port}")

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
    )