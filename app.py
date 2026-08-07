import streamlit as st
import database
import os

from face_module import (
    get_embedding,
    find_face
)



# Database

database.create_database()



# Page

st.set_page_config(
    page_title="Face Attendance System",
    page_icon="📸",
    layout="wide"
)


st.title("📸 AI Face Attendance System")



# Menu

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


    col1,col2 = st.columns(2)


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


    st.header("👤 Register Student (5 Photos)")


    name = st.text_input(
        "Enter Student Name"
    )


    st.write(
        "Student ke 5 photos capture karo"
    )


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



    if st.button("Save Student"):


        images = [
            img1,
            img2,
            img3,
            img4,
            img5
        ]


        if name and all(images):


            os.makedirs(
                "images",
                exist_ok=True
            )


            image_paths = []
            embeddings = []



            for i,img in enumerate(images):


                path = f"images/{name}_{i+1}.jpg"


                with open(path,"wb") as file:

                    file.write(
                        img.getvalue()
                    )


                embedding = get_embedding(
                    path
                )


                if embedding is None:

                    st.error(
                        f"Photo {i+1} me face detect nahi hua"
                    )

                    st.stop()



                image_paths.append(path)

                embeddings.append(
                    embedding
                )



            database.register_student(

                name,

                image_paths,

                embeddings

            )


            st.success(
                "5 Photos ke sath Face Registered ✅"
            )



        else:


            st.warning(
                "Name aur 5 Photos required hain"
            )





# ==========================
# Attendance
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



        with open(test_image,"wb") as file:

            file.write(
                image.getvalue()
            )



        person,score = find_face(
            test_image
        )


        st.write(
            f"Match Score : {score:.3f}"
        )



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
                    "Attendance already marked ⚠️"
                )


        else:


            st.error(
                "Face Not Recognized ❌"
            )





# ==========================
# Records
# ==========================

elif menu == "Attendance Records":


    st.header(
        "📋 Attendance Records"
    )


    data = database.get_attendance()


    if data:

        st.dataframe(
            data
        )

    else:

        st.info(
            "No Records Found"
        )