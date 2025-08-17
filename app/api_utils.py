import requests
import streamlit as st

API_BASE = "http://localhost:8000"

def get_api_response(question, session_id, model):
    data = {"question": question, "model": model}
    if session_id:
        data["session_id"] = session_id
    try:
        r = requests.post(f"{API_BASE}/chat", json=data)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")
        return {"error": str(e)}

def upload_document(file):
    try:
        files = {"file": (file.name, file, getattr(file, "type", "application/octet-stream"))}
        r = requests.post(f"{API_BASE}/upload-doc", files=files)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Upload API error: {e}")
        return {"error": str(e)}

def list_documents():
    try:
        r = requests.get(f"{API_BASE}/list-docs")
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"List docs API error: {e}")
        return []

def delete_document(file_id):
    try:
        r = requests.post(f"{API_BASE}/delete-doc", json={"file_id": file_id})
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Delete API error: {e}")
        return {"error": str(e)}

