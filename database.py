
from datetime import datetime
from dotenv import load_dotenv
import os

from pymongo import MongoClient
import gridfs
from bson import ObjectId


# ==========================
# Load Environment
# ==========================

load_dotenv()


# ==========================
# MongoDB Connection
# ==========================

client = MongoClient(
    os.getenv("MONGO_URI")
)

db = client["face_attendance"]


# ==========================
# Collections
# ==========================

students_collection = db["students"]

attendance_collection = db["attendance"]


# ==========================
# GridFS
# ==========================

fs = gridfs.GridFS(db)


# ==========================
# Database Connect
# ==========================

def create_database():

    try:

        client.admin.command("ping")

        print(
            "MongoDB Connected Successfully"
        )

    except Exception as e:

        print(
            "MongoDB Connection Error:",
            e
        )


# ==========================
# Register Student
# ==========================

def register_student(
    name,
    image_paths,
    embeddings,
    image_data
):

    # Check existing student
    old_student = students_collection.find_one(
        {"name": name}
    )


    # ==========================
    # Delete Old MongoDB Photos
    # ==========================

    if old_student:

        old_file_ids = old_student.get(
            "photo_file_ids",
            []
        )

        for file_id in old_file_ids:

            try:

                fs.delete(
                    ObjectId(file_id)
                )

            except Exception:

                pass


    # ==========================
    # Upload New Photos to GridFS
    # ==========================

    new_file_ids = []


    for i, data in enumerate(image_data):

        file_id = fs.put(

            data,

            filename=f"{name}_{i + 1}.jpg",

            contentType="image/jpeg",

            student_name=name

        )

        new_file_ids.append(
            str(file_id)
        )


    # ==========================
    # Save Student Information
    # ==========================

    students_collection.update_one(

        {"name": name},

        {
            "$set": {

                "name": name,

                # Local photo paths
                "images": image_paths,

                # MongoDB GridFS photo IDs
                "photo_file_ids": new_file_ids,

                # Face embeddings
                "embeddings": [

                    e.tolist()

                    for e in embeddings

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
# Get Photo From MongoDB
# ==========================

def get_photo(file_id):

    try:

        file = fs.get(
            ObjectId(file_id)
        )

        return file.read()

    except Exception:

        return None


# ==========================
# Delete Student
# ==========================

def delete_student(name):

    student = students_collection.find_one(

        {
            "name": name
        }

    )


    if not student:

        return False


    # ==========================
    # Delete MongoDB GridFS Photos
    # ==========================

    file_ids = student.get(
        "photo_file_ids",
        []
    )


    for file_id in file_ids:

        try:

            fs.delete(
                ObjectId(file_id)
            )

        except Exception:

            pass


    # ==========================
    # Delete Student Record
    # ==========================

    students_collection.delete_one(

        {
            "name": name
        }

    )


    return True


# ==========================
# Attendance
# ==========================

def mark_attendance(name):

    today = datetime.now().strftime(
        "%d-%m-%Y"
    )


    current_time = datetime.now().strftime(
        "%I:%M %p"
    )


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

        attendance_collection

        .find()

        .sort(
            "_id",
            -1
        )

    )


# ==========================
# Total Students
# ==========================

def total_students():

    return students_collection.count_documents(
        {}
    )


# ==========================
# Today's Attendance
# ==========================

def today_attendance():

    today = datetime.now().strftime(
        "%d-%m-%Y"
    )


    return attendance_collection.count_documents(

        {
            "date": today
        }

    )
