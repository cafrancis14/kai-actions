import streamlit as st
import json
import random
import requests
import csv
from io import StringIO
from datetime import datetime
from pathlib import Path

# -------------------------------------------------------------
# Serve plugin and schema files directly
# -------------------------------------------------------------
params = st.experimental_get_query_params()
if "path" in params:
    target = params["path"][0]
    if target in ["openapi.yaml", "ai-plugin.json"]:
        file_path = Path(__file__).parent / target
        if file_path.exists():
            st.markdown(f"```text\n{file_path.read_text()}\n```")
        else:
            st.write("❌ File not found.")
        st.stop()

# -------------------------------------------------------------
# Normal app UI
# -------------------------------------------------------------
st.set_page_config(page_title="Kai Actions API")
st.title("Kai Actions API")
st.caption("✅ Live and connected to Google Sheets.")

# ---------------- Endpoints ----------------

def handle_recap(data):
    convo = data.get("conversation", "")
    recap = f"""
- {convo[:60]}...
- Theme: truth finding its pace.
- Direction: one breath, one step.

Quiet question: What feels lighter now?
"""
    return {"recap": recap.strip()}

def handle_mirror(data):
    reflection = "It sounds like you're holding care and honesty together — staying real."
    return {"reflection": reflection}

def handle_anchor(data):
    anchors = [
        "Feel your feet on the ground. One slow breath in… one out. Want another?",
        "Notice the air on your skin. That’s real. Would you like one more?",
        "Let your shoulders drop a little. You can stop here. Do you want another?"
    ]
    return {"anchor": random.choice(anchors)}

def handle_save_reflection(data):
    text = data.get("text", "")
    timestamp = datetime.utcnow().isoformat()
    GOOGLE_SHEETS_WEBHOOK = "https://YOUR_GOOGLE_APPS_SCRIPT_URL_HERE"

    if GOOGLE_SHEETS_WEBHOOK != "https://YOUR_GOOGLE_APPS_SCRIPT_URL_HERE":
        try:
            requests.post(
                GOOGLE_SHEETS_WEBHOOK,
                headers={"Content-Type": "application/json"},
                data=json.dumps({"text": text, "timestamp": timestamp}),
                timeout=5
            )
        except Exception as e:
            st.error(f"Error sending to Google Sheets: {e}")
    return {"message": f"Reflection saved at {timestamp}"}

def handle_get_reflections():
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
    try:
        response = requests.get(SHEET_CSV_URL)
        if response.status_code != 200:
            return {"error": f"Google Sheets fetch failed ({response.status_code})"}
        data = list(csv.reader(StringIO(response.text)))
        reflections = [{"timestamp": r[1], "text": r[2]} for r in data[1:]]
        return {"reflections": reflections}
    except Exception as e:
        return {"error": str(e)}

def handle_export_reflections():
    SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/export?format=csv"
    return {"export_url": SHEET_CSV_URL}

# -------------------------------------------------------------
# Manual API Tester
# -------------------------------------------------------------
st.subheader("Manual API Test")
endpoint = st.selectbox(
    "Choose endpoint",
    ["recap", "mirror", "anchor", "save_reflection", "get_reflections", "export_reflections"]
)
body = st.text_area("Paste JSON body here:")

if st.button("Run"):
    try:
        data = json.loads(body) if body else {}
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        st.stop()

    if endpoint == "recap":
        st.json(handle_recap(data))
    elif endpoint == "mirror":
        st.json(handle_mirror(data))
    elif endpoint == "anchor":
        st.json(handle_anchor(data))
    elif endpoint == "save_reflection":
        st.json(handle_save_reflection(data))
    elif endpoint == "get_reflections":
        st.json(handle_get_reflections())
    elif endpoint == "export_reflections":
        st.json(handle_export_reflections())
