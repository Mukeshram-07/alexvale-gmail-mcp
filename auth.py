import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]


def get_credentials() -> Credentials:
    """
    Create and refresh Gmail OAuth credentials using environment variables.

    Required environment variables:
    - GMAIL_CLIENT_ID
    - GMAIL_CLIENT_SECRET
    - GMAIL_REFRESH_TOKEN
    """

    creds = Credentials(
        token=None,
        refresh_token=os.environ["GMAIL_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GMAIL_CLIENT_ID"],
        client_secret=os.environ["GMAIL_CLIENT_SECRET"],
        scopes=SCOPES,
    )

    creds.refresh(Request())

    return creds


if __name__ == "__main__":
    try:
        credentials = get_credentials()

        print("Gmail OAuth authentication successful")
        print(f"Credentials valid: {credentials.valid}")

    except KeyError as error:
        print(
            f"Missing required environment variable: {error.args[0]}"
        )
        raise

    except Exception as error:
        print(f"Gmail OAuth authentication failed: {error}")
        raise