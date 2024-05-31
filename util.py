import pymupdf
from openai import OpenAI
import os

client = OpenAI()


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
                        fonts.add(span['font'])
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
        'font_color': [[r, g, b] for r, g, b in font_color]
    }
    return {
        'status': 200,
        'text': text,
        'presentation': presentation
    }


def generate_system_prompt():
    prompt = """You are an exceptional HR professional assistant designed to extract and format valuable information based on the provided Curriculum Vitae (CV) into JSON format.
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
      "sections": [list of sections in the CV (e.g. Contact information, Profile Summary, Education, Professional experience, Skills, Awards, Certifications)],
      "profile_summary": "Pluck the section from the CV if and only if the section is present in CV",
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
    res = get_content_from_pdf('uploads/Yuvraj_Parmar_Resume_2023_v2.pdf')
    print(res)
    # get_decimal_to_rgb_color(0)
