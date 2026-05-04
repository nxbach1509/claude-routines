#!/usr/bin/env python3
"""
One-time script to generate Gmail OAuth2 token.
Run locally ONCE, then paste the output JSON into GitHub Secrets as GMAIL_TOKEN_JSON.

Setup:
  1. Go to Google Cloud Console → Create a project
  2. Enable Gmail API
  3. Create OAuth2 credentials (Desktop app) → Download as credentials.json
  4. Run: python setup_gmail_token.py
  5. Copy the printed JSON → GitHub repo Settings → Secrets → GMAIL_TOKEN_JSON
"""

import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)

    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes),
    }

    print("\n✅ Paste the following JSON into GitHub Secrets as GMAIL_TOKEN_JSON:\n")
    print(json.dumps(token_data, indent=2))


if __name__ == "__main__":
    main()
