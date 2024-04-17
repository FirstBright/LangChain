import unittest
from crawler import Crawler
from sql import SQLModule
from vector_store import VectorStore
from retriever import Retriever

class TestCrawler(unittest.TestCase):
    def test_crawl(self):
        vector_store = VectorStore()
        crawler = Crawler(vector_store)
        documents = crawler.crawl('http://example.com/law')  # 테스트 URL
        self.assertTrue(len(documents) > 0, "No documents were crawled.")
        self.assertIn("Expected Content", documents[0], "Crawled content does not include expected text.")



class TestSQLModule(unittest.TestCase):
    def test_database_connection(self):
        sql_module = SQLModule(db_path=':memory:')  # Use in-memory database for testing
        result = sql_module.execute_query("SELECT 1")
        self.assertEqual(result[0][0], 1)

class TestVectorStore(unittest.TestCase):
    def test_add_document(self):
        vector_store = VectorStore()
        initial_count = len(vector_store.documents)
        vector_store.add_document("Test document")
        self.assertEqual(len(vector_store.documents), initial_count + 1)

class TestRetriever(unittest.TestCase):
    def test_retrieve(self):
        vector_store = VectorStore()
        vector_store.add_document("Test document")
        vector_store.add_document("Another document")
        retriever = Retriever(vector_store)
        query_vector = vector_store.vectorizer.transform(["Test document"])
        result = retriever.retrieve(query_vector)
        self.assertIn("Test document", result)

if __name__ == '__main__':
    unittest.main()
