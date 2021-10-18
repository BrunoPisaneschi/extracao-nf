import pdfplumber

def read_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as _pdf:
        _first_page = _pdf.pages[0]
        return _first_page.extract_text()