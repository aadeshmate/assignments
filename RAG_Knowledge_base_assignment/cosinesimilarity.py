
import numpy as np

def cosine_similarity(vector1,vector2):
    vector1=np.array(vector1)
    vector2=np.array(vector2)

    dot_product = np.dot(vector1,vector2)

    normal_vector1 = np.linalg.norm(vector1)
    normal_vector2 = np.linalg.norm(vector2)

    return dot_product/(normal_vector1*normal_vector2)
