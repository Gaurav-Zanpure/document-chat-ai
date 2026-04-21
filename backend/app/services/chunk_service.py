def chunk_text(pages, chunk_size=1000, overlap=200):
    chunks = []

    for page_data in pages:
        text = page_data["text"]
        page_num = page_data["page"]

        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append({
                    "text": chunk,
                    "page": page_num,
                    "chunk_index": chunk_index
                })

            start += (chunk_size - overlap)
            chunk_index += 1

    return chunks