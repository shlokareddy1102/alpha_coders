from pymongo import MongoClient
from datetime import datetime
import os

# ----------------------------
# MongoDB Connection
# ----------------------------

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
DB_NAME = "alpha_coders"
COLLECTION_NAME = "students"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
students_collection = db[COLLECTION_NAME]


# ----------------------------
# ID COUNTER
# ----------------------------

def get_next_numeric_id():
    counter = db["counters"].find_one_and_update(
        {"_id": "student_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return counter["seq"]


# ----------------------------
# CREATE STUDENT
# ----------------------------

def create_student(student_document):
    students_collection.insert_one(student_document)


# ----------------------------
# GET STUDENT BY UUID
# ----------------------------

def get_student_by_uuid(student_id):
    return students_collection.find_one({"student_id": student_id})


# ----------------------------
# GET STUDENTS BY NUMERIC IDS
# ----------------------------

def get_students_by_numeric_ids(numeric_ids):
    return list(
        students_collection.find({"numeric_id": {"$in": numeric_ids}})
    )


# ----------------------------
# UPDATE STUDENT
# ----------------------------

def update_student(student_id, update_data):
    students_collection.update_one(
        {"student_id": student_id},
        {"$set": update_data}
    )


# ----------------------------
# DELETE STUDENT
# ----------------------------

def delete_student(student_id):
    students_collection.delete_one({"student_id": student_id})


# ----------------------------
# GET ALL STUDENTS (FOR FAISS REBUILD)
# ----------------------------

def get_all_students():
    return list(students_collection.find())

