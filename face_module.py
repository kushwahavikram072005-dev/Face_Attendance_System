import os
import cv2
import numpy as np
from insightface.app import FaceAnalysis

# Load InsightFace Model
app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=-1)


# -------------------------------------
# Face Embedding
# -------------------------------------
def get_embedding(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    faces = app.get(image)

    if len(faces) == 0:
        return None

    return faces[0].embedding


# -------------------------------------
# Cosine Similarity
# -------------------------------------
def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -------------------------------------
# Find Matching Face
# -------------------------------------
def find_face(test_image):

    test_embedding = get_embedding(test_image)

    if test_embedding is None:
        return None

    folder = "images"

    if not os.path.exists(folder):
        return None

    best_score = 0
    best_person = None

    for file in os.listdir(folder):

        if file.lower().endswith((".jpg", ".png", ".jpeg")):

            image_path = os.path.join(folder, file)

            db_embedding = get_embedding(image_path)

            if db_embedding is None:
                continue

            score = cosine_similarity(
                test_embedding,
                db_embedding
            )

            if score > best_score:
                best_score = score
                best_person = file.split(".")[0]
    if best_score > 0.90:
     return best_person, best_score

    return None, best_score