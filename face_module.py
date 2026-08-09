
import cv2
import numpy as np
from insightface.app import FaceAnalysis
import database


# ==========================
# Load InsightFace Model
# ==========================

app = FaceAnalysis(
    name="buffalo_l"
)

app.prepare(
    ctx_id=-1
)


# ==========================
# Get Face Embedding
# ==========================

def get_embedding(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return None

    faces = app.get(image)

    # Exactly ONE face must be present
    if len(faces) != 1:
        return None

    return faces[0].embedding


# ==========================
# Cosine Similarity
# ==========================

def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    denominator = (
        np.linalg.norm(a)
        *
        np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return np.dot(a, b) / denominator


# ==========================
# Find Matching Face
# ==========================

def find_face(test_image):

    test_embedding = get_embedding(test_image)

    if test_embedding is None:
        return None, 0.0

    students = database.get_students()

    best_person = None
    best_score = 0.0

    for student in students:

        if "embeddings" not in student:
            continue

        for saved_embedding in student["embeddings"]:

            score = cosine_similarity(
                test_embedding,
                saved_embedding
            )

            if score > best_score:
                best_score = score
                best_person = student["name"]

    # ==========================
    # Match Threshold
    # ==========================

    if best_score > 0.90:
        return best_person, best_score

    return None, best_score
