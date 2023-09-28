import os
import io
import nltk
import spacy
import re
from pdfminer3.converter import TextConverter
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfpage import PDFPage
from pdfminer3.layout import LAParams
from pyresparser import ResumeParser
from pdfreader import PDFDocument
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
nltk.download('stopwords')
nlp = spacy.load('en_core_web_sm')


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    pages = 0
    fonts = set()
    colors = set()

    with open(os.path.join(file), 'rb') as fh:
        doc = PDFDocument(fh)
        page = next(doc.pages())
        try:
            for page_layout in extract_pages(fh):
                for element in page_layout:
                    if isinstance(element, LTTextContainer):
                        for text_line in element:
                            for character in text_line:
                                if isinstance(character, LTChar):
                                    fonts.add(character.fontname)
                                    colors.add(character.graphicstate.scolor)
        except:
            pass

        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            pages += 1
        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return {'text': text, 'page': pages, 'fonts': list(fonts), 'colors': list(colors)}


def find_summary(input_text):

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Find the email address in the input text using regex
    email_match = re.search(email_pattern, input_text.lower())
    if email_match:
        email_address = email_match.group(0)

        # Find the index of the email address in the input text
        email_index = input_text.index(email_address)

        # Extract the text after the email address until the start of "WORK EXPERIENCES" section
        summary_text = input_text[email_index + len(email_address):]

        # Use regex to find the start of "WORK EXPERIENCES" section (all capital letter sentence)
        work_exp_start = re.search(r'\n[A-Z\s]+\n', summary_text)
        if work_exp_start:
            # Extract the text until the start of "WORK EXPERIENCES" section
            summary_text = summary_text[:work_exp_start.start()].strip()

            return summary_text
        else:
            paragraphs = input_text.split('\n\n')
            # Index 1 corresponds to the first paragraph
            first_paragraph = paragraphs[1]
            return first_paragraph

    else:
        return 'InvalidEmail'


def parse_resume_data(file):
    print("file path", file)
    try:
        resume_data = ResumeParser(os.path.join(file)).get_extracted_data()
    except Exception as error:
        print("Error in parsing", error)
        resume_data = {}
    return resume_data


def delete_files():

    # delete all files from /media/ folder
    folder = ''
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


def find_degree(text):
    degree_pattern = re.compile(
        r'\b(?:B\.?S\.?|M\.?S\.?|B\.?A\.?|M\.?A\.?|B\.?Tech\.?|M\.?Tech\.?|Ph\.?D\.?|Bachelor|Master|PhD)\b', re.IGNORECASE)

    # Find all matches of degrees in the text
    degrees_found = re.findall(degree_pattern, text)

    # Remove duplicates from the list
    unique_degrees = list(set(degrees_found))

    for degree in unique_degrees:
        print("Degree ============", degree)


def find_social_media_links(text):
    social_media_patterns = {
        "facebook": r"(?i)(?:https?:\/\/)?(?:www\.)?facebook\.com\/[\w\.]+",
        "twitter": r"(?i)(?:https?:\/\/)?(?:www\.)?twitter\.com\/[\w]+",
        "instagram": r"(?i)(?:https?:\/\/)?(?:www\.)?instagram\.com\/[\w\.]+",
        "linkedin": r"(?i)(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[\w\-]+",
        "github": r"(?i)(?:https?:\/\/)?(?:www\.)?github\.com\/[\w\-]+",
        # Add more social media patterns as needed
    }

    social_media_links = []

    for platform, pattern in social_media_patterns.items():
        matches = re.findall(pattern, text)
        if matches:
            # social_media_links[platform] = matches
            social_media_links.append(matches[0])
            # print(f"{platform.capitalize()} Links: {matches}")
        if not matches:
            # Find for Platform name in the text
            platform_matches = re.findall(platform, text, re.IGNORECASE)
            if platform_matches:
                social_media_links.append(platform_matches[0])
    return social_media_links
