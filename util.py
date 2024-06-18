import pymupdf
from openai import OpenAI
import os


API_KEY = "sk-proj-jFruYRvMQ3K6oXpythznT3BlbkFJ2MapZaxyalVnkkVZ6eTQ"

client = OpenAI(api_key=API_KEY)


def get_decimal_to_rgb_color(color):
    # Convert to hexadecimal and remove the '0x' prefix
    color_hex = f"{color:06x}"
    # print(color_hex)
    # Extract the red, green, and blue components
    red = int(color_hex[0:2], 16)
    green = int(color_hex[2:4], 16)
    blue = int(color_hex[4:6], 16)
    return red, green, blue


def get_text_styling_info(doc):
    fonts, font_color = set(), set()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            if block['type'] == 0:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        f = span['font']
                        if f.split('-')[0] != f:
                            fonts.add(f.split('-')[0])
                        elif f.split('+')[0] != f:
                            fonts.add(f.split('+')[0])
                        else:
                            fonts.add(f)
                        font_color.add(get_decimal_to_rgb_color(span['color']))
    return fonts, font_color


def get_content_from_pdf(file_path):
    try:
        doc = pymupdf.open(file_path)
    except:
        return {'status': 404}
    finally:
        os.remove(file_path)

    text = ''
    for page in doc:
        text += page.get_text()
    if not text:
        return {'status': 404}
    fonts, font_color = set(), set()
    try:
        fonts, font_color = get_text_styling_info(doc)
    except:
        pass
    presentation = {
        'page_count': doc.page_count,
        'word_count': len(text.split()),
        'fonts': list(fonts),
        'colors': [[r, g, b] for r, g, b in font_color]
    }
    return {
        'status': 200,
        'text': text,
        'presentation': presentation
    }


def generate_system_prompt():
    prompt = """You are an exceptional HR professional assistant designed to extract and format valuable information based on the provided Curriculum Vitae (CV) into JSON format.
    You must strictly adhere to the following example JSON format and include all the fields. If data is not present, leave the fields empty and never make up something.
    Example JSON:
    {
      "contact_information": {
        "name": "",
        "phone": "",
        "email": "",
        "address": "",
        "social_links": {
          "facebook": "",
          "twitter": "",
          "instagram": "",
          "linkedin": "",
          "github": ""
        }
      },
      "sections": [list of sections in the CV (e.g. Contact information, Profile Summary, Education, Professional experience, Skills, Awards, Certifications)],
      "profile_summary": "Pluck the section from the CV if and only if the section is present in CV",
      "work_experience": {
        "number_of_jobs": "",
        "jobs_info": [
          {
            "role": "",
            "organization": "",
            "bullet_point: {
            "points": ["Information listed as bullet points if exists."],
            "status": "good/bad based on bullet point writing quality if exists",
            "suggestion": "How can be better if writing quality is not good and exists"
            }
          }
        ]
      },
      "education": [
        {
          "degree": "",
          "discipline": "",
          "institute": "",
          "bullet_point: {
            "points": ["Information listed as bullet points if exists."],
            "status": "good/bad based on bullet point writing quality if exists",
            "suggestion": "How can be better if writing quality is not good and exists"
          }
        }
      ],
      "skills": {
        "soft_skills": [],
        "technical/professional_skills": [],
        "other_skills": []
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


def calculate_score(obj):
    checked, passed, failed = 0, 0, 0
    # if filename and name is same
    try:
        if obj["file_information"]["is_naming_same"]:
            # print(1)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # is file type pdf
    try:
        if obj["file_information"]["content_type"] == "application/pdf":
            # print(2)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass

    # file size 20KB to 1MB
    try:
        if 20 * 1024 <= obj["file_information"]["size"] <= 1024 * 1024:
            # print(3)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # greater than 3 section
    # try:
    #     if len(obj["sections"]) >= 3:
    #         # print(4)
    #         passed += 1
    #     else:
    #         failed += 1
    #     checked += 1
    # except:
    #     pass
    # page count less than or equal 2
    try:
        if obj["presentation"]["page_count"] <= 2:
            # print(5)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # 350 to 800 words
    try:
        if 350 <= obj["presentation"]["word_count"] <= 800:
            # print(6)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass

    # file name suggested maximum of 24 characters
    # try:
    #     if obj["file_information"]["file_name_length"] <= 24:
    #         # print(7)
    #         passed += 1
    #     else:
    #         failed += 1
    #     checked += 1
    # except:
    #     pass
    # name exist in resume
    
    try:
        if obj["contact_information"]["name"]:
            # print(8)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # email exist in resume
    try:
        if obj["contact_information"]["email"] and '@' in obj["contact_information"]["email"]:
            # print(9)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # phone exists
    # try:
    #     if obj["contact_information"]["phone"]:
    #         # print(10)
    #         passed += 1
    #     else:
    #         failed += 1
    #     checked += 1
    # except:
    #     pass
    # number_of_jobs > 0
    try:
        if int(obj["work_experience"]["number_of_jobs"]) > 0:
            # print(11)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # job title present
    try:
        if int(obj["work_experience"]["number_of_jobs"]) > 0:
            jobs = obj["work_experience"]["jobs_info"]
            # print(12)
            if all(True if job["role"] else False for job in jobs):
                passed += 1
            else:
                failed += 0
            checked += 1
    except:
        pass
    # profile summary exist
    try:
        if obj["profile_summary"]:
            # print(13)
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # profile summary 50 to 80 words
    try:
        if obj["profile_summary"]:
            if 50 <= len(obj["profile_summary"].split()) <= 80:
                # print(14)
                passed += 1
            else:
                failed += 1
            checked += 1
    except:
        pass

    # social link > 1
    try:
        social_links = obj["contact_information"]["social_links"]
        cnt = sum(1 if value else 0 for _, value in social_links.items())
        # print(15)
        if cnt > 1:
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass
    # education check
    try:
        educations = obj["education"]
        if educations:
            # print(16)
            if all(True if education["degree"] else False for education in educations):
                passed += 1
            else:
                failed += 1
            checked += 1
    except:
        pass

    # unique font must be 1
    try:
        fonts = obj["presentation"]["fonts"]
        if len(fonts) == 1:
            passed += 1
        else:
            failed += 1
        checked += 1
    except:
        pass

    return {
        'checked': checked,
        'passed': passed,
        'failed': failed,
        'score': int((passed / checked) * 100)
    }


# if __name__ == '__main__':
#     res = get_content_from_pdf('uploads/Yuvraj_Parmar_Resume_2023_v2.pdf')
#     print(res)
# get_decimal_to_rgb_color(0)
