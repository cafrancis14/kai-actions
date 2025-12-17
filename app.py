import streamlit as st
import json
import random
from datetime import datetime
import requests
import os
import streamlit as st
from pathlib import Path

# Serve ai-plugin.json or openapi.yaml directly if requested
params = st.experimental_get_query_params()
if "file" in params:
    filename = params["file"][0]
    path = Path(__file__).parent / filename
    if path.exists():
        with open(path, "r") as f:
            st.download_button("Download", f, file_name=filename)
        st.stop()

st.set_page_config(page_title="Kai Actions API")

st.write("✅ Kai Actions API is live with Google Sheets support.")

# --- Utility functions ---
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
    msg = data.get("message", "")
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

    # OPTIONAL: Add your Google Apps Script webhook URL here ↓↓↓
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

# --- Test interface (for manual checks) ---
st.subheader("Manual API Test")
path = st.selectbox("Endpoint", ["recap", "mirror", "anchor", "save_reflection"])
body = st.text_area("Paste JSON body here:")

if st.button("Run"):
    try:
        data = json.loads(body) if body else {}
    except Exception as e:
        st.error(f"Invalid JSON: {e}")
        st.stop()

    if path == "recap":
        st.json(handle_recap(data))
    elif path == "mirror":
        st.json(handle_mirror(data))
    elif path == "anchor":
        st.json(handle_anchor(data))
    elif path == "save_reflection":
        st.json(handle_save_reflection(data))
