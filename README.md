# Indian Constitution Book AI app

Goal: Query the ebook and return summarization and page numbers where the solution of the query might be found.

Steps Involved:
1. Load the documents
2. Clean the document page_content.
3. Rewrite the page number of each document as it is in the pdf document.
4. Send finalized documents to vector DB
5. Set up LLM
6. Ask user for query.
7. Put query to Pinecone retriever for semantic search.
8. Get the most similar documents
9. Use the page_content of the documents as context and send the page numbers of the documents to the user for reference to the physical book.
10. Finally, the LLM should respond the user with a summarised response along with the page numbers.

