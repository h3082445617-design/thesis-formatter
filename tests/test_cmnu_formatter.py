# tests/test_cmnu_formatter.py
"""CMNU 格式化器测试"""

import pytest
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from src.formatters import CmnuFormatter
from src.utils import SectionDetector, StyleApplier


class TestCmnuFormatter:
    """CMNU 格式化器集成测试"""

    @pytest.fixture
    def sample_doc(self):
        """创建样本论文文档"""
        doc = Document()
        # TODO: 构建包含各部分的样本文档
        return doc

    def test_formatter_initialization(self):
        """测试格式化器初始化"""
        formatter = CmnuFormatter()

        assert formatter is not None
        assert hasattr(formatter, 'format_document')
        assert hasattr(formatter, '_detect_parts')
        assert hasattr(formatter, '_format_abstract')
        assert hasattr(formatter, '_format_body')

    def test_format_simple_document(self, tmp_path):
        """测试格式化简单文档"""
        # 创建样本文档
        input_doc = Document()
        input_doc.add_paragraph('摘要')
        input_doc.add_paragraph('这是摘要内容')
        input_doc.add_paragraph('关键词: 关键词1; 关键词2')
        input_doc.add_paragraph('第1章 绪论')
        input_doc.add_paragraph('正文内容')

        # 保存为临时文件
        input_path = tmp_path / "test_input.docx"
        input_doc.save(str(input_path))

        # 格式化
        formatter = CmnuFormatter()
        output_path = formatter.format_document(str(input_path))

        # 验证输出文件存在
        assert Path(output_path).exists()

        # 验证输出文档可以打开
        output_doc = Document(output_path)
        assert len(output_doc.paragraphs) > 0


class TestSectionDetector:
    """部分检测器测试"""

    def test_match_keywords_abstract(self):
        """测试摘要关键词匹配"""
        doc = Document()
        doc.add_paragraph('摘要')
        doc.add_paragraph('这是摘要内容')

        detector = SectionDetector(doc)
        idx = detector._match_keywords('abstract')

        assert idx == 0, "应该匹配第一段落的'摘要'"

    def test_match_keywords_references(self):
        """测试参考文献关键词匹配"""
        doc = Document()
        doc.add_paragraph('正文内容')
        doc.add_paragraph('参考文献')
        doc.add_paragraph('[1] 作者. 标题')

        detector = SectionDetector(doc)
        idx = detector._match_keywords('references')

        assert idx == 1, "应该匹配第二段落的'参考文献'"

    def test_match_keywords_not_found(self):
        """测试未找到关键词"""
        doc = Document()
        doc.add_paragraph('这是一个文档')
        doc.add_paragraph('没有任何特殊关键词')

        detector = SectionDetector(doc)
        idx = detector._match_keywords('abstract')

        assert idx is None, "未找到时应返回 None"

    def test_detect_parts_simple(self):
        """测试简单场景：检测摘要、目录、正文、参考文献"""
        doc = Document()
        doc.add_paragraph('摘要')
        doc.add_paragraph('摘要正文第一段')
        doc.add_paragraph('摘要正文第二段')
        doc.add_paragraph('关键词: 生物多样性')
        doc.add_paragraph('目录')
        doc.add_paragraph('第1章 ... 1')
        doc.add_paragraph('第1章 正文开始')
        doc.add_paragraph('第1章 正文内容')
        doc.add_paragraph('参考文献')
        doc.add_paragraph('[1] 作者. 标题. 期刊')
        doc.add_paragraph('致谢')
        doc.add_paragraph('感谢导师的指导')

        detector = SectionDetector(doc)
        parts = detector.detect_parts()

        assert parts['abstract'] == (0, 3), "摘要应该是 0-3"
        assert parts['toc'] == (4, 5), "目录应该是 4-5"
        assert parts['body'] == (6, 8), "正文应该是 6-8"
        assert parts['references'] == (9, 10), "参考文献应该是 9-10"
        assert parts['acknowledgment'] == (11, 12), "致谢应该是 11-12"

    def test_detect_parts_missing_toc(self):
        """测试目录缺失的情况"""
        doc = Document()
        doc.add_paragraph('摘要')
        doc.add_paragraph('摘要内容')
        doc.add_paragraph('第1章 标题')  # 直接开始正文，没有目录
        doc.add_paragraph('正文内容')
        doc.add_paragraph('参考文献')

        detector = SectionDetector(doc)
        parts = detector.detect_parts()

        # 应该至少检测到摘要、正文、参考文献
        assert parts['abstract'] is not None
        assert parts['body'] is not None
        assert parts['references'] is not None
        assert parts['toc'] is None  # 目录未检测到

    def test_detect_abstract(self):
        """测试摘要检测"""
        # TODO: 实现
        pass

    def test_detect_references(self):
        """测试参考文献检测"""
        # TODO: 实现
        pass


class TestStyleApplier:
    """样式应用器测试"""

    def test_apply_font_song(self):
        """测试应用宋体"""
        doc = Document()
        para = doc.add_paragraph('测试文本')
        run = para.runs[0]

        applier = StyleApplier()
        applier.apply_font(run, '宋体', Pt(12), bold=False)

        assert run.font.name == '宋体'
        assert run.font.size == Pt(12)
        assert run.bold == False

    def test_apply_font_hei_bold(self):
        """测试应用黑体加粗"""
        doc = Document()
        para = doc.add_paragraph('标题')
        run = para.runs[0]

        applier = StyleApplier()
        applier.apply_font(run, '黑体', Pt(16), bold=True)

        assert run.font.name == '黑体'
        assert run.font.size == Pt(16)
        assert run.bold == True

    def test_apply_paragraph_format_standard(self):
        """测试应用标准段落格式（1.5倍行距、首行缩进）"""
        doc = Document()
        para = doc.add_paragraph('正文内容')

        applier = StyleApplier()
        applier.apply_paragraph_format(
            para,
            alignment=0,  # 左对齐
            line_spacing=1.5,
            space_before=Pt(0),
            space_after=Pt(6),
            indent_first_line=Cm(0.5)
        )

        pf = para.paragraph_format
        assert pf.line_spacing == 1.5
        assert pf.space_before == Pt(0)
        assert pf.space_after == Pt(6)
        assert pf.first_line_indent == Cm(0.5)

    def test_apply_hanging_indent(self):
        """测试参考文献悬挂缩进"""
        doc = Document()
        para = doc.add_paragraph('[1] 作者. 标题. 期刊')

        applier = StyleApplier()
        applier.apply_hanging_indent(para, hanging_indent=Cm(0.5))

        pf = para.paragraph_format
        # 悬挂缩进: first_line_indent = -hanging_indent
        assert pf.first_line_indent == Cm(-0.5)
        assert pf.left_indent == Cm(0.5)
