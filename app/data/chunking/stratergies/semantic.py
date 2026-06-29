import numpy as np

from nltk.tokenize import sent_tokenize
from sentence_transformers import util

from app.data.chunking.base import BaseChunker
from app.data.embeddings.base import BaseEmbedder
from app.data.chunking.base import Chunk

class SemanticChunker(BaseChunker):

    """
    Creates chunks based on the semantic meaning.
    """

    def __init__(
    self,
    embedder: BaseEmbedder,
    similarity_threshold: float = 0.85,
    max_chunk_size: int = 1000,
    ):
        """
        Initialize the semantic chunker.

        Parameters
        ----------
        embedder:
            Embedding model used to represent sentences.

        similarity_threshold:
            Minimum cosine similarity required for two
            consecutive sentences to belong to the same chunk.

        max_chunk_size:
            Maximum number of characters permitted in a chunk.
        """

        self.embedder = embedder
        self.similarity_threshold = similarity_threshold
        self.max_chunk_size = max_chunk_size


    def _split_sentences(
            self,
            text: str,
    ) -> list[str]:
        
        """
        Split a document into individual sentences.

        Returns
        -------
        list[str]
            Sentences in their original order.
        """

        return sent_tokenize(
            text=text
            )
    
    def _embed_sentences(
            self,
            sentences: list[str],
    ) -> np.ndarray:
        
        """
        Generate embeddings for a sequence of sentences.
        """

        return self.embedder.embed(sentences)

    
    def _compute_similarities(
            self,
            embeddings: np.ndarray,
    ) -> list[float]:
        
        """
        Compute cosine similarity between consecutive
        sentence embeddings.

        Returns
        -------
        list[float]
            Cosine similarity scores for each pair of
            adjacent sentences.
        """

        cos_sims = []

        for i in range(len(embeddings) - 1):

            similarity = util.cos_sim(
                embeddings[i], 
                embeddings[i + 1]
                ).item()

            cos_sims.append(similarity)
        
        return cos_sims
    

    def _find_boundaries(
            self,
            similarities: list[float],
    ) -> list[bool]:
        """
        Determine semantic chunk boundaries based on
        adjacent sentence similarities.

        Returns
        -------
        list[bool]
            A boolean list where True indicates that a new
            chunk should begin after the corresponding
            similarity score.
        """

        boundaries = []

        for similarity in similarities:

            if similarity > self.similarity_threshold:

                boundaries.append(False)

            else:
                
                boundaries.append(True)

        return boundaries
    

    def _build_chunks(
            self,
            sentences: list[str],
            boundaries: list[bool],
            document_id: str,
    ) -> list[Chunk]:
        """
        Build Chunk objects from sentences and semantic boundaries.

        Parameters
        ----------
        sentences:
            List of document sentences.

        boundaries:
            Boolean list where True indicates that a new chunk
            should begin after the current sentence.

        document_id:
            Identifier of the source document.

        Returns
        -------
        list[Chunk]
            Semantic chunks for the document.
        """
        
        
        # Stores the final chunk texts.
        text_chunks = []

        # Sentences currently being accumulated into one chunk.
        current_chunk = []

        for i in range(len(boundaries)):

            # Always add the current sentence.
            current_chunk.append(sentences[i])

            if boundaries[i]:

                text_chunks.append(
                " ".join(current_chunk)
                )

                current_chunk = []
        
        # Add the final sentence (it has no boundary after it).
        current_chunk.append(sentences[-1])

        if current_chunk:

            text_chunks.append(
                " ".join(current_chunk)
            )

        chunks = []

        # Convert chunk texts into Chunk models.
        for chunk_index, chunk_text in enumerate(text_chunks):

            chunks.append(

                Chunk(
                    chunk_id=f"{document_id}_{chunk_index}",
                    document_id=document_id,
                    text=chunk_text,
                    chunk_index=chunk_index,
                    character_count=len(chunk_text),
                    word_count=len(chunk_text.split()),
                )
            )

        return chunks
    

    def chunk(
            self,
            text: str,
            document_id: str,
    ) -> list[Chunk]:
        
        """
        Split a document into semantic chunks.

        Parameters
        ----------
        text:
            Document text to chunk.

        document_id:
            Identifier of the source document.

        Returns
        -------
        list[Chunk]
            Semantically coherent chunks.
        """

        sentences = self._split_sentences(
            text=text,
            )
        
        if not sentences:
            return []
        
        embeddings = self._embed_sentences(
            sentences=sentences,
            )
        
        similarities = self._compute_similarities(
            embeddings=embeddings,
        )

        boundaries = self._find_boundaries(
            similarities=similarities,
        )

        chunks = self._build_chunks(
            sentences=sentences,
            boundaries=boundaries,
            document_id=document_id,
        )

        return chunks