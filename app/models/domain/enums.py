"""
Domain enumerations for Rishi AI.

These enums define the controlled vocabulary used throughout the application. 
They should remain stable and be imported instead of
hardcoding string literals.
"""

from enum import Enum

# Corpus Classification

class Category(str, Enum):
    """Top level classification of a document."""

    SCRIPTURE = "Scripture"
    COMMENTARY = "Commentary"
    DICTIONARY = "Dictionary"
    PHILOSOPHY = "Philosophy"
    HISTORY = "History"
    RITUAL = "Ritual"
    ACADEMIC = "Academic"
    MISCELLANEOUS = "Miscellaneous"

class DocumentKind(str, Enum):
    """More specific classification within a category."""

    PRIMARY_SCRIPTURE = "Primary Scripture"
    SCRIPTURE_WITH_COMMENTARY = "Scripture with Commentary"

    COMMENTARY = "Commentary"
    SUB_COMMENTARY = "Sub Commentary"

    TRANSLATION = "Translation"

    DICTIONARY = "Dictionary"
    LEXICON = "Lexicon"

    RESEARCH_PAPER = "Research Paper"
    BOOK = "Book"
    ARTICLE = "Article"
    ESSAY = "Essay"
    THESIS = "Thesis"

# Language

class Language(str, Enum):
    """Languages supported by the Corpus."""

    SANSKRIT = "Sanskrit"
    ENGLISH = "English"
    HINDI = "Hindi"

# Source Format

class DocumentFormat(str, Enum):
    """Physical format of the source document."""

    PDF = "pdf"
    EPUB = "epub"
    HTML = "html"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "md"

# Processing Pipeline

class ProcessingStatus(str, Enum):
    """Current stage of the document in the ingestion pipeline."""

    RAW = "raw"
    EXTRACTED = "extracted"
    CLEANED = "cleaned"
    CHUNKED = "chunked"
    EMBEDDED = "embedded"
    INDEXED = "indexed"

# Quality Level

class QualityLevel(str, Enum):
    """Overall quality assesment of a document."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERIFIED = "verified"