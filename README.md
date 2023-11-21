# Legal_AI

This project explores langchain and llm based apps. 

The goal is to create an app that takes user input/context data like PDF's and provides it as context to a LLM. 

Langchain is an AI first framework, that enables developers to build context aware reasoning apps by linking LLM's with external data sources for advanced NLP apps.

# Embedding and Vector Databases

### Theory
  
 ![image](https://github.com/izzypt/Legal_AI/assets/73948790/ec397a70-1363-4bc1-a291-cb4ffb5f70d4)

- Starting from the PDF position of the image above:
  - We are going to be taking the PDF's from our user and break them down into chunks of strings
  - Later we going to convert those chuncks into embeddings (embeddings are vector representation of the text/ contains information about the meaning of the text)
  - Those embeddings are stored in a vector store (knowledge base/vector database)

- Starting from the user position of the image above:
  - Once we have our DB we can take questions from the user:
  - He asks some question like "What is a neural network" and we embedd his question into vectors/numerical representation using the same algorithm we used to embedd the PDF'S into chunks of text.
  - With this we can make a semantic search, allowing us to find in the DB the vectors that have similar meaning to our question.
  - This will give us a rank of results that are relevant.
  - Those results we will give them to the LLM which will, in turn, return us an answer.

### Use

### Integration
