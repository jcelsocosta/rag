import spacy
from src.domain.usecase.transformer.data_ingestion import AbstractDataIngestionTransformer
from typing import List

nlp = spacy.load("pt_core_news_sm")

class DataIngestionTransformer(AbstractDataIngestionTransformer):
    def generate_chunks(self, full_text: str, max_words = 80) -> List[str]:
        documents = nlp(full_text)

        sentences = [sent.text.strip() for sent in documents.sents]
        
        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            words = sentence.split()
            if current_length + len(words) <= max_words:
                current_chunk.append(sentence)
                current_length += len(words)
            else:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = len(words)

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks