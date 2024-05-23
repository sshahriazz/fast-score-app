import pymupdf
from openai import OpenAI
import json

client = OpenAI()


def get_decimal_to_rgb_color(color):
    # Convert to hexadecimal and remove the '0x' prefix
    color_hex = f"{color:06x}"
    # print(color_hex)
    # Extract the red, green, and blue components
    red = int(color_hex[0:2], 16)
    green = int(color_hex[2:4], 16)
    blue = int(color_hex[4:6], 16)

    # Combine into an RGB tuple
    return (red, green, blue)


def get_content_from_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ''
    for page in doc:
        text += page.get_text()
    fonts = set()
    font_color = set()

    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            # print(block)
            for line in block["lines"]:
                for span in line["spans"]:
                    fonts.add(span['font'])
                    # print(span['color'])
                    font_color.add(get_decimal_to_rgb_color(span['color']))

    # print(fonts)
    font_color_list = [[r, g, b] for r, g, b in font_color]
    presentation = {
        'page_count': doc.page_count,
        'word_count': len(text.split()),
        'fonts': list(fonts),
        'font_color': font_color_list
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
    # get_decimal_to_rgb_color(0)
