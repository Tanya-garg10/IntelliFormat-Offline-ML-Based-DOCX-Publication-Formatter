"""
IntelliFormat Formatter Package
Enforces publication-grade typography, margins, spacing, and structural styles via python-docx.
Strictly adheres to the text preservation mandate (zero text modifications).
"""

from .document_formatter import DocumentFormatter
from .margins import MarginManager
from .styles import PublicationStyles
from .headings import HeadingManager

__all__ = ["DocumentFormatter", "MarginManager", "PublicationStyles", "HeadingManager"]
