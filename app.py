from fastapi import FastAPI, Request, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from categorize_skills import skills_category
from scanner.pdfanalyzer import find_social_media_links, find_degree, pdf_reader, find_summary, parse_resume_data, parse_resume_data, delete_files
import aiofiles
import os
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/")
async def root(file: UploadFile):

    if (file.content_type != "application/pdf"):
        return {
            "message": "Please upload a pdf file.",
        }
    try:
        filepath = os.path.join('./files', os.path.basename(file.filename))
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(100):
                await f.write(chunk)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='There was an error uploading the file')
    finally:
        await file.close()

    filepath = os.path.join('./files', os.path.basename(file.filename))
    file_information = {
        "fileName": "",
        "name": "",
        "modified_date": "",
        "size": 0,
        "content_type": "",
        "mod_gap": ""
    }

    presentation = {
        "page_count": 0,
        "word_count": 0,
        "fonts": [],
        "colors": [],
    }

    structure = {
        "sections": [],
        "contact_information": "",
    }

    contact_information = {
        "name": "",
        "phone": "",
        "email": "",
        "social_links": []
    }

    education = {
        "degrees": [],
        "skills": "",
        "skills_category": {},
    }
    work_experience = {
        "number_of_jobs": 0,
        "job_titles": [],
        "company": [],
    }
    score_data = {
        "passed": 0,
        "failed": 0,
        "dismissed": 0,
        "score": 0,
        "tests": 0,
        "score_history": []
    }
    summary = ""

    if (file):
        file_information["fileName"] = file.filename
        file_information["modified_date"] = ''
        file_information["mod_gap"] = ''
        file_information["size"] = round(float(file.size) / 1024 / 1024, 2)
        file_information["content_type"] = file.content_type
    data = pdf_reader(filepath)
    presentation['page_count'] = data['page']
    presentation['word_count'] = len(data['text'].split())

    presentation['fonts'] = data['fonts']

    presentation['colors'] = data['colors']

    summary = find_summary(data['text'])

    parsed_data = parse_resume_data(filepath)
    selected_keys = []
    for key, value in parsed_data.items():
        if value is not None and value != "" and value != [] and value != 0.0:
            selected_keys.append(key)
    structure['sections'] = selected_keys

    if parsed_data['designation'] is not None:
        work_experience['number_of_jobs'] = len(parsed_data['designation'])
    else:
        work_experience['number_of_jobs'] = 0
    work_experience['job_titles'] = parsed_data['designation']
    work_experience['company'] = parsed_data['company_names']

    if parsed_data['email'] is not None and parsed_data['mobile_number'] is not None and parsed_data['name'] is not None:
        structure['contact_information'] = parsed_data['email'] + \
            " " + parsed_data['mobile_number']

    file_information['name'] = parsed_data['name']
    find_degree(data['text'])
    # form.clean()

    # Contact Information
    contact_information['name'] = parsed_data['name']
    contact_information['phone'] = parsed_data['mobile_number']
    contact_information['email'] = parsed_data['email']

    contact_information["social_links"] = find_social_media_links(data['text'])

    # Education
    education['degrees'] = parsed_data['degree']
    education['skills'] = parsed_data['skills']
    education['skills_category'] = skills_category(parsed_data['skills'])

    # calculate score based on presence and absent of data on the dict
    if (file_information["name"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (file_information["content_type"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (file_information["size"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (file_information["mod_gap"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (presentation["page_count"] > 0):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (presentation["word_count"] > 350 and presentation["word_count"] < 800):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (len(presentation["fonts"]) > 1):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (len(presentation["colors"]) > 1):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (len(structure["sections"]) > 3):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (structure["contact_information"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (contact_information["name"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (contact_information["phone"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (contact_information["email"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (len(contact_information["social_links"]) > 0):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (education["degrees"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (education["skills"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (education["skills_category"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (work_experience["number_of_jobs"] > 0):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (work_experience["job_titles"] is not None):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (work_experience["company"]):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    if (summary):
        score_data["passed"] += 1
        score_data["score"] += 1
    else:
        score_data["failed"] += 1

    score_data['tests'] = score_data["dismissed"] + \
        score_data["failed"] + score_data["passed"]

    os.unlink(filepath)

    return {
        "file_information": file_information,
        "presentation": presentation,
        "structure": structure,
        "contact_information": contact_information,
        "education": education,
        "work_experience": work_experience,
        "score_data": score_data,
        "summary": summary,
    }
