import base64
from email.message import EmailMessage

from googleapiclient.discovery import build

from auth import get_credentials


def get_gmail_service():
    credentials = get_credentials()

    return build(
        "gmail",
        "v1",
        credentials=credentials,
    )


def search_emails(query="", max_results=10):
    service = get_gmail_service()

    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results,
    ).execute()

    messages = result.get("messages", [])

    emails = []

    for message in messages:
        data = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="metadata",
            metadataHeaders=[
                "From",
                "Subject",
                "Date",
            ],
        ).execute()

        headers = {
            header["name"]: header["value"]
            for header in data["payload"]["headers"]
        }

        emails.append(
            {
                "id": message["id"],
                "from": headers.get("From"),
                "subject": headers.get("Subject"),
                "date": headers.get("Date"),
                "snippet": data.get("snippet"),
            }
        )

    return emails


def send_email(to: str, subject: str, body: str):
    service = get_gmail_service()

    message = EmailMessage()
    message.set_content(body)

    message["To"] = to
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    result = service.users().messages().send(
        userId="me",
        body={
            "raw": encoded_message,
        },
    ).execute()

    return {
        "status": "sent",
        "message_id": result["id"],
        "to": to,
        "subject": subject,
    }


if __name__ == "__main__":
    emails = search_emails(
        query="newer_than:7d",
        max_results=5,
    )

    for email in emails:
        print(email)
        print("-" * 80)