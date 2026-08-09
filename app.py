
import streamlit as st
import database
import os

from face_module import (
    get_embedding,
    find_face
)


# ==========================
# Database
# ==========================

database.create_database()


# ==========================
# Page
# ==========================

st.set_page_config(
    page_title="Face Attendance System",
    page_icon="📸",
    layout="wide"
)

st.title("📸 AI Face Attendance System")


# ==========================
# Project Folders
# ==========================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

IMAGES_DIR = os.path.join(
    BASE_DIR,
    "images"
)

TEMP_DIR = os.path.join(
    BASE_DIR,
    "temp"
)


os.makedirs(
    IMAGES_DIR,
    exist_ok=True
)

os.makedirs(
    TEMP_DIR,
    exist_ok=True
)


# ==========================
# Menu
# ==========================

menu = st.sidebar.radio(
    "Select Option",
    [
        "Dashboard",
        "Register Face",
        "Take Attendance",
        "Attendance Records"
    ]
)


# ==========================================================
# Dashboard
# ==========================================================

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


# ==========================================================
# Register Face
# ==========================================================

elif menu == "Register Face":

    st.header(
        "👤 Register Student (5 Photos)"
    )


    name = st.text_input(
        "Enter Student Name"
    )


    st.write(
        "Student ke 5 photos capture karo"
    )


    # ==========================
    # Camera
    # ==========================

    img1 = st.camera_input(
        "Photo 1"
    )


    img2 = st.camera_input(
        "Photo 2"
    )


    img3 = st.camera_input(
        "Photo 3"
    )


    img4 = st.camera_input(
        "Photo 4"
    )


    img5 = st.camera_input(
        "Photo 5"
    )


    # ==========================
    # Save Student
    # ==========================

    if st.button(
        "Save Student"
    ):


        images = [

            img1,
            img2,
            img3,
            img4,
            img5

        ]


        # ==========================
        # Check Name + Photos
        # ==========================

        if name and all(images):


            clean_name = name.strip()


            image_paths = []

            embeddings = []

            image_data = []


            # ==========================
            # Process 5 Photos
            # ==========================

            for i, img in enumerate(images):


                # --------------------------
                # Get Photo Bytes
                # --------------------------

                photo_bytes = img.getvalue()


                image_data.append(
                    photo_bytes
                )


                # --------------------------
                # Filename
                # --------------------------

                filename = (

                    f"{clean_name}_{i + 1}.jpg"

                )


                # --------------------------
                # Local Path
                # --------------------------

                path = os.path.join(

                    IMAGES_DIR,

                    filename

                )


                # --------------------------
                # Save Local Photo
                # --------------------------

                with open(

                    path,

                    "wb"

                ) as file:

                    file.write(
                        photo_bytes
                    )


                # --------------------------
                # Verify Photo
                # --------------------------

                if not os.path.exists(path):

                    st.error(

                        f"Photo {i + 1} save nahi hui ❌"

                    )

                    st.stop()


                # --------------------------
                # Generate Embedding
                # --------------------------

                embedding = get_embedding(
                    path
                )


                # --------------------------
                # Face Check
                # --------------------------

                if embedding is None:

                    st.error(

                        f"Photo {i + 1} me face detect nahi hua ❌"

                    )


                    # Remove invalid photo

                    if os.path.exists(path):

                        os.remove(path)


                    st.stop()


                # --------------------------
                # Store Data
                # --------------------------

                image_paths.append(
                    path
                )


                embeddings.append(
                    embedding
                )


            # ==========================
            # Save Everything to MongoDB
            # ==========================

            database.register_student(

                clean_name,

                image_paths,

                embeddings,

                image_data

            )


            # ==========================
            # Success
            # ==========================

            st.success(

                "5 Photos ke sath Face Registered Successfully ✅"

            )


            st.success(

                "Actual Photos MongoDB me bhi save ho gayi hain ☁️📸"

            )


            st.info(

                "Local images folder me bhi photos save hain 💻"

            )


            # ==========================
            # Show Saved Photos
            # ==========================

            st.write(
                "Saved Photos:"
            )


            for path in image_paths:

                st.write(

                    os.path.basename(path)

                )


        else:

            st.warning(

                "Name aur 5 Photos required hain ⚠️"

            )


# ==========================================================
# Take Attendance
# ==========================================================

elif menu == "Take Attendance":

    st.header(
        "✅ Take Attendance"
    )


    image = st.camera_input(
        "Capture Face"
    )


    if image:


        # ==========================
        # Test Image
        # ==========================

        test_image = os.path.join(

            TEMP_DIR,

            "test.jpg"

        )


        # ==========================
        # Save Test Image
        # ==========================

        with open(

            test_image,

            "wb"

        ) as file:

            file.write(

                image.getvalue()

            )


        # ==========================
        # Find Face
        # ==========================

        person, score = find_face(

            test_image

        )


        st.write(

            f"Match Score : {score:.3f}"

        )


        # ==========================
        # Attendance
        # ==========================

        if person:


            result = database.mark_attendance(

                person

            )


            if result:

                st.success(

                    f"Attendance Marked : {person} ✅"

                )

            else:

                st.warning(

                    "Attendance already marked today ⚠️"

                )


        else:

            st.error(

                "Face Not Recognized ❌"

            )


# ==========================================================
# Attendance Records
# ==========================================================

elif menu == "Attendance Records":

    st.header(

        "📋 Attendance Records"

    )


    data = database.get_attendance()


    if data:

        st.dataframe(

            data,

            use_container_width=True

        )

    else:

        st.info(

            "No Records Found"

        )
