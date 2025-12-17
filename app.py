import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Kai Actions API")

st.write("Kai Actions API is live.")

def handle_recap(data):
    convo = data.get("conversation", "")
    recap = f"""
- {convo[:60]}...
- Theme: truth finding its pace.
- Direction: one breath, one step.

Quiet question: What feels lighter now?
"""
    return {"recap": recap}

def handle_mirror(data):
    msg = data.get("message", "")
    reflection = "It sounds like you're holding care and honesty together — staying real."
    return {"reflection": reflection}

def handle_anchor(data):
    anchors = [
        "Feel your feet. Slow breath in… slow out. Want another?",
        "Notice the air on your skin. That’s real. Would you like one more?",
        "Let your shoulders drop. You can stop here. Do you want another?"
    ]
    import random
    return {"anchor": random.choice(anchors)}

def handle_save_reflection(data):
    text = data.get("text", "")
    timestamp = datetime.utcnow().isoformat()
    return {"message": f"Reflection saved at {timestamp}"}

# Simulate endpoints
path = st.experimental_get_query_params().get("path", [""])[0]
body = st.text_area("Paste JSON body here (for testing):")

if st.button("Run"):
    try:
        data = json.loads(body) if body else {}
    except:
        st.error("Invalid JSON.")
        st.stop()

    if path == "recap":
        st.json(handle_recap(data))
    elif path == "mirror":
        st.json(handle_mirror(data))
    elif path == "anchor":
        st.json(handle_anchor(data))
    elif path == "save_reflection":
        st.json(handle_save_reflection(data))
    else:
        st.error("Unknown path.")
