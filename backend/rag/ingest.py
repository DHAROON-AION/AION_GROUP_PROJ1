from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter  # type: ignore


DOCUMENTS_DIR = Path("documents")


def load_documents(documents_dir=DOCUMENTS_DIR):
    """
    Load every .txt document from the documents directory.

    Returns:
        [
            {
                "filename": "...",
                "category": "...",
                "text": "..."
            },
            ...
        ]
    """

    documents = []

    for file_path in documents_dir.rglob("*.txt"):

        with open(file_path, "r", encoding="utf-8") as f:

            documents.append(
                {
                    "filename": file_path.name,
                    "category": file_path.parent.name,
                    "text": f.read()
                }
            )

    return documents


def chunk_text(text: str):
    """
    Split text into overlapping chunks using LangChain.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", " ", ""]
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

        for i, chunk in enumerate(chunks, start=1):
            print(f"\nChunk {i}")
            print("-" * 40)
            print(chunk)