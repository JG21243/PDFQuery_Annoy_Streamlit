import os
import openai
import pdfplumber
import streamlit as st
from annoy import AnnoyIndex

text_storage = {}

def extract_text_from_pdf(file_obj, pages_per_chunk=4):
    try:
        text_chunks = []
        pdf = pdfplumber.open(file_obj)
        num_pages = len(pdf.pages)
        for i in range(0, num_pages, pages_per_chunk):
            text = []
            for j in range(i, min(i + pages_per_chunk, num_pages)):
                text.append(pdf.pages[j].extract_text())
            text_chunks.append(' '.join(text))
        return text_chunks
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None

def create_openai_embedding(text, max_words=400):
    words = text.split()
    chunks = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    embeddings = []
    for chunk in chunks:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=chunk
        )
        embeddings.append(response["data"][0]["embedding"])
    embedding = [sum(x) / len(x) for x in zip(*embeddings)]
    return embedding

def setup_annoy(dimension=1536):
    index = AnnoyIndex(dimension, 'angular')
    return index

def upsert_to_annoy(index, vector_id, vector_values, text):
    index.add_item(vector_id, vector_values)
    text_storage[vector_id] = text
    print(f"Upserted data to index with vector ID {vector_id}")

def query_annoy(index, question_embedding, top_k=3):
    try:
        print(f"Querying index with question embedding {question_embedding}")
        query_results = index.get_nns_by_vector(question_embedding, top_k, include_distances=True)
        print(f"Query results: {query_results}")
        return query_results
    except Exception as e:
        print(f"Error querying Annoy: {e}")
        return {'results': []}

def generate_answer(context_data, question):
    prompt = f"Context: {', '.join(context_data)}\nQuestion: {question}\nAnswer:"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",  
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.0,
    )
    
    return response.choices[0].message['content'].strip()

def interpret_answer(answer):
    return answer

def process_query_results(query_results):
    results, scores = query_results
    context_data = []
    for i, result in enumerate(results):
        context_data.append(f"{result}: {scores[i]} - {text_storage[result]}")
    return context_data

def main():
    st.title('PDF Query Interface')
    file = st.file_uploader("Upload a PDF Document")
    user_question = st.text_input("Enter Your Question")

    if file and user_question:
        text_chunks = extract_text_from_pdf(file)
        
        if text_chunks is None:
            st.error("An error occurred while reading the PDF file. Please try again with a different file.")
            return

        openai.api_key = st.secrets["openai"]["api_key"]
        index = setup_annoy()

        for i, text in enumerate(text_chunks):
            if text:
                response = create_openai_embedding(text)
                print(f"OpenAI Response for chunk {i}: {response}")

                vector_id = i
                vector_values = response
                upsert_to_annoy(index, vector_id, vector_values, text)

        try:
            index.build(10)  # 10 trees
        except Exception as e:
            print(f"Error building Annoy index: {e}")
            return

        question = user_question
        question_embedding = create_openai_embedding(question)
        query_results = query_annoy(index, question_embedding)
        context_data = process_query_results(query_results)
        answer = generate_answer(context_data, question)
        interpreted_answer = interpret_answer(answer)

        st.text_area("Answer", interpreted_answer)

if __name__ == "__main__":
    main()
