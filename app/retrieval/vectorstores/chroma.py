import chromadb


class ChromaStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="storage/vectordb"
        )

        self.collection = self.client.get_or_create_collection(
            "rishi_ai"
        )