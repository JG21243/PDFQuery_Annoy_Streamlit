
# PDF Query Interface with Streamlit and OpenAI

This project is a Streamlit application that allows users to upload a PDF file and ask questions related to the content of the PDF. The application utilizes OpenAI's API for text embeddings and Annoy for similarity search to generate relevant answers.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Function Walkthrough](#function-walkthrough)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites
- Python 3.11
- Streamlit
- OpenAI
- pdfplumber
- Annoy

## Installation

1. Clone the repository.
    ```bash
    git clone https://github.com/yourusername/yourprojectname.git
    ```
2. Navigate into the project directory.
    ```bash
    cd yourprojectname
    ```
3. Install the required packages.
    ```bash
    pip install -r requirements.txt
    ```
   
## Usage
1. To run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Function Walkthrough

### `extract_text_from_pdf(file_obj, pages_per_chunk=8)`
This function takes in a PDF file object and an optional `pages_per_chunk` parameter to extract text from the PDF in chunks. It returns a list of text chunks.

### `create_openai_embedding(text, max_words=700)`
This function receives a text string and an optional `max_words` parameter to create text embeddings using OpenAI's API. It returns an embedding vector.

### `setup_annoy(dimension=1536)`
This function initializes an Annoy index for similarity search with a specified dimension (default is 1536). It returns the Annoy index object.

### `upsert_to_annoy(index, vector_id, vector_values, text)`
Upserts (inserts or updates) a text vector into the Annoy index. Also stores the original text in a global dictionary `text_storage`.

### `query_annoy(index, question_embedding, top_k=3)`
Queries the Annoy index with an embedding of a question and returns the closest `top_k` matches along with their distances.

### `generate_answer(context_data, question)`
Generates an answer based on the context data and a user's question. It uses OpenAI's ChatCompletion API to generate the answer.

### `interpret_answer(answer)`
Placeholder for any additional processing on the generated answer. Currently, it returns the answer as-is.

### `process_query_results(query_results)`
Processes the results from the Annoy query to create a context for generating an answer. It returns the processed context data.

### `main()`
The main function initializes the Streamlit interface, calls the other functions in sequence, and displays the generated answer.

## Contributing

If you want to contribute to this project, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.




**Understanding Text Chunking and Chunk Embedding**

1. **Text Chunking by Pages**: The `extract_text_from_pdf` function creates text chunks based on `pages_per_chunk` (default is 8 pages per chunk). Each chunk contains the text from those 8 pages.
2. **Embedding Creation**: The `create_openai_embedding` function takes each of these text chunks and may further break them down into smaller pieces based on `max_words` (700 words). It creates embeddings for these smaller pieces.
3. **Averaging Embeddings**: The function then averages the embeddings of these smaller pieces to create a single embedding for the original text chunk (which was based on `pages_per_chunk`).
4. **Annoy Index**: This averaged embedding is what gets stored in the Annoy index. The index associates this embedding with the original text chunk (based on `pages_per_chunk`).
5. **Querying**: When you query the Annoy index, it returns the `top_k` most relevant text chunks based on these averaged embeddings. Because the averaged embedding represents the original text chunk (based on `pages_per_chunk`), the text chunks returned are also based on `pages_per_chunk`.

While the embeddings are initially created based on `max_words` of 700, they are averaged to represent the original text chunk, which is based on `pages_per_chunk`. Therefore, the `top_k` results are aligned with the `pages_per_chunk` parameter.
