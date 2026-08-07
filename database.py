from datetime import datetime
from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))

db = client["face_attendance"]

students_collection = db["students"]
attendance_collection = db["attendance"]



# ==========================
# Database Connect
# ==========================

def create_database():
    print("MongoDB Connected Successfully")



# ==========================
# Register Student (5 Photos)
# ==========================

def register_student(name, image_paths, embeddings):

    students_collection.update_one(
        {"name": name},
        {
            "$set": {
                "name": name,
                "images": image_paths,
                "embeddings": [
                    e.tolist() for e in embeddings
                ]
            }
        },
        upsert=True
    )

    return True



# ==========================
# Get Students
# ==========================

def get_students():

    return list(
        students_collection.find()
    )



# ==========================
# Attendance
# ==========================

def mark_attendance(name):

    today = datetime.now().strftime("%d-%m-%Y")
    current_time = datetime.now().strftime("%I:%M %p")


    old = attendance_collection.find_one(
        {
            "name": name,
            "date": today
        }
    )


    if old:
        return False



    attendance_collection.insert_one(
        {
            "name": name,
            "date": today,
            "time": current_time
        }
    )


    return True



# ==========================
# Get Attendance
# ==========================

def get_attendance():

    return list(
        attendance_collection.find().sort("_id",-1)
    )



# ==========================
# Total Students
# ==========================

def total_students():

    return students_collection.count_documents({})



# ==========================
# Today Attendance
# ==========================

def today_attendance():

    today = datetime.now().strftime("%d-%m-%Y")

    return attendance_collection.count_documents(
        {
            "date": today
        }
    )