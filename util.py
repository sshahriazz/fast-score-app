import pymupdf
from openai import OpenAI
import json

client = OpenAI()

def get_content_from_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ''
    for page in doc:
        text += page.get_text()
    fonts = set()

    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block["lines"]:
                for span in line["spans"]:
                    fonts.add(span['font'])
    # print(fonts)
    presentation = {
        'page_count': doc.page_count,
        'word_count': len(text.split()),
        'fonts': list(fonts)
    }
    # print(presentation)
    return text, presentation


def generate_system_prompt():
    prompt = """You are an exceptional HR professional assistant designed to extract and format valuable information from Curriculum Vitae (CV) into JSON.
    You must strictly follow the following example JSON format.
    Example JSON:
    {
      "contact_information": {
        "name": "",
        "phone": "",
        "email": "",
        "social_links": {
          "facebook": "",
          "twitter": "",
          "instagram": "",
          "linkedin": "",
          "github": ""
        }
      },
      "sections": [list of sections in the CV (e.g. Contact information, Education, Professional experience, Skills, Awards, Certifications)],
      "work_experience": {
        "number_of_jobs": "",
        "jobs_info": [
          {
            "role": "",
            "organization": ""
          }
        ]
      },
      "education": [
        {
          "degree": "",
          "discipline": "",
          "institute": ""
        }
      ],
      "skills": {
        "Soft Skills": [],
        "Technical/Professional Skills": [],
        "Other Skills": []
      }
    }
    """
    return prompt


def generate_user_prompt(content):
    return f'"""CV Content: {content}"""'


def get_formatted_resume_content(content):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": generate_system_prompt()},
            {"role": "user", "content": generate_user_prompt(content)}
        ]
    )
    return response.choices[0].message.content


if __name__ == '__main__':
    get_content_from_pdf('uploads/2b18ceb6-8aef-4289-b2bc-db2f94375733.pdf')
