"""
call_nexus_agent.py — Call the NEXUS_AGENT via Snowflake REST API or Connector.

This script demonstrates calling a Cortex Agent from outside Snowflake —
the pattern for embedding agents in Streamlit apps, Python backends, or CI/CD.

────────────────────────────────────────────────────────────────────────────────
SETUP
────────────────────────────────────────────────────────────────────────────────

1. Install dependencies:

   pip3 install requests snowflake-connector-python

2. Run from your terminal:

   python3 call_nexus_agent.py

────────────────────────────────────────────────────────────────────────────────
"""

import json
import sys
import time
import threading


# ──────────────────────────────────────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────────────────────────────────────

# Your Snowflake account URL (NO https://)
ACCOUNT_URL = "<your-account_url>"

# PAT AUTH
PAT_TOKEN = "your_pat"

# Connector fallback (only used if PAT_TOKEN is empty)
SNOWFLAKE_USER = "<your-username>"
SNOWFLAKE_PASSWORD = "<your-password>"
SNOWFLAKE_ACCOUNT = "<your-account>"

# Agent config
AGENT_NAME = "NEXUS_HOL.AGENTS.NEXUS_AGENT"

QUESTION = (
    "Which clients have the highest portfolio value? "
    "Show me the top 5."
)


# ──────────────────────────────────────────────────────────────────────────────
# Progress Indicator
# ──────────────────────────────────────────────────────────────────────────────

stop_spinner = False


def progress_indicator():
    elapsed = 0

    while not stop_spinner:
        if elapsed == 0:
            print("Working...")
            print(
                "The Cortex Agent is reasoning, calling tools, "
                "generating SQL, and executing queries."
            )
            print(
                "This commonly takes 20–30 seconds for multi-tool workflows.\n"
            )
        else:
            print(f"...still working ({elapsed}s elapsed)")

        time.sleep(5)
        elapsed += 5


# ──────────────────────────────────────────────────────────────────────────────
# Response Parsing
# ──────────────────────────────────────────────────────────────────────────────

def extract_text_from_agent_response(result):
    """
    Extract assistant text from Cortex Agent REST response.
    """

    text = ""

    # REST API response format
    if "content" in result:
        for block in result.get("content", []):
            if block.get("type") == "text":
                text += block.get("text", "")

    # DATA_AGENT_RUN response format
    elif "messages" in result:
        for msg in result.get("messages", []):
            if msg.get("role") == "assistant":
                for block in msg.get("content", []):
                    if block.get("type") == "text":
                        text += block.get("text", "")

    return text


# ──────────────────────────────────────────────────────────────────────────────
# PAT + REST API
# ──────────────────────────────────────────────────────────────────────────────

def call_via_pat(account_url, pat, agent_name, question):
    """
    Call the named Cortex Agent using REST API + PAT.
    """

    import requests

    database, schema, name = agent_name.split(".")

    url = (
        f"https://{account_url}"
        f"/api/v2/databases/{database}"
        f"/schemas/{schema}"
        f"/agents/{name}:run"
    )

    headers = {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Snowflake-Authorization-Token-Type":
            "PROGRAMMATIC_ACCESS_TOKEN",
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question,
                    }
                ],
            }
        ],
        "stream": False,
    }

    print(f"[REST API] calling {agent_name} ...")
    print(f"[REST API] question: {question}\n")

    # Start progress indicator
    global stop_spinner
    stop_spinner = False

    spinner = threading.Thread(target=progress_indicator)
    spinner.start()

    try:
        resp = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=180,
        )

        stop_spinner = True
        spinner.join()

        resp.raise_for_status()

        result = resp.json()

        text = extract_text_from_agent_response(result)

        print("\n" + "─" * 60)
        print("AGENT RESPONSE:")
        print("─" * 60)

        if text:
            print(text)
        else:
            print(json.dumps(result, indent=2))

    except Exception as e:
        stop_spinner = True
        spinner.join()

        print("\nERROR:")
        print(str(e))


# ──────────────────────────────────────────────────────────────────────────────
# Connector + DATA_AGENT_RUN
# ──────────────────────────────────────────────────────────────────────────────

def call_via_connector(
    account,
    user,
    password,
    agent_name,
    question,
):
    """
    Call the agent using DATA_AGENT_RUN.
    """

    import snowflake.connector

    print(f"[Connector] connecting to {account} as {user} ...")

    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
    )

    request_json = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question,
                    }
                ],
            }
        ],
        "stream": False,
    })

    sql = f"""
    SELECT SNOWFLAKE.CORTEX.DATA_AGENT_RUN(
        '{agent_name}',
        {json.dumps(request_json)}
    ) AS response
    """

    print(f"[Connector] calling {agent_name} ...")
    print(f"[Connector] question: {question}\n")

    # Start progress indicator
    global stop_spinner
    stop_spinner = False

    spinner = threading.Thread(target=progress_indicator)
    spinner.start()

    try:
        cursor = conn.cursor()

        cursor.execute(sql)

        row = cursor.fetchone()

        stop_spinner = True
        spinner.join()

        cursor.close()
        conn.close()

        if not row or not row[0]:
            print("No response returned.")
            return

        result = (
            json.loads(row[0])
            if isinstance(row[0], str)
            else row[0]
        )

        text = extract_text_from_agent_response(result)

        print("\n" + "─" * 60)
        print("AGENT RESPONSE:")
        print("─" * 60)

        if text:
            print(text)
        else:
            print(json.dumps(result, indent=2))

    except Exception as e:
        stop_spinner = True
        spinner.join()

        print("\nERROR:")
        print(str(e))


# ──────────────────────────────────────────────────────────────────────────────
# Validation
# ──────────────────────────────────────────────────────────────────────────────

def validate_config():
    errors = []

    if not ACCOUNT_URL:
        errors.append("ACCOUNT_URL is not set.")

    if not PAT_TOKEN:
        if "<your-username>" in SNOWFLAKE_USER:
            errors.append("SNOWFLAKE_USER is not set.")

        if "<your-password>" in SNOWFLAKE_PASSWORD:
            errors.append("SNOWFLAKE_PASSWORD is not set.")

    if errors:
        print("Configuration errors — open this file and fill in your values:\n")

        for e in errors:
            print(f"  ✗ {e}")

        sys.exit(1)


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    validate_config()

    start = time.time()

    if PAT_TOKEN:
        print("Auth method: PAT REST API\n")

        call_via_pat(
            ACCOUNT_URL,
            PAT_TOKEN,
            AGENT_NAME,
            QUESTION,
        )

    else:
        print("Auth method: Connector → DATA_AGENT_RUN\n")

        call_via_connector(
            SNOWFLAKE_ACCOUNT,
            SNOWFLAKE_USER,
            SNOWFLAKE_PASSWORD,
            AGENT_NAME,
            QUESTION,
        )

    elapsed = round(time.time() - start)

    print(f"\n[done in {elapsed}s]")
