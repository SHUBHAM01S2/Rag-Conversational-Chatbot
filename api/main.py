import os
import uuid
import shutil
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from api.pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRequest
from api.langchain_utils import get_rag_chain
from api.db_utils import create_tables, insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record
from api.chroma_utils import index_document_to_chroma, delete_doc_from_chroma

logging.basicConfig(filename='app.log', level=logging.INFO)
app = FastAPI()
create_tables()  # create DB tables at startup

@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id or str(uuid.uuid4())
    logging.info(f"Session: {session_id}, Query: {query_input.question}")
    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(query_input.model.value)
    answer = rag_chain.invoke({"input": query_input.question, "chat_history": chat_history})['answer']
    insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)

@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = [".pdf", ".docx", ".html"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    temp_file = f"temp_{file.filename}"
    try:
        with open(temp_file, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file, file_id)
        if success:
            return {"message": f"{file.filename} uploaded", "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail="Failed to index document")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return [
        {
            "file_id": doc["id"], 
            "filename": doc["filename"], 
            "upload_timestamp": doc["upload_timestamp"]
        } 
        for doc in get_all_documents()
    ]

@app.post("/delete-doc")
def delete_document(request: DeleteFileRequest):
    if delete_doc_from_chroma(request.file_id):
        delete_document_record(request.file_id)
        return {"deleted": True}
    return {"deleted": False, "error": "Failed to delete from Chroma"}
