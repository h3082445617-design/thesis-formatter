"""中央民族大学学位论文格式化器"""

from typing import Dict, Tuple, Optional
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from src.utils import SectionDetector, StyleApplier


class CmnuFormatter:
    """中央民族大学学位论文格式化器"""

    # CMNU 标准参数
    MARGINS = {
        'top': Cm(2.5),
        'bottom': Cm(2.5),
        'left': Cm(2.2),
        'right': Cm(2.2)
    }

    def __init__(self):
        """初始化格式化器"""
        self.style_applier = StyleApplier()
        self.debug = False

    def format_document(self, input_path: str, output_path: Optional[str] = None,
                        debug: bool = False) -> str:
        """
        格式化论文文档

        Args:
            input_path: 输入 .docx 文件路径
            output_path: 输出文件路径（默认：input_formatted.docx）
            debug: 是否打印调试信息

        Returns:
            输出文件路径
        """
        self.debug = debug

        # 打开文档
        doc = Document(input_path)

        # 1. 检测各部分
        detector = SectionDetector(doc)
        parts = detector.detect_parts(debug=self.debug)

        if self.debug:
            print(f"Detected parts: {parts}")

        # 2. 应用边距
        self._apply_margins(doc)

        # 3. 应用各部分格式
        self._format_abstract(doc, parts)
        self._format_toc(doc, parts)
        self._format_body(doc, parts)
        self._format_references(doc, parts)
        self._format_appendix(doc, parts)
        self._format_acknowledgment(doc, parts)

        # 4. 处理页码（最关键，稍后实现）
        # self._setup_page_numbers(doc, parts)

        # 5. 保存输出
        if output_path is None:
            base_path = Path(input_path)
            output_path = str(base_path.parent / f"{base_path.stem}_formatted.docx")

        doc.save(output_path)

        if self.debug:
            print(f"Document saved to: {output_path}")

        return output_path

    def _apply_margins(self, doc: Document):
        """应用页边距"""
        for section in doc.sections:
            section.top_margin = self.MARGINS['top']
            section.bottom_margin = self.MARGINS['bottom']
            section.left_margin = self.MARGINS['left']
            section.right_margin = self.MARGINS['right']

    def _detect_parts(self, doc: Document) -> Dict[str, Optional[Tuple[int, int]]]:
        """检测论文各部分"""
        detector = SectionDetector(doc)
        return detector.detect_parts()

    # TODO: 实现各部分格式化方法
    def _format_abstract(self, doc: Document, parts: Dict):
        """格式化摘要"""
        pass

    def _format_toc(self, doc: Document, parts: Dict):
        """格式化目录"""
        pass

    def _format_body(self, doc: Document, parts: Dict):
        """格式化正文"""
        pass

    def _format_references(self, doc: Document, parts: Dict):
        """格式化参考文献"""
        pass

    def _format_appendix(self, doc: Document, parts: Dict):
        """格式化附录"""
        pass

    def _format_acknowledgment(self, doc: Document, parts: Dict):
        """格式化致谢"""
        pass
