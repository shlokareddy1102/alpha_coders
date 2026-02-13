from pymongo import MongoClient
from datetime import datetime
import os

# ----------------------------
# MongoDB Connection
# ----------------------------

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "campus_placement"
COLLECTION_NAME = "students"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
students_collection = db[COLLECTION_NAME]

# Ensure unique index on student_id
students_collection.create_index("student_id", unique=True)


# ----------------------------
# SAVE OR UPDATE STUDENT
# ----------------------------
def save_student(student_id, summary, embedding):
    """
    Insert or update student.
    Embedding must already be a Python list.
    """

    document = {
        "student_id": student_id,
        "ai_processed": {
            "summary": summary,
            "embedding": embedding
        },
        "updated_at": datetime.utcnow()
    }

    students_collection.update_one(
        {"student_id": student_id},
        {
            "$set": document,
            "$setOnInsert": {"created_at": datetime.utcnow()}
        },
        upsert=True
    )


# ----------------------------
# REMOVE STUDENT
# ----------------------------
def remove_student(student_id):
    students_collection.delete_one({"student_id": student_id})


# ----------------------------
# GET ALL STUDENTS (FOR REBUILD)
# ----------------------------
def get_all_students():
    """
    Returns list of dicts:
    [
        {"id": 101, "embedding": [...]},
        ...
    ]
    """

    students = students_collection.find(
        {},
        {"student_id": 1, "ai_processed.embedding": 1}
    )

    result = []

    for student in students:
        if "ai_processed" in student and "embedding" in student["ai_processed"]:
            result.append({
                "id": student["student_id"],
                "embedding": student["ai_processed"]["embedding"]
            })

    return result
