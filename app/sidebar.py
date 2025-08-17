import streamlit as st
from api_utils import upload_document, list_documents, delete_document


def display_sidebar():
    # Model selection
    model_options = ["gpt-4o", "gpt-4o-mini"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # Document upload
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html"])
    if uploaded_file and st.sidebar.button("Upload"):
        with st.spinner("Uploading..."):
            upload_response = upload_document(uploaded_file)
            if upload_response and "file_id" in upload_response:
                st.sidebar.success(
                    f"File uploaded successfully with ID {upload_response['file_id']}."
                )
                st.session_state.documents = list_documents()
            else:
                st.sidebar.error(
                    f"Failed to upload file: {upload_response.get('error', 'Unknown error')}"
                    if upload_response else "Upload failed"
                )

    # List and delete documents
    st.sidebar.header("Uploaded Documents")
    if st.sidebar.button("Refresh Document List"):
        st.session_state.documents = list_documents()

    # Display document list and delete functionality
    if "documents" in st.session_state and st.session_state.documents:
        for doc in st.session_state.documents:
            st.sidebar.text(f"{doc['name']} (ID: {doc['file_id']})")

        selected_file_id = st.sidebar.selectbox(
            "Select a document to delete",
            options=[doc["file_id"] for doc in st.session_state.documents],
            format_func=lambda fid: next(
                (doc["name"] for doc in st.session_state.documents if doc["file_id"] == fid),
                fid,
            ),
        )

        if st.sidebar.button("Delete Selected Document"):
            delete_response = delete_document(selected_file_id)
            if delete_response and "deleted" in delete_response:
                st.sidebar.success(f"Document deleted successfully.")
                st.session_state.documents = list_documents()
            else:
                st.sidebar.error(
                    f"Failed to delete document: {delete_response.get('error', 'Unknown error')}"
                    if delete_response else "Delete failed"
                )
