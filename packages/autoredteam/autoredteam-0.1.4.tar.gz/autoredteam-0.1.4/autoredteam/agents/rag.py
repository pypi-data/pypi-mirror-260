import os
from langchain.prompts import PromptTemplate
from langchain_community.llms.octoai_endpoint import OctoAIEndpoint
from langchain_community.embeddings import OctoAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

from milvus import default_server
from langchain_community.vectorstores import Milvus


class RagAgent():
    
    def __init__(
        self, 
        llm, 
        path,
        embeddings=OctoAIEmbeddings(endpoint_url="https://text.octoai.run/v1/embeddings"),
        generations=1
    ):
        # initialize the LLM and embeddings
        print("Creating LLM Agent: " + llm)
        self.llm = OctoAIEndpoint(
            endpoint_url="https://text.octoai.run/v1/chat/completions",
            model_kwargs={
                "model": llm,
                "max_tokens": 128,
                "presence_penalty": 0,
                "temperature": 0.01,
                "top_p": 0.9,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. Keep your responses limited to one short paragraph if possible.",
                    },
                ],
            },
            )
        self.embeddings = embeddings
        self.generations = generations
        
        # load and chunk the documents
        print("Loading documents from: " + path)
        self.path = path
        files = os.listdir(self.path)
        file_texts = []
        for file in files:
            with open(f"{self.path}/{file}") as f:
                file_text = f.read()
            text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=512, chunk_overlap=64,
            )
            texts = text_splitter.split_text(file_text)
            for i, chunked_text in enumerate(texts):
                file_texts.append(Document(
                    page_content=chunked_text,
                    metadata={"doc_title": file.split(".")[0], "chunk_num": i}))
                
        # create the vector store
        print("Creating vector db server")
        default_server.start()
        
        print("Creating vector store")
        self.vector_store = Milvus.from_documents(
            file_texts,
            embedding=self.embeddings,
            connection_args={"host": "localhost", "port": default_server.listen_port},
            collection_name="cities"
        )
        self.retriever = self.vector_store.as_retriever()
        
        # set up the chain
        template = """Answer the question based only on the following context:
        {context}


        Question: {question}
        """
        prompt = PromptTemplate.from_template(template)
        from langchain_core.runnables import RunnablePassthrough
        from langchain_core.output_parsers import StrOutputParser
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def generate(self, prompt):
        return [self.chain.invoke(prompt) for _ in range(self.generations)]
