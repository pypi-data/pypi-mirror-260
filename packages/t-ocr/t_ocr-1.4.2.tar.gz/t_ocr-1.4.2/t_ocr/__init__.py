"""Top-level package for T - OCR."""

__author__ = """Thoughtful"""
__email__ = "support@thoughtfulautomation.com"
__version__ = "1.4.2"

from .textract import Textract
from .free_ocr import FreeOCR, PSM

__all__ = [
    "Textract",
    "FreeOCR",
    "PSM",
]
