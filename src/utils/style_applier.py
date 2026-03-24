# src/utils/style_applier.py
"""样式应用工具集"""

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from typing import Optional


class StyleApplier:
    """样式应用器"""

    def __init__(self):
        """初始化 CMNU 标准参数"""
        # 字体
        self.font_song = '宋体'
        self.font_hei = '黑体'
        self.font_tnr = 'Times New Roman'

        # 字号
        self.size_3 = Pt(16)        # 三号
        self.size_4 = Pt(14)        # 四号
        self.size_xiaosi = Pt(12)   # 小四号
        self.size_5 = Pt(10.5)      # 五号

        # 行距
        self.line_spacing_1 = 1.0
        self.line_spacing_1_5 = 1.5
        self.line_spacing_fixed_20pt = 20

    def apply_font(self, run, font_name: str, size: Optional[Pt] = None, bold: bool = False):
        """应用字体样式"""
        run.font.name = font_name
        if size:
            run.font.size = size
        run.bold = bold

    def apply_paragraph_format(self, paragraph, alignment: int = 0,
                               line_spacing: float = 1.5,
                               space_before: Pt = None,
                               space_after: Pt = None,
                               indent_first_line: Cm = None):
        """应用段落格式"""
        pf = paragraph.paragraph_format
        pf.alignment = alignment
        pf.line_spacing = line_spacing

        if space_before:
            pf.space_before = space_before
        if space_after:
            pf.space_after = space_after
        if indent_first_line:
            pf.first_line_indent = indent_first_line

    def apply_hanging_indent(self, paragraph, hanging_indent: Cm = Cm(0.5)):
        """应用悬挂缩进（用于参考文献）"""
        pf = paragraph.paragraph_format
        pf.first_line_indent = -hanging_indent  # 负值表示悬挂
        pf.left_indent = hanging_indent
