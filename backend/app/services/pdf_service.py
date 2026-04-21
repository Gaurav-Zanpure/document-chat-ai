import fitz


def clean_text(text: str):
    # remove excessive newlines and spaces
    text = text.replace("\n", " ")
    text = " ".join(text.split())  # removes extra spaces
    return text


def extract_text_from_pdf(file_path: str):
    doc = fitz.open(file_path)

    pages = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()

        if text.strip():
            cleaned = clean_text(text)

            pages.append({
                "page": page_num,
                "text": cleaned
            })

    doc.close()
    return pages