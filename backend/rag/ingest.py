from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore
from pypdf import PdfReader


DOCUMENTS_DIR = Path("documents")


def load_txt(file_path: Path):
    """Load text from a .txt file."""

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf(file_path: Path):
    """Extract text from a PDF."""

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def load_documents(documents_dir=DOCUMENTS_DIR):
    """
    Load all supported documents (.txt and .pdf).

    Returns:
        [
            {
                "filename": "...",
                "category": "...",
                "text": "..."
            }
        ]
    """

    documents = []

    for file_path in documents_dir.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() == ".txt":
            text = load_txt(file_path)

        elif file_path.suffix.lower() == ".pdf":
            text = load_pdf(file_path)

        else:
            continue

        documents.append(
            {
                "filename": file_path.name,
                "category": file_path.parent.name,
                "text": text,
            }
        )

    return documents


def chunk_text(text: str):
    """
    Split text into overlapping chunks using LangChain.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
    )

    return splitter.split_text(text)


if __name__ == "__main__":

    documents = load_documents()

    print(f"\nLoaded {len(documents)} documents.\n")

    for document in documents:

        chunks = chunk_text(document["text"])

        print("=" * 60)
        print(f"Document : {document['filename']}")
        print(f"Category : {document['category']}")
        print(f"Chunks   : {len(chunks)}")
        print("=" * 60)