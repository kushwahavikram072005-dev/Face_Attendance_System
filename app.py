import streamlit as st
import database
import os
from face_module import find_face
from datetime import datetime


# Database Create
database.create_database()


# Page Setting
st.set_page_config(
    page_title="Face Attendance System",
    page_icon="📸",
    layout="wide"
)


st.title("📸 AI Face Attendance System")

st.sidebar.title("Menu")


menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Register Face",
        "Take Attendance",
        "Attendance Records"
    ]
)


# ==========================
# Dashboard
# ==========================
if menu == "Dashboard":

    st.header("📊 Dashboard")


    col1, col2 = st.columns(2)


    with col1:
        st.metric(
            "Total Students",
            database.total_students()
        )


    with col2:
        st.metric(
            "Today's Attendance",
            database.today_attendance()
        )


    st.success(
        "System Running Successfully ✅"
    )


# ==========================
# Register Face
# ==========================
elif menu == "Register Face":

    st.header("👤 Register New Face")


    name = st.text_input(
        "Enter Student Name"
    )


    image = st.camera_input(
        "Capture Student Face"
    )


    if st.button("Save Face"):


        if name and image:


            os.makedirs(
                "images",
                exist_ok=True
            )


            image_path = f"images/{name}.jpg"


            with open(image_path, "wb") as file:
                file.write(image.getvalue())


            database.register_student(
                name,
                image_path
            )


            st.success(
                "Face Registered Successfully ✅"
            )


        else:

            st.warning(
                "Name aur Image dono required hai"
            )


# ==========================
# Take Attendance
# ==========================
elif menu == "Take Attendance":

    st.header("✅ Take Attendance")


    image = st.camera_input(
        "Capture Face"
    )


    if image:


        os.makedirs(
            "temp",
            exist_ok=True
        )


        test_image = "temp/test.jpg"


        with open(test_image, "wb") as file:
            file.write(image.getvalue())


        st.image(
            test_image
        )


        st.write(
            "Face Checking..."
        )


        person, score = find_face(test_image)
        st.write(f"Match Score: {score:.3f}")


        if person:


            result = database.mark_attendance(
                person
            )


            if result:

                st.success(
                    f"Attendance Marked: {person} ✅"
                )

            else:

                st.warning(
                    f"{person} ki attendance pehle hi lag chuki hai ⚠️"
                )


        else:

            st.error(
                "Face Not Recognized ❌"
            )


# ==========================
# Attendance Records
# ==========================
elif menu == "Attendance Records":


    st.header("📋 Attendance Records")


    records = database.get_attendance()


    if records:


        st.table(records)


    else:


        st.warning(
            "No Attendance Found"
        )