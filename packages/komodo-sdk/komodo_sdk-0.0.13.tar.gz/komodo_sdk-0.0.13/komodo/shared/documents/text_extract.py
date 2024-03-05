import json
import re
import tempfile

import html2text
import textract
from bs4 import BeautifulSoup
from ftfy import ftfy
from unidecode import unidecode
from urlextract import URLExtract


def extract_text(path, payload, content_type):
    if content_type == 'text/html':
        html = payload.decode().strip()
        text = extract_text_from_html_bs4(html)
    else:
        text = textract.process(path).decode().strip()  # method='pdfminer'
    return to_clean_text(text)


def extract_urls(text):
    extractor = URLExtract(cache_dir=tempfile.gettempdir())
    return list(filter(lambda x: x.startswith('http'), list(set(extractor.find_urls(text)))))


def extract_urls_from_pdf(path):
    import PyPDF2
    PDFFile = open(path, 'rb')

    PDF = PyPDF2.PdfReader(PDFFile)
    pages = len(PDF.pages)
    key = '/Annots'
    uri = '/URI'
    ank = '/A'

    urls = []

    for page in range(pages):
        # print("Current Page: {}".format(page))
        pageSliced = PDF.pages[page]
        pageObject = pageSliced.get_object()
        if key in pageObject.keys():
            ann = pageObject[key]
            for a in ann:
                u = a.get_object()
                if uri in u[ank].keys():
                    # print(u[ank][uri])
                    urls.append(u[ank][uri])

    return urls


def extract_text_from_html(html):
    return html2text.html2text(html).strip()


def extract_text_from_html_bs4(html):
    soup = BeautifulSoup(html, 'html.parser')
    # append the text to the link
    for a in soup.select('a[href]'):
        a.contents.append(soup.new_string(' ({})'.format(a['href'])))

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # unwrap() all tags
    for tag in soup.select('*'):
        tag.unwrap()

    return soup.text.strip()


def extract_text_from_html5lib_bs4(html):
    soup = BeautifulSoup(html, features='html5lib')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    text = soup.get_text("\n")
    return "".join([s for s in text.strip().splitlines(True) if s.strip()])


def remove_extra_space(text):
    # First, replace multiple newlines with a single newline,
    # so you don't get empty paragraphs
    text = re.sub(r'\n\s*\n', '\n', text)

    # Split the text into lines
    lines = text.split('\n')

    # Wrap each line in a <p> tag and join them
    return '\n'.join(line.strip() for line in lines)


def replace_quoted_printable(text):
    try:
        import quopri
        decoded_text = quopri.decodestring(text).decode('utf-8')
        return unidecode(decoded_text)
    except ValueError as e:
        print("Warning: could not decode quoted printable text (not a big issue): ", e)
        return text


def to_clean_text(payload):
    if payload is None:
        return ''
    if isinstance(payload, bytes):
        payload = payload.decode('ascii', 'ignore')
    else:
        payload = payload.encode('ascii', 'ignore').decode('ascii', 'ignore')
    return replace_quoted_printable(remove_extra_space(ftfy(payload)))


def extract_text_between_ticks(text, tick='```', tag='json'):
    # Regular expression pattern to match text between ```json and ```
    pattern = rf'{tick}{tag}(.*?){tick}'
    match = re.search(pattern, text, re.DOTALL)

    if match:
        json_str = match.group(1).strip()  # Strip to remove any leading/trailing whitespace
        return to_clean_text(json_str)
    else:
        return to_clean_text(text)


def extract_json(text, tick='```'):
    text = extract_text_between_ticks(text, tick=tick, tag='json')
    if text is not None:
        try:
            text = json.dumps(json.loads(text))
        except:
            pass
    return to_clean_text(text)


if __name__ == '__main__':
    text = '''
    ```json
    {
      "personal_info": {
        "name": "JEFFREY S. LEVIN", 
        "address": "607 Sunnyhill Terrace\nRiver Vale, NJ 07675",
        "phone": "201.446.6158",
        "email": "jeffreylevin98@yahoo.com",
        "years_of_experience": null,
        "gender": null
      }
    }
    ```
    stuff here
    '''

    extracted_json = extract_text_between_ticks(text, tag='json')
    if extracted_json is not None:
        print(json.loads(json.dumps(extracted_json, indent=4, separators=(',', ': '))))
