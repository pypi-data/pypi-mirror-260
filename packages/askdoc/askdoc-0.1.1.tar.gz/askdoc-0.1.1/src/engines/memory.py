import numpy as np
from loguru import logger
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from ..utils import log_time

class UserMemory:
    def __init__(self) -> None:
        self.encoder = SentenceTransformer('pritamdeka/S-PubMedBert-MS-MARCO')
        # Counter of number of documents that are embedded for the user
        self.counter = 0
        # Hash map of all the history embeddings of the user
        # Keys will be integers, values will be a Dict {payload: [..], metadata: [..]}
        self.embedding_dict = {}
        # Embeddings are stored in a numpy array. New embeddings are concatenated
        self.embeddings = np.array([])

    @log_time(name='embedder')
    def add_memory(self, documents: List[str], metadata: List[str]):
        """
        Embed a list of documents using the provided embedding model.
        """

        assert len(documents) == len(metadata), 'Metadata needs to provided for each document'

        logger.info(f'Length of documents to embed: {len(documents)}')
        logger.debug(f'Documents: {documents}')

        embeddings = np.array([self.encoder.encode(doc) for doc in documents])

        if self.embeddings.any():
            self.embeddings = np.concatenate((self.embeddings, embeddings), axis=0)

        else:
            self.embeddings = embeddings

        for payload, md in zip(documents, metadata):
            self.embedding_dict.update({
                self.counter:{
                    'payload': payload,
                    'metadata': md
                }
            })
            self.counter += 1

    @log_time(name='search')
    def search(self, query, top_k=5) -> List[Dict]:
        """
        Search for the most similar documents to a query embedding.
        
        Search is performed in a numpy array
        """
        # Exit early if the memory does not have anything
        if not self.embeddings.any():
            return None

        query_embedding = self.encoder.encode(query)

        similarities = cosine_similarity(query_embedding.reshape(1, -1), self.embeddings)
        top_k_indices = np.argsort(similarities[0])[::-1][:top_k]

        logger.info(f'Top {top_k} indices: {top_k_indices}')

        return [self.embedding_dict.get(i) for i in top_k_indices]


if __name__ == '__main__':
    import argparse
    from .reporting import ReportParser

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', type=str, help='Filepath of the report')
    parser.add_argument('-q', type=str, help='Query from the report')

    args = parser.parse_args()

    parser = ReportParser()
    parsed_report = parser.parse(filename=args.f)
    cleaned_report = parser.clean_ocr(parsed_report)

    history = UserMemory()

    history.add_memory(
        documents=list(cleaned_report.values()),
        metadata=[f'Medical document, page: {k}' for k in parsed_report.keys()]
    )

    result = history.search(query=args.q)

    print(result)