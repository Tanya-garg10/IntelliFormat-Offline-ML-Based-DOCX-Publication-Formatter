"""
Image parser module.
Extracts embedded images, shapes, and their association with captions.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from docx import Document


@dataclass
class ImageInfo:
    index: int
    r_id: str
    content_type: str
    filename: str
    paragraph_index: Optional[int] = None
    associated_caption_index: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "r_id": self.r_id,
            "content_type": self.content_type,
            "filename": self.filename,
            "paragraph_index": self.paragraph_index,
            "associated_caption_index": self.associated_caption_index,
        }


class ImageParser:
    """Parses images from docx document package parts and paragraph elements."""

    @staticmethod
    def extract_images(doc: Document) -> List[ImageInfo]:
        images: List[ImageInfo] = []
        idx = 0

        # Scan document part relationships for image types
        try:
            for rel_id, rel in doc.part.rels.items():
                if "image" in rel.target_ref.lower():
                    img = ImageInfo(
                        index=idx,
                        r_id=rel_id,
                        content_type=getattr(rel, "target_mode", "Internal"),
                        filename=rel.target_ref,
                    )
                    images.append(img)
                    idx += 1
        except Exception:
            pass

        return images
