from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from util import get_content_from_pdf, get_formatted_resume_content
import uuid
import shutil
import os
import json
import datetime

app = FastAPI()

# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "https://example.com",
# ]
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allows cookies to be included
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/health")
def health_check():
    return {
        "status": 200,
        "message": "API is healthy."
    }


@app.post("/uploadfile/")
def create_upload_file(file: UploadFile):
    if file.content_type != 'application/pdf':
        return {
            "status": 415,
            "message": "Please upload a pdf file.",
        }

    file_information = {
        'file_name': file.filename,
        'size': file.size,
        'content_type': file.content_type
    }

    # directory for saving uploaded files
    saved_dir = "uploads/"

    # Ensure the directory exists
    if not os.path.exists(saved_dir):
        os.makedirs(saved_dir)

    filename = f'{str(uuid.uuid4())}.pdf'
    saved_filepath = os.path.join(saved_dir, filename)

    try:
        # Efficiently save the file using shutil.copyfileobj()
        with open(saved_filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        return {
            'message': 'File saving issue'
        }

    modification_time = os.path.getmtime(saved_filepath)

    # Convert the timestamp to a readable date and time format
    file_information["modified_date"] = datetime.datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d')

    pdf_content, presentation = get_content_from_pdf(saved_filepath)
    os.remove(saved_filepath)

    # pdf_parsed_info = json.loads(get_formatted_resume_content(pdf_content))
    pdf_parsed_info = dict()
    pdf_parsed_info.update({'file_information': file_information})
    pdf_parsed_info.update({'presentation': presentation})

    return pdf_parsed_info
