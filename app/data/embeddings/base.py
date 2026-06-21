from abc import ABC, abstractmethod

import numpy as np


class BaseEmbedder(ABC):

    @abstractmethod
    def embed(
        self,
        texts: list[str],
    ) -> np.ndarray:
        """
        Generate embeddings.
        """
        raise NotImplementedError