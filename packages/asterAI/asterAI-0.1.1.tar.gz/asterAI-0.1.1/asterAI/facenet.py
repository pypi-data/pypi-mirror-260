from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import os
from typing import List
import random
import numpy as np
import faiss
import pickle

def generate_embedding(path: str) -> np.ndarray:

    img = Image.open(path)
    width, height = img.size
    mtcnn = MTCNN(image_size=width, margin=0)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    img_cropped = mtcnn(img)
    img_embedding = resnet(img_cropped.unsqueeze(0))
    return img_embedding.detach().numpy()

   

def generate_random_batch_embedding(folder_path: str, random_sample_size: int) -> np.ndarray:
    files = os.listdir(folder_path)
    image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    image_paths = [os.path.join(folder_path, file) for file in image_files]
    random_images = random.sample(image_paths, random_sample_size)
    return np.vstack([generate_embedding(path) for path in random_images])



def generate_specific_batch_embedding(path_list: List) -> np.ndarray:
    return np.vstack([generate_embedding(path).flatten() for path in path_list])





def faiss_model(query_vector, data, k=5) -> faiss.swigfaiss_avx2.IndexFlatL2:
    query_vector = query_vector.astype('float32') / np.linalg.norm(query_vector)
    data_normalized = data.astype('float32') / np.linalg.norm(data, axis=1, keepdims=True)
    index = faiss.IndexFlatL2(data.shape[1])
    index.add(data_normalized)
    return index

    

def faiss_sum(index,query_vector,k) -> float:
    distances, _ = index.search(query_vector, k)
    return np.sum(distances)/len(distances)


def serialize_faiss_model(path, faiss_model):
    with open(path, 'wb') as file:
        pickle.dump(faiss_model, file)
        
def deserialize_faiss_model(path) -> faiss.swigfaiss_avx2.IndexFlatL2:
    with open(path, 'rb') as file:
        deserialized_model = pickle.load(file)
    return deserialized_model