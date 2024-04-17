from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

class VectorStore:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.documents = []
        self.document_vectors = None

    def add_document(self, document):
        self.documents.append(document)
        self.document_vectors = self.vectorizer.fit_transform(self.documents)

    def save_vectors(self):
        with open("vectors.pkl", "wb") as f:
            pickle.dump(self.document_vectors, f)
