from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore


def load_text(file_path):

    with open(str(file_path), "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text: str):
    """
    Split text into overlapping chunks using LangChain.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    return chunks


if __name__ == "__main__":

    document = load_text("sample.txt")

    chunks = chunk_text(document)

    print(f"\nTotal Chunks: {len(chunks)}\n")

    for index, chunk in enumerate(chunks, start=1):

        print("=" * 60)
        print(f"Chunk {index}")
        print("=" * 60)

        print(chunk)
        print()
