import re

from langchain_core.documents import Document


def clean_legal_text(text: str) -> str:
    """
    Clean legal PDF text for RAG.
    - Preserves section titles, numbers, case references, citations.
    - Removes TOC dots, headers, footers, page numbers.
    - Collapses inline newlines so paragraphs flow naturally.
    """

    # Remove headers/footers like "Introductory [Chap 1]" or "Syn A]"
    text = re.sub(r'\bIntroductory\s*\[.*?\]|\bSyn\s*[A-Z]+\]?', ' ', text, flags=re.IGNORECASE)

    # Remove standalone page numbers
    text = re.sub(r'\n?\s*\d+\s*\n', '\n', text)

    # Remove TOC filler dots/dashes
    text = re.sub(r'[\.\-\s]{6,}', ' ', text)
    text = re.sub(r'^\s*[\.·\-\s]{5,}\s*$', ' ', text, flags=re.MULTILINE)

    # Fix hyphenated words broken at line breaks (e.g., Consti-\ntution → Constitution)
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)

    # 🚀 Collapse all "intra-paragraph" newlines into spaces
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # Ensure paragraph breaks (double \n) are normalized
    text = re.sub(r'\n{2,}', '\n\n', text)

    # Normalize spaces
    text = re.sub(r'[ \t]+', ' ', text).strip()

    # Remove any strange OCR junk
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # keep only ASCII safely

    return text


def clean_and_prepare_docs(start_page_num: int, end_page_num: int, docs: list[Document]):
    page_num = start_page_num
    clean_docs: list[Document] = []

    for i in range(len(docs)):
        doc = docs[i]
        doc.page_content = clean_legal_text(doc.page_content)
        doc.metadata["page_label"] = page_num
        page_num += 1

        clean_docs.append(doc)

    return clean_docs
