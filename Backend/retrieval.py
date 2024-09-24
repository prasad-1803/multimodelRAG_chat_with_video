# Create a retriever
vectorstore = MultimodalLanceDB(uri=LANCEDB_HOST_FILE, embedding=embedder, table_name=TBL_NAME)
retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={"k": 1})

# Query the vector store
query1 = "a toddler and an adult"
results = retriever.invoke(query1)

# Display the retrieved results
display_retrieved_results(results)
