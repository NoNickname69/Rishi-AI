from abc import ABC, abstractmethod

from PIL.Image import Image



class BaseOCR(ABC):
    """
    Abstract base class for OCR engines.

    OCR implementations extract machine-readable text
    from images while hiding the underlying OCR library
    from the rest of the application.
    """

    @abstractmethod
    def extract_text(
        self,
        image: Image,
    ) -> str:
        
        """
        Extract text from a single image.

        Parameters:
        image: Input image to process.

        Returns:
        The extracted text.
        """

        # Concurrent OCR engines must implement this method.
        
        raise NotImplementedError