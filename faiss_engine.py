import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ===============================
# CONFIG
# ===============================
INDEX_FILE = "students.index"
DIMENSION = 384  # all-MiniLM-L6-v2 embedding size

# ===============================
# LOAD MODEL ONCE
# ===============================
model = SentenceTransformer("all-MiniLM-L6-v2")

# ===============================
# LOAD OR CREATE INDEX
# ===============================
def load_or_create_index():
    if os.path.exists(INDEX_FILE):
        print("Loading existing FAISS index...")
        return faiss.read_index(INDEX_FILE)
    else:
        print("Creating new FAISS index...")
        base_index = faiss.IndexFlatIP(DIMENSION)
        return faiss.IndexIDMap(base_index)

index = load_or_create_index()

# ===============================
# SAVE INDEX
# ===============================
def save_index():
    faiss.write_index(index, INDEX_FILE)
    print("FAISS index saved.")


# ===============================
# ADD STUDENT
# ===============================
def register_student(student_id: int, summary_text: str):
    embedding = model.encode(summary_text)
    vector = np.array([embedding]).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(vector)

    # Add with custom ID
    index.add_with_ids(vector, np.array([student_id]))

    save_index()
    print(f"Student {student_id} added.")


# ===============================
# REMOVE STUDENT
# ===============================
def remove_student(student_id: int):
    index.remove_ids(np.array([student_id]))
    save_index()
    print(f"Student {student_id} removed.")


# ===============================
# MATCH JD
# ===============================
def match_jd(jd_text: str, top_k=5):
    if index.ntotal == 0:
        return []

    top_k = min(top_k, index.ntotal)

    embedding = model.encode(jd_text)
    vector = np.array([embedding]).astype("float32")

    faiss.normalize_L2(vector)

    scores, ids = index.search(vector, top_k)

    results = []
    for score, student_id in zip(scores[0], ids[0]):
        if student_id == -1:
            continue

        results.append({
            "student_id": int(student_id),
            "score": float(score)
        })

    return results
