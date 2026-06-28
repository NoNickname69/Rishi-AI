from app.data.ocr.base import BaseOCR

from rapidocr_onnxruntime import RapidOCR

from PIL.Image import Image



class RapidOCRProcessor(BaseOCR):
    """
    OCR implementation using the RapidOCR engine.

    This class wraps RapidOCR behind the BaseOCR
    interface so the OCR backend can be replaced
    without affecting the rest of the application.
    """

    def __init__(self):
        """
        Initialize the RapidOCR engine.
        """

        self.engine = RapidOCR()

    def extract_text(
            self,
            image: Image,
            ) -> str:
        """
        Extract text from an image using RapidOCR.

        Parameters:
        image: Input image to process.

        Returns:
        The extracted text.
        """


        # Run text recognition
        result, _ = self.engine(image) # Intetionally not using confidence score for text results.

        texts: list[str] = []


        # Process results
        if result:

            for line in result:

                text = line[1]

                texts.append(text)
            
            return "\n".join(texts)
        
        else:
            return ""