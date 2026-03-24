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

        Raises:
            ValueError: 如果 input_path 无效
            FileNotFoundError: 如果文件不存在
            IOError: 如果文件操作失败
        """
        self.debug = debug

        # 1. 验证输入路径
        if not input_path or not isinstance(input_path, str):
            raise ValueError(f"input_path must be a non-empty string, got: {input_path}")

        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file does not exist: {input_path}")

        # 2. 打开文档
        try:
            doc = Document(input_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {input_path}")
        except Exception as e:
            raise IOError(f"Failed to open document: {input_path}. Error: {str(e)}")

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

        # 确保输出目录存在
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

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

    # TODO: 实现各部分格式化方法
    def _format_abstract(self, doc: Document, parts: Dict):
        """
        格式化摘要部分

        标题: 三号黑体，居中，单倍行距，段前24磅/段后18磅
        正文: 小四号宋体，1.5倍行距，首行缩进2字符
        关键词标签: 四号黑体
        关键词内容: 小四号宋体
        """
        if parts.get('abstract') is None:
            return

        start, end = parts['abstract']

        for idx in range(start, end + 1):
            if idx >= len(doc.paragraphs):
                break

            para = doc.paragraphs[idx]
            text = para.text.strip()

            # 标题行（包含"摘要"）
            if '摘要' in text and idx == start:
                for run in para.runs:
                    self.style_applier.apply_font(run, '黑体', Pt(16), bold=True)
                pf = para.paragraph_format
                pf.alignment = 1  # 居中
                pf.line_spacing = 1.0
                pf.space_before = Pt(24)
                pf.space_after = Pt(18)

            # 关键词标签行
            elif text.startswith('关键词:') or text.startswith('关键词：'):
                for run in para.runs:
                    if '关键词' in run.text:
                        self.style_applier.apply_font(run, '黑体', Pt(14), bold=True)
                    else:
                        self.style_applier.apply_font(run, '宋体', Pt(12), bold=False)

            # 普通正文
            else:
                for run in para.runs:
                    self.style_applier.apply_font(run, '宋体', Pt(12), bold=False)

                pf = para.paragraph_format
                pf.line_spacing = 1.5
                pf.first_line_indent = Cm(0.5)  # 2字符缩进
                pf.space_before = Pt(0)
                pf.space_after = Pt(6)

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
