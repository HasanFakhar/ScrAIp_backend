
from fastapi import HTTPException
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
import time

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
pinecone = Pinecone(api_key=PINECONE_API_KEY)

async def create_index(index_name: str):
    for current_index in pinecone.list_indexes():
        if index_name == current_index['name']:
            raise HTTPException(status_code=400, detail="index with that name already exists")
    pinecone.create_index(
        name=index_name,
        dimension=1024,  # Replace with your model dimensions
        metric="cosine",  # Replace with your model metric
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

async def create_embeddings(index_name: str, data: list):

    embeddings = pinecone.inference.embed(
        model="multilingual-e5-large",
        inputs=[d['text'] for d in data],
        parameters={"input_type": "passage", "truncate": "END"}
    )

    while not pinecone.describe_index(index_name).status['ready']:
        time.sleep(1)


    index = pinecone.Index(index_name)

    vectors = []

    for d, e in zip(data, embeddings):
        vectors.append({
            "id": d['id'],
            "values": e['values'],
            "metadata": {'text': d['text']}
        })

    index.upsert(
        vectors=vectors,
        namespace="ns1"
    )

    while not index.describe_index_stats()['total_vector_count'] == len(data):
        time.sleep(1)
    return index.describe_index_stats()

async def get_results(index_name: str, query: str):

    embedding = pinecone.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )

    index = pinecone.Index(index_name)

    results = index.query(
        namespace="ns1",
        vector=embedding[0].values,
        top_k=20,
        include_values=False,
        include_metadata=True
    )

    print(results)
    return results.to_dict()
