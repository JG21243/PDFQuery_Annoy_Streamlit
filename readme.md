
You bring up an excellent point. Let's clarify:

Text Chunking by Pages: The extract_text_from_pdf function creates text chunks based on pages_per_chunk (default is 8 pages per chunk). Each chunk contains the text from those 8 pages.

Embedding Creation: The create_openai_embedding function takes each of these text chunks and may further break them down into smaller pieces based on max_words (700 words). It creates embeddings for these smaller pieces.

Averaging Embeddings: The function then averages the embeddings of these smaller pieces to create a single embedding for the original text chunk (which was based on pages_per_chunk).

Annoy Index: This averaged embedding is what gets stored in the Annoy index. The index associates this embedding with the original text chunk (based on pages_per_chunk).

Querying: When you query the Annoy index, it returns the top_k most relevant text chunks based on these averaged embeddings. Because the averaged embedding represents the original text chunk (based on pages_per_chunk), the text chunks returned are also based on pages_per_chunk.

So, while the embeddings are initially created based on max_words of 700, they are averaged to represent the original text chunk, which is based on pages_per_chunk. Therefore, the top_k results are aligned with the pages_per_chunk parameter.
