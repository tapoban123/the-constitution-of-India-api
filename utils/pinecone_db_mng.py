from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter

from utils.constants import PINECONE
from pinecone import Pinecone, CloudProvider, AwsRegion, Metric, IndexEmbed, EmbedModel, ServerlessSpec
from langchain_mistralai import MistralAIEmbeddings


class PineconeManager:
    def __init__(self, index_name: str):
        self.pc = Pinecone(api_key=PINECONE.API_KEY.value)
        self.index_name = index_name
        self._embeddings = MistralAIEmbeddings(
            model="mistral-embed",
        )
        self._vector_store = PineconeVectorStore(index_name=self.index_name, embedding=self._embeddings)

    def create_index(self):
        if not self.pc.has_index(self.index_name):
            self.pc.create_index(
                name=self.index_name,
                metric=Metric.COSINE,
                # The Mistral AI embedding model uses 1024 dimensions.
                dimension=1024,
                spec=ServerlessSpec(
                    cloud=CloudProvider.AWS,
                    region=AwsRegion.US_EAST_1,
                )
            )
            print(f"Created index : {self.index_name}", end="\n" * 2)

        print(f"Index {self.index_name} already exists.", end="\n" * 2)

    def delete_index(self):
        self.pc.delete_index(self.index_name)
        print(f"Deleted index : {self.index_name}", end="\n" * 2)

    def save_docs_to_index(self, docs: list[Document]):
        print(f"Started upload of documents.")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=150,
        )

        docs = splitter.split_documents(docs)

        self._vector_store.from_documents(docs,
                                          index_name=self.index_name,
                                          embedding=self._embeddings,
                                          )
        print(f"Completed upload of all documents.", end="\n" * 3)

    def perform_similarity_search(self, query: str):
        self.pc.s
        similar_docs = self._vector_store.similarity_search(query=query, k=5)
        formatted_content = " ".join(x.page_content for x in similar_docs)
        page_nos = [doc.metadata["page_label"] for doc in similar_docs]

        return formatted_content, page_nos
