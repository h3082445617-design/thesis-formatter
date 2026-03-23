"""Core thesis document formatting engine."""

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING
from src.exceptions import FormattingError, FileCorruptedError, InvalidFileFormatError
import os
import time


class DocumentFormatter:
    """Core engine for formatting thesis documents according to GB/T 7714 standard."""

    TIMEOUT_SECONDS = 30

    def __init__(self):
        """Initialize formatter with GB/T 7714 standard settings."""
        self.body_font_name = '宋体'
        self.body_font_size = Pt(12)
        self.body_line_spacing = 1.5
        self.heading1_font_size = Pt(18)
        self.heading2_font_size = Pt(14)
        self.heading3_font_size = Pt(12)
        self.paragraph_space_before = Pt(0)
        self.paragraph_space_after = Pt(6)
        self.margin_left = Cm(2.5)
        self.margin_right = Cm(2)
        self.margin_top = Cm(2)
        self.margin_bottom = Cm(2)

    def format_document(self, input_path, keep_original=True):
        """
        Format a Word document according to GB/T 7714 standard.

        Args:
            input_path: Path to input .docx file
            keep_original: If True, save original as backup

        Returns:
            Path to formatted document

        Raises:
            InvalidFileFormatError: If file is not .docx
            FileCorruptedError: If file cannot be opened
            FormattingError: If formatting fails
        """
        start_time = time.time()

        # Validate file format
        if not input_path.lower().endswith('.docx'):
            raise InvalidFileFormatError(f"文件格式必须是.docx，你上传的是 {os.path.splitext(input_path)[1]} 文件")

        # Check file exists
        if not os.path.exists(input_path):
            raise FileCorruptedError("文件无法访问或不存在")

        try:
            # Load document
            doc = Document(input_path)
        except Exception as e:
            raise FileCorruptedError(f"文件无效或损坏：{str(e)}")

        try:
            # Apply formatting
            self._unify_fonts_and_spacing(doc)

            # Generate output path
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_formatted{ext}"

            # Save
            doc.save(output_path)

            elapsed = time.time() - start_time
            if elapsed > self.TIMEOUT_SECONDS:
                raise FormattingError(f"处理超时（{elapsed:.1f}秒），你的文件可能过于复杂")

            return output_path

        except FormattingError:
            raise
        except Exception as e:
            raise FormattingError(f"处理失败：{str(e)}")

    def _unify_fonts_and_spacing(self, doc):
        """Apply uniform font, size, and line spacing to all paragraphs."""
        for paragraph in doc.paragraphs:
            # Set line spacing
            paragraph.paragraph_format.line_spacing = self.body_line_spacing

            # Set paragraph spacing
            paragraph.paragraph_format.space_before = self.paragraph_space_before
            paragraph.paragraph_format.space_after = self.paragraph_space_after

            # Set font for all runs
            for run in paragraph.runs:
                run.font.name = self.body_font_name
                run.font.size = self.body_font_size

        # Also apply to table cells
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        paragraph.paragraph_format.line_spacing = self.body_line_spacing
                        for run in paragraph.runs:
                            run.font.name = self.body_font_name
                            run.font.size = self.body_font_size
