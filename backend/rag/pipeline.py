from ingest import load_text, chunk_text
from embed import generate_embeddings

import sys
from pathlib import Path

# Add backend folder to Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from database.qdrant import create_collection, upload_embeddings

from pathlib import Path

current_dir = Path(__file__).parent
sample_file = current_dir / "sample.txt"

document = load_text(sample_file)

chunks = chunk_text(document)

embeddings = generate_embeddings(chunks)

create_collection()

upload_embeddings(chunks, embeddings)