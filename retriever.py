from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query_vector):
        similarities = cosine_similarity(query_vector, self.vector_store.document_vectors)
        most_similar_index = similarities.argmax()
        return self.vector_store.documents[most_similar_index]
