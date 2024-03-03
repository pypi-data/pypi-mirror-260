import os
import json
import requests
import pdfplumber
from typing import List
import tensorflow as tf
from pinecone import Pinecone

class PineconeUploader:
    def __init__(self, api_key, host):
        self.api_key = api_key
        self.host = host
        self.pinecone = Pinecone(api_key=self.api_key)
        self.index = self.pinecone.Index(host=self.host)

def read_pdf(directory):
    texts = []
    if not os.path.exists(directory):
        os.makedirs(directory)
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            with pdfplumber.open(os.path.join(directory, filename)) as pdf:
                text = "".join(page.extract_text() for page in pdf.pages)
                texts.append({"filename": filename, "content": text})
    return texts

def vectorize_text(texts: List[str]) -> List[float]:
    vectorizer = tf.keras.layers.TextVectorization()
    vectorizer.adapt(texts)
    vectors = vectorizer(texts)
    dense_layer = tf.keras.layers.Dense(1536, activation='relu')  
    flattened_vectors = dense_layer(vectors).numpy().flatten()
    return [float(value) for value in flattened_vectors]

def upsert_files(texts, host, api_key):
    for text_info in texts:
        file_name = text_info['filename']
        content = text_info.get('content')
        if not content:
            raise ValueError(f"No content found for file: {file_name}")
        print(f"Processing file: {file_name}")
        vectorized_chunks = []
        chunks = [content[i:i+1500] for i in range(0, len(content), 1500)]
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}")
            vectorized_text = vectorize_text([chunk])
            if not all(-3.402823669209385e+38 <= value <= 3.402823669209385e+38 for value in vectorized_text):
                raise ValueError(f"Error: Vectorization failed for chunk {i+1} of file {file_name}. Values out of range")
            pinecone_vector_obj = {
                'id': f"{file_name}_chunk_{i+1}",
                'values': vectorized_text,
                'metadata': {
                    'source': f"{file_name}_chunk_{i+1}",
                    'text': chunk 
                }
            }
            vectorized_chunks.append(pinecone_vector_obj)
        formatted_vectors = {"vectors": vectorized_chunks}
        payload = json.dumps(formatted_vectors)
        req_url = f"https://{host}/vectors/upsert"
        headers = {
            "Api-Key": api_key,
            "Accept": "application/json",
            "Content-Type": "application/json" 
        }
        response = requests.post(req_url, data=payload, headers=headers)
        print(response.status_code, response.text)
    
    return "Uploaded vectors to Pinecone"


