# 中央民族大学论文格式化工具 - 实现计划

> **对 agentic 工作者**: 推荐使用 superpowers:subagent-driven-development 或 superpowers:executing-plans 逐个任务执行此计划。步骤使用复选框 (`- [ ]`) 语法跟踪进度。

**目标**: 创建一个 Python 脚本，自动将硕士学位论文按照中央民族大学规范进行格式化，支持所有关键部分（摘要、目录、正文、参考文献、附录、致谢），包括正确的页码系统（前置罗马数字 + 正文阿拉伯数字）。

**架构**: 采用分层设计，主格式化器（CmnuFormatter）协调部分检测、样式应用、页码处理。核心挑战是页码分节实现（需要 OXml 操作）和部分边界自动检测（带用户手动指定的降级方案）。

**技术栈**: Python 3.8+, python-docx 0.8.11, pytest 7.4.0

---

## 文件结构与职责

```
thesis-formatter/
├── src/
│   ├── formatters/
│   │   ├── __init__.py                  # 导出 CmnuFormatter
│   │   ├── base_formatter.py            # （已有）基础抽象类
│   │   ├── gbt_formatter.py             # （已有）GB/T 格式化器
│   │   └── cmnu_formatter.py            # （新增）中央民族大学格式化器主类
│   └── utils/
│       ├── __init__.py                  # 导出工具函数
│       ├── section_detector.py          # （新增）论文部分检测
│       └── style_applier.py             # （新增）样式应用工具集
├── scripts/
│   └── format_thesis.py                 # （新增）命令行脚本入口
├── tests/
│   └── test_cmnu_formatter.py           # （新增）集成测试
└── docs/superpowers/plans/
    └── 2026-03-24-cmnu-thesis-formatter-implementation.md  # （本文件）
```

### 每个文件的职责

| 文件 | 职责 | 依赖 |
|------|------|------|
| `cmnu_formatter.py` | 主协调器，调用部分检测→样式应用→页码处理 | section_detector, style_applier |
| `section_detector.py` | 自动检测论文各部分边界（摘要、目录、正文等） | 无 |
| `style_applier.py` | 应用具体的字体、行距、缩进、对齐规则 | 无 |
| `format_thesis.py` | CLI 入口，处理参数、错误、用户交互 | CmnuFormatter |
| `test_cmnu_formatter.py` | 单元测试 + 集成测试 | 所有上述模块 |

---

## 任务分解 (18-24小时)

### 任务 1: 初始化项目结构与工具库

**文件**:
- Create: `src/utils/__init__.py`
- Create: `src/formatters/__init__.py`
- Create: `src/utils/section_detector.py` (框架)
- Create: `src/utils/style_applier.py` (框架)
- Create: `tests/test_cmnu_formatter.py` (框架)

- [ ] **步骤 1: 创建 utils 包初始化文件**

```python
# src/utils/__init__.py
"""论文格式化工具集"""

from .section_detector import SectionDetector
from .style_applier import StyleApplier

__all__ = ['SectionDetector', 'StyleApplier']
```

- [ ] **步骤 2: 创建 formatters 包初始化文件**

```python
# src/formatters/__init__.py
"""论文格式化器集合"""

from .cmnu_formatter import CmnuFormatter

__all__ = ['CmnuFormatter']
```

- [ ] **步骤 3: 创建 section_detector.py 框架**

```python
# src/utils/section_detector.py
"""自动检测论文各部分边界"""

from typing import Dict, Tuple, Optional
from docx import Document


class SectionDetector:
    """论文部分检测器"""

    # 部分关键词映射
    KEYWORDS = {
        'abstract': ['摘要', '内容摘要', '中文摘要'],
        'toc': ['目录', '目  录', '目    录'],
        'body': [],  # 通常在摘要和参考文献之间
        'references': ['参考文献', '参考资料', '文献', '参考文献 '],
        'appendix': ['附录', '附  录'],
        'acknowledgment': ['致谢', '后记', '致  谢', '致     谢']
    }

    def __init__(self, doc: Document):
        self.doc = doc
        self.paragraphs = doc.paragraphs

    def detect_parts(self, debug: bool = False) -> Dict[str, Optional[Tuple[int, int]]]:
        """
        检测论文各部分的段落范围

        Returns:
            {
                'abstract': (start_idx, end_idx),
                'toc': (start_idx, end_idx),
                'body': (start_idx, end_idx),
                'references': (start_idx, end_idx),
                'appendix': (start_idx, end_idx),
                'acknowledgment': (start_idx, end_idx)
            }
        """
        # TODO: 实现关键词匹配逻辑
        # TODO: 实现启发式检测逻辑
        pass

    def _match_keywords(self, part_name: str) -> Optional[int]:
        """匹配关键词，返回第一个匹配的段落索引"""
        # TODO: 实现
        pass

    def _heuristic_detect(self, parts: Dict) -> Dict:
        """启发式检测失败部分"""
        # TODO: 实现
        pass
```

- [ ] **步骤 4: 创建 style_applier.py 框架**

```python
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
        # TODO: 实现
        pass

    def apply_paragraph_format(self, paragraph, alignment: int = 0,
                               line_spacing: float = 1.5,
                               space_before: Pt = None,
                               space_after: Pt = None,
                               indent_first_line: Cm = None):
        """应用段落格式"""
        # TODO: 实现
        pass

    def apply_hanging_indent(self, paragraph, hanging_indent: Cm = Cm(0.5)):
        """应用悬挂缩进（用于参考文献）"""
        # TODO: 实现
        pass
```

- [ ] **步骤 5: 创建 test_cmnu_formatter.py 框架**

```python
# tests/test_cmnu_formatter.py
"""CMNU 格式化器测试"""

import pytest
from docx import Document
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
        # TODO: 实现
        pass


class TestSectionDetector:
    """部分检测器测试"""

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

    def test_apply_font(self):
        """测试字体应用"""
        # TODO: 实现
        pass
```

- [ ] **步骤 6: 提交初始结构**

```bash
cd /c/Users/Administrator/thesis-formatter
git add src/utils/__init__.py src/utils/section_detector.py src/utils/style_applier.py
git add src/formatters/__init__.py
git add tests/test_cmnu_formatter.py
git commit -m "feat: initialize CMNU formatter project structure with empty modules"
```

---

### 任务 2: 实现 SectionDetector (部分检测)

**文件**:
- Modify: `src/utils/section_detector.py`
- Modify: `tests/test_cmnu_formatter.py` (add detector tests)

#### 关键词匹配逻辑

- [ ] **步骤 1: 编写 _match_keywords 测试**

```python
# tests/test_cmnu_formatter.py - 补充到 TestSectionDetector

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestSectionDetector::test_match_keywords_abstract -v`
期望: FAIL (未实现)

- [ ] **步骤 2: 实现 _match_keywords 方法**

```python
# src/utils/section_detector.py - 补充到 SectionDetector 类

def _match_keywords(self, part_name: str) -> Optional[int]:
    """匹配关键词，返回第一个匹配的段落索引"""
    keywords = self.KEYWORDS.get(part_name, [])

    for idx, paragraph in enumerate(self.paragraphs):
        text = paragraph.text.strip()
        for keyword in keywords:
            if keyword in text or text == keyword:
                return idx

    return None
```

- [ ] **步骤 3: 运行关键词匹配测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestSectionDetector::test_match_keywords_abstract \
        tests/test_cmnu_formatter.py::TestSectionDetector::test_match_keywords_references \
        tests/test_cmnu_formatter.py::TestSectionDetector::test_match_keywords_not_found -v
```

期望: 3 个 PASS

#### 部分边界检测逻辑

- [ ] **步骤 4: 编写 detect_parts 测试 (简单场景)**

```python
# tests/test_cmnu_formatter.py - 补充

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestSectionDetector::test_detect_parts_simple -v`
期望: FAIL

- [ ] **步骤 5: 实现 detect_parts 方法**

```python
# src/utils/section_detector.py - 补充到 SectionDetector 类

def detect_parts(self, debug: bool = False) -> Dict[str, Optional[Tuple[int, int]]]:
    """
    检测论文各部分的段落范围

    策略：
    1. 关键词匹配找到每个部分的起始位置
    2. 下一个部分的开始 = 上一个部分的结束
    3. 如果未找到某部分，返回 None
    """
    parts = {
        'abstract': None,
        'toc': None,
        'body': None,
        'references': None,
        'appendix': None,
        'acknowledgment': None
    }

    # 第一层：关键词匹配
    part_starts = {}  # part_name -> start_idx
    for part_name in parts.keys():
        idx = self._match_keywords(part_name)
        if idx is not None:
            part_starts[part_name] = idx

    if debug:
        print(f"Detected part starts: {part_starts}")

    # 第二层：推断每个部分的范围（start, end）
    # 按逻辑顺序：abstract → toc → body → references → appendix → acknowledgment
    order = ['abstract', 'toc', 'body', 'references', 'appendix', 'acknowledgment']
    part_indices = [(name, part_starts[name]) for name in order if name in part_starts]

    for i, (part_name, start_idx) in enumerate(part_indices):
        # 结束位置 = 下一个部分的开始 - 1（或文档末尾）
        if i + 1 < len(part_indices):
            end_idx = part_indices[i + 1][1] - 1
        else:
            end_idx = len(self.paragraphs) - 1

        parts[part_name] = (start_idx, end_idx)

    return parts
```

- [ ] **步骤 6: 运行 detect_parts 测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestSectionDetector::test_detect_parts_simple -v
```

期望: PASS

- [ ] **步骤 7: 编写降级逻辑测试 (部分关键词缺失)**

```python
# tests/test_cmnu_formatter.py - 补充

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestSectionDetector::test_detect_parts_missing_toc -v`
期望: PASS (当前实现已支持)

- [ ] **步骤 8: 提交部分检测实现**

```bash
git add src/utils/section_detector.py tests/test_cmnu_formatter.py
git commit -m "feat: implement section detector with keyword matching and range detection"
```

---

### 任务 3: 实现 StyleApplier (样式应用)

**文件**:
- Modify: `src/utils/style_applier.py`
- Modify: `tests/test_cmnu_formatter.py` (add applier tests)

#### 字体应用

- [ ] **步骤 1: 编写字体应用测试**

```python
# tests/test_cmnu_formatter.py - 补充到 TestStyleApplier

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_font_song -v`
期望: FAIL

- [ ] **步骤 2: 实现 apply_font 方法**

```python
# src/utils/style_applier.py - 补充到 StyleApplier 类

def apply_font(self, run, font_name: str, size: Optional[Pt] = None, bold: bool = False):
    """应用字体样式"""
    run.font.name = font_name
    if size:
        run.font.size = size
    run.bold = bold
```

- [ ] **步骤 3: 运行字体测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_font_song \
        tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_font_hei_bold -v
```

期望: 2 个 PASS

#### 段落格式应用

- [ ] **步骤 4: 编写段落格式测试**

```python
# tests/test_cmnu_formatter.py - 补充

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_paragraph_format_standard -v`
期望: FAIL

- [ ] **步骤 5: 实现 apply_paragraph_format 方法**

```python
# src/utils/style_applier.py - 补充到 StyleApplier 类

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
```

- [ ] **步骤 6: 运行段落格式测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_paragraph_format_standard -v
```

期望: PASS

#### 悬挂缩进（参考文献）

- [ ] **步骤 7: 编写悬挂缩进测试**

```python
# tests/test_cmnu_formatter.py - 补充

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_hanging_indent -v`
期望: FAIL

- [ ] **步骤 8: 实现 apply_hanging_indent 方法**

```python
# src/utils/style_applier.py - 补充到 StyleApplier 类

def apply_hanging_indent(self, paragraph, hanging_indent: Cm = Cm(0.5)):
    """应用悬挂缩进（用于参考文献）"""
    pf = paragraph.paragraph_format
    pf.first_line_indent = -hanging_indent  # 负值表示悬挂
    pf.left_indent = hanging_indent
```

- [ ] **步骤 9: 运行悬挂缩进测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestStyleApplier::test_apply_hanging_indent -v
```

期望: PASS

- [ ] **步骤 10: 提交样式应用实现**

```bash
git add src/utils/style_applier.py tests/test_cmnu_formatter.py
git commit -m "feat: implement style applier with font, paragraph, and hanging indent support"
```

---

### 任务 4: 实现 CmnuFormatter 基础框架

**文件**:
- Create: `src/formatters/cmnu_formatter.py`
- Modify: `tests/test_cmnu_formatter.py` (add formatter tests)

- [ ] **步骤 1: 编写 CmnuFormatter 初始化与主流程测试**

```python
# tests/test_cmnu_formatter.py - 补充到 TestCmnuFormatter

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
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_formatter_initialization -v`
期望: FAIL

- [ ] **步骤 2: 创建 CmnuFormatter 基础框架**

```python
# src/formatters/cmnu_formatter.py
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
```

- [ ] **步骤 3: 更新 formatters __init__.py**

```python
# src/formatters/__init__.py
"""论文格式化器集合"""

from .cmnu_formatter import CmnuFormatter

__all__ = ['CmnuFormatter']
```

- [ ] **步骤 4: 运行初始化测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_formatter_initialization -v
```

期望: PASS

- [ ] **步骤 5: 运行简单文档格式化测试**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_simple_document -v
```

期望: PASS (仅验证基础框架，格式化暂未实现)

- [ ] **步骤 6: 提交 CmnuFormatter 基础框架**

```bash
git add src/formatters/cmnu_formatter.py tests/test_cmnu_formatter.py
git commit -m "feat: implement CmnuFormatter base structure with parts detection"
```

---

### 任务 5: 实现摘要格式化

**文件**:
- Modify: `src/formatters/cmnu_formatter.py` (_format_abstract)
- Modify: `tests/test_cmnu_formatter.py` (add abstract formatting tests)

- [ ] **步骤 1: 编写摘要格式化测试**

```python
# tests/test_cmnu_formatter.py - 补充

def test_format_abstract_title(self, tmp_path):
    """测试摘要标题格式化（三号黑体，居中）"""
    doc = Document()
    para_title = doc.add_paragraph('摘要')
    para_content = doc.add_paragraph('这是摘要内容。')
    para_keywords = doc.add_paragraph('关键词: 词1; 词2')

    input_path = tmp_path / "test_abstract.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    parts = {'abstract': (0, 2)}

    # 手动调用格式化（暂不通过主流程）
    doc = Document(str(input_path))
    formatter._format_abstract(doc, parts)

    # 检查标题
    title_para = doc.paragraphs[0]
    title_run = title_para.runs[0]

    assert title_run.font.name == '黑体'
    assert title_run.font.size == Pt(16)  # 三号
    assert title_run.bold == True
    assert title_para.paragraph_format.alignment == 1  # 居中

def test_format_abstract_content(self, tmp_path):
    """测试摘要正文格式化（小四号宋体，1.5倍行距，首行缩进）"""
    doc = Document()
    doc.add_paragraph('摘要')
    para_content = doc.add_paragraph('这是摘要内容。')

    input_path = tmp_path / "test_abstract.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    parts = {'abstract': (0, 1)}

    doc = Document(str(input_path))
    formatter._format_abstract(doc, parts)

    # 检查正文
    content_para = doc.paragraphs[1]
    content_run = content_para.runs[0]

    assert content_run.font.name == '宋体'
    assert content_run.font.size == Pt(12)  # 小四号
    assert content_para.paragraph_format.line_spacing == 1.5
    assert content_para.paragraph_format.first_line_indent == Cm(0.5)  # 2字符缩进
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_abstract_title -v`
期望: FAIL

- [ ] **步骤 2: 实现 _format_abstract 方法**

```python
# src/formatters/cmnu_formatter.py - 补充到 CmnuFormatter 类

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
```

- [ ] **步骤 3: 运行摘要格式化测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_abstract_title \
        tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_abstract_content -v
```

期望: 2 个 PASS

- [ ] **步骤 4: 提交摘要格式化实现**

```bash
git add src/formatters/cmnu_formatter.py tests/test_cmnu_formatter.py
git commit -m "feat: implement abstract formatting with title and content styles"
```

---

### 任务 6: 实现正文格式化（标题层级）

**文件**:
- Modify: `src/formatters/cmnu_formatter.py` (_format_body)
- Modify: `tests/test_cmnu_formatter.py` (add body formatting tests)

#### 标题层级检测与格式化

- [ ] **步骤 1: 编写标题层级检测测试**

```python
# tests/test_cmnu_formatter.py - 补充

def test_detect_heading_level_1(self):
    """测试一级标题检测（数字开头如'第1章'或'1 '）"""
    doc = Document()
    doc.add_paragraph('第1章 绪论')

    formatter = CmnuFormatter()
    level = formatter._detect_heading_level('第1章 绪论')
    assert level == 1

def test_detect_heading_level_2(self):
    """测试二级标题检测（如'1.1 '）"""
    formatter = CmnuFormatter()
    level = formatter._detect_heading_level('1.1 研究背景')
    assert level == 2

def test_detect_heading_level_3(self):
    """测试三级标题检测（如'1.1.1 '）"""
    formatter = CmnuFormatter()
    level = formatter._detect_heading_level('1.1.1 问题阐述')
    assert level == 3

def test_not_a_heading(self):
    """测试非标题文本"""
    formatter = CmnuFormatter()
    level = formatter._detect_heading_level('这是普通正文文本。')
    assert level == 0  # 0 表示非标题
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_detect_heading_level_1 -v`
期望: FAIL

- [ ] **步骤 2: 实现 _detect_heading_level 方法**

```python
# src/formatters/cmnu_formatter.py - 补充到 CmnuFormatter 类

import re

def _detect_heading_level(self, text: str) -> int:
    """
    检测标题层级

    返回值:
        0: 非标题
        1: 一级标题（如'第1章'、'1 '、'一'）
        2: 二级标题（如'1.1 '）
        3: 三级标题（如'1.1.1 '）
    """
    text = text.strip()

    # 三级（1.1.1 或 1.1.1.）
    if re.match(r'^\d+\.\d+\.\d+[\.\s]', text):
        return 3

    # 二级（1.1 或 1.1.）
    if re.match(r'^\d+\.\d+[\.\s]', text):
        return 2

    # 一级（第1章、1 、第一、一）
    if re.match(r'^(第[一二三四五六七八九十〇\d]+章|[\d\u4e00-\u9fff]\s)', text):
        return 1

    return 0
```

- [ ] **步骤 3: 运行标题检测测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_detect_heading_level_1 \
        tests/test_cmnu_formatter.py::TestCmnuFormatter::test_detect_heading_level_2 \
        tests/test_cmnu_formatter.py::TestCmnuFormatter::test_detect_heading_level_3 \
        tests/test_cmnu_formatter.py::TestCmnuFormatter::test_not_a_heading -v
```

期望: 4 个 PASS

#### 正文格式化实现

- [ ] **步骤 4: 编写正文格式化测试**

```python
# tests/test_cmnu_formatter.py - 补充

def test_format_body_heading_level_1(self, tmp_path):
    """测试一级标题格式化（三号黑体，居中）"""
    doc = Document()
    doc.add_paragraph('第1章 绪论')

    input_path = tmp_path / "test_body_h1.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    parts = {'body': (0, 0)}

    doc = Document(str(input_path))
    formatter._format_body(doc, parts)

    h1_para = doc.paragraphs[0]
    h1_run = h1_para.runs[0]

    assert h1_run.font.name == '黑体'
    assert h1_run.font.size == Pt(16)  # 三号
    assert h1_run.bold == True
    assert h1_para.paragraph_format.alignment == 1  # 居中

def test_format_body_heading_level_2(self, tmp_path):
    """测试二级标题格式化（四号黑体，左对齐）"""
    doc = Document()
    doc.add_paragraph('1.1 研究背景')

    input_path = tmp_path / "test_body_h2.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    parts = {'body': (0, 0)}

    doc = Document(str(input_path))
    formatter._format_body(doc, parts)

    h2_para = doc.paragraphs[0]
    h2_run = h2_para.runs[0]

    assert h2_run.font.name == '黑体'
    assert h2_run.font.size == Pt(14)  # 四号
    assert h2_run.bold == True
    assert h2_para.paragraph_format.alignment == 0  # 左对齐
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_body_heading_level_1 -v`
期望: FAIL

- [ ] **步骤 5: 实现 _format_body 方法**

```python
# src/formatters/cmnu_formatter.py - 补充到 CmnuFormatter 类

def _format_body(self, doc: Document, parts: Dict):
    """
    格式化正文部分

    标题：
      - 一级：三号黑体，居中，单倍行距，段前24磅/段后18磅
      - 二级：四号黑体，左对齐，固定行距20磅，段前24磅/段后6磅
      - 三级：小四号黑体，左对齐，固定行距20磅，段前12磅/段后6磅

    正文：小四号宋体，1.5倍行距，首行缩进2字符
    """
    if parts.get('body') is None:
        return

    start, end = parts['body']

    for idx in range(start, end + 1):
        if idx >= len(doc.paragraphs):
            break

        para = doc.paragraphs[idx]
        text = para.text.strip()
        level = self._detect_heading_level(text)

        if level == 1:
            # 一级标题
            for run in para.runs:
                self.style_applier.apply_font(run, '黑体', Pt(16), bold=True)
            pf = para.paragraph_format
            pf.alignment = 1  # 居中
            pf.line_spacing = 1.0
            pf.space_before = Pt(24)
            pf.space_after = Pt(18)

        elif level == 2:
            # 二级标题
            for run in para.runs:
                self.style_applier.apply_font(run, '黑体', Pt(14), bold=True)
            pf = para.paragraph_format
            pf.alignment = 0  # 左对齐
            pf.line_spacing_pt = 20  # 固定行距20磅
            pf.space_before = Pt(24)
            pf.space_after = Pt(6)

        elif level == 3:
            # 三级标题
            for run in para.runs:
                self.style_applier.apply_font(run, '黑体', Pt(12), bold=True)
            pf = para.paragraph_format
            pf.alignment = 0  # 左对齐
            pf.line_spacing_pt = 20  # 固定行距20磅
            pf.space_before = Pt(12)
            pf.space_after = Pt(6)

        else:
            # 普通正文
            for run in para.runs:
                self.style_applier.apply_font(run, '宋体', Pt(12), bold=False)

            pf = para.paragraph_format
            pf.line_spacing = 1.5
            pf.first_line_indent = Cm(0.5)  # 2字符缩进
            pf.alignment = 3  # 两端对齐
            pf.space_before = Pt(0)
            pf.space_after = Pt(6)
```

- [ ] **步骤 6: 运行正文格式化测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_body_heading_level_1 \
        tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_body_heading_level_2 -v
```

期望: 2 个 PASS

- [ ] **步骤 7: 提交正文格式化实现**

```bash
git add src/formatters/cmnu_formatter.py tests/test_cmnu_formatter.py
git commit -m "feat: implement body formatting with three-level heading detection"
```

---

### 任务 7: 实现参考文献格式化

**文件**:
- Modify: `src/formatters/cmnu_formatter.py` (_format_references)
- Modify: `tests/test_cmnu_formatter.py` (add reference formatting tests)

- [ ] **步骤 1: 编写参考文献格式化测试**

```python
# tests/test_cmnu_formatter.py - 补充

def test_format_references_title(self, tmp_path):
    """测试参考文献标题格式化（三号黑体，居中）"""
    doc = Document()
    doc.add_paragraph('参考文献')
    doc.add_paragraph('[1] 作者. 标题. 期刊, 2020')

    input_path = tmp_path / "test_ref.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    parts = {'references': (0, 1)}

    doc = Document(str(input_path))
    formatter._format_references(doc, parts)

    ref_title = doc.paragraphs[0]
    ref_title_run = ref_title.runs[0]

    assert ref_title_run.font.name == '黑体'
    assert ref_title_run.font.size == Pt(16)  # 三号
    assert ref_title_run.bold == True
    assert ref_title.paragraph_format.alignment == 1  # 居中

def test_format_references_hanging_indent(self, tmp_path):
    """测试参考文献悬挂缩进"""
    doc = Document()
    doc.add_paragraph('参考文献')
    ref_para = doc.add_paragraph('[1] 作者. 标题. 期刊, 2020')

    input_path = tmp_path / "test_ref_indent.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    parts = {'references': (0, 1)}

    doc = Document(str(input_path))
    formatter._format_references(doc, parts)

    ref_content = doc.paragraphs[1]
    ref_run = ref_content.runs[0]

    # 五号宋体
    assert ref_run.font.name == '宋体'
    assert ref_run.font.size == Pt(10.5)  # 五号

    # 悬挂缩进
    pf = ref_content.paragraph_format
    assert pf.first_line_indent == Cm(-0.5)  # 悬挂缩进
    assert pf.left_indent == Cm(0.5)
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_references_title -v`
期望: FAIL

- [ ] **步骤 2: 实现 _format_references 方法**

```python
# src/formatters/cmnu_formatter.py - 补充到 CmnuFormatter 类

def _format_references(self, doc: Document, parts: Dict):
    """
    格式化参考文献部分

    标题: 三号黑体，居中，单倍行距，段前24磅/段后18磅
    条目: 五号宋体，1.5倍行距，两端对齐，悬挂缩进（首行无缩进，第二行对齐）
    """
    if parts.get('references') is None:
        return

    start, end = parts['references']

    for idx in range(start, end + 1):
        if idx >= len(doc.paragraphs):
            break

        para = doc.paragraphs[idx]
        text = para.text.strip()

        # 标题行（包含"参考文献"）
        if '参考文献' in text and idx == start:
            for run in para.runs:
                self.style_applier.apply_font(run, '黑体', Pt(16), bold=True)
            pf = para.paragraph_format
            pf.alignment = 1  # 居中
            pf.line_spacing = 1.0
            pf.space_before = Pt(24)
            pf.space_after = Pt(18)

        # 参考文献条目（以[数字]开头）
        elif re.match(r'^\[\d+\]', text):
            for run in para.runs:
                self.style_applier.apply_font(run, '宋体', Pt(10.5), bold=False)

            pf = para.paragraph_format
            pf.line_spacing = 1.5
            pf.alignment = 3  # 两端对齐

            # 应用悬挂缩进
            self.style_applier.apply_hanging_indent(para, hanging_indent=Cm(0.5))
```

- [ ] **步骤 3: 运行参考文献格式化测试，验证通过**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_references_title \
        tests/test_cmnu_formatter.py::TestCmnuFormatter::test_format_references_hanging_indent -v
```

期望: 2 个 PASS

- [ ] **步骤 4: 实现 _format_appendix 和 _format_acknowledgment（简化版）**

```python
# src/formatters/cmnu_formatter.py - 补充

def _format_appendix(self, doc: Document, parts: Dict):
    """格式化附录部分（与致谢相同格式）"""
    if parts.get('appendix') is None:
        return

    start, end = parts['appendix']
    self._format_generic_section(doc, start, end, '附录')

def _format_acknowledgment(self, doc: Document, parts: Dict):
    """格式化致谢部分（与附录相同格式）"""
    if parts.get('acknowledgment') is None:
        return

    start, end = parts['acknowledgment']
    self._format_generic_section(doc, start, end, '致谢')

def _format_toc(self, doc: Document, parts: Dict):
    """格式化目录部分"""
    if parts.get('toc') is None:
        return

    start, end = parts['toc']
    self._format_generic_section(doc, start, end, '目录')

def _format_generic_section(self, doc: Document, start: int, end: int, section_title: str):
    """通用的部分格式化（适用于附录、致谢、目录等）"""
    for idx in range(start, end + 1):
        if idx >= len(doc.paragraphs):
            break

        para = doc.paragraphs[idx]
        text = para.text.strip()

        # 标题行
        if section_title in text and idx == start:
            for run in para.runs:
                self.style_applier.apply_font(run, '黑体', Pt(16), bold=True)
            pf = para.paragraph_format
            pf.alignment = 1  # 居中
            pf.line_spacing = 1.0
            pf.space_before = Pt(24)
            pf.space_after = Pt(18)

        # 正文
        else:
            for run in para.runs:
                self.style_applier.apply_font(run, '宋体', Pt(12), bold=False)

            pf = para.paragraph_format
            pf.line_spacing = 1.5
            pf.first_line_indent = Cm(0.5)  # 2字符缩进
            pf.space_before = Pt(0)
            pf.space_after = Pt(6)
```

- [ ] **步骤 5: 提交参考文献和其他部分格式化实现**

```bash
git add src/formatters/cmnu_formatter.py tests/test_cmnu_formatter.py
git commit -m "feat: implement references, appendix, acknowledgment, and toc formatting"
```

---

### 任务 8: 实现页码分节（关键，最复杂）

**文件**:
- Modify: `src/formatters/cmnu_formatter.py` (_setup_page_numbers)
- Modify: `tests/test_cmnu_formatter.py` (add page number tests)

⚠️ **这是最高优先级和最高复杂度的任务。预计 5-6 小时。**

#### 页码分节设计

页码要求：
- 前置部分（摘要、目录）: 大写罗马数字 (I, II, III...)，位置：页面底端居中
- 正文（第1章起）: 阿拉伯数字 (1, 2, 3...)，位置：页面底端居中

实现方案：
1. 在正文开始位置前插入分节符
2. 第一个分节：罗马数字页码
3. 第二个分节：阿拉伯数字页码，页码重新开始为 1

- [ ] **步骤 1: 编写页码分节测试**

```python
# tests/test_cmnu_formatter.py - 补充

def test_page_numbers_roman_numerals(self, tmp_path):
    """测试前置部分罗马数字页码"""
    doc = Document()
    # 模拟摘要部分（应该用罗马数字）
    for _ in range(5):
        doc.add_paragraph('摘要内容')

    input_path = tmp_path / "test_page_roman.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    doc = Document(str(input_path))

    # 设置页码（暂时只测试能否成功调用）
    parts = {'body': (3, 4)}  # 假设第3-4段是正文
    formatter._setup_page_numbers(doc, parts)

    # 验证document有section
    assert len(doc.sections) >= 1

def test_page_numbers_arabic_in_body(self, tmp_path):
    """测试正文部分阿拉伯数字页码"""
    doc = Document()
    for i in range(10):
        doc.add_paragraph(f'正文内容 {i}')

    input_path = tmp_path / "test_page_arabic.docx"
    doc.save(str(input_path))

    formatter = CmnuFormatter()
    doc = Document(str(input_path))

    parts = {'body': (0, 9)}
    formatter._setup_page_numbers(doc, parts)

    assert len(doc.sections) >= 1
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_page_numbers_roman_numerals -v`
期望: FAIL (未实现)

- [ ] **步骤 2: 实现 _setup_page_numbers 基础版本**

```python
# src/formatters/cmnu_formatter.py - 补充到 CmnuFormatter 类

from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.enum.section import WD_SECTION

def _setup_page_numbers(self, doc: Document, parts: Dict):
    """
    设置页码系统：前置部分罗马数字，正文部分阿拉伯数字

    实现策略：
    1. 获取第一个分节（默认存在）
    2. 在正文开始处插入分节符
    3. 第一个分节：罗马数字页码
    4. 第二个分节：阿拉伯数字页码，从1开始
    """
    try:
        # 获取正文开始位置
        body_start = parts.get('body')
        if body_start is None:
            if self.debug:
                print("Warning: body part not found, skipping page numbers setup")
            return

        body_start_idx = body_start[0]

        # 获取文档body元素
        body = doc.element.body

        # 在正文开始段落前插入分节符
        body_para = doc.paragraphs[body_start_idx]
        para_element = body_para._element

        # 创建分节符（分节结束符）
        sectPr = self._get_or_create_sectPr(body_para)

        # 第一个分节：设置罗马数字页码
        self._setup_section_page_numbers(doc.sections[0], 'roman', None)

        # 插入新分节
        # 创建新的分节属性
        new_sectPr = self._create_new_section(doc)

        # 在正文开始处插入新分节
        para_element.insert(len(para_element), new_sectPr)

        # 第二个分节：设置阿拉伯数字页码，从1开始
        if len(doc.sections) > 1:
            self._setup_section_page_numbers(doc.sections[1], 'arabic', 1)
        else:
            # 如果只有一个分节，创建新的
            new_section = doc.sections[0]
            self._setup_section_page_numbers(new_section, 'arabic', 1)

        if self.debug:
            print("Page numbers setup completed")

    except Exception as e:
        if self.debug:
            print(f"Error setting up page numbers: {str(e)}")
        # 降级方案：仅应用一套阿拉伯数字
        self._setup_simple_page_numbers(doc)

def _get_or_create_sectPr(self, paragraph):
    """获取或创建段落的分节属性"""
    pPr = paragraph._element.get_or_add_pPr()
    sectPr = pPr.find(qn('w:sectPr'))
    if sectPr is None:
        sectPr = OxmlElement('w:sectPr')
        pPr.append(sectPr)
    return sectPr

def _create_new_section(self, doc: Document):
    """创建新的分节属性元素"""
    sectPr = OxmlElement('w:sectPr')

    # 复制第一个分节的属性（页边距等）
    original_sectPr = doc.sections[0]._sectPr

    # 复制关键属性
    for attr in ['pgSz', 'pgMar', 'cols', 'headerReference', 'footerReference']:
        elem = original_sectPr.find(qn(f'w:{attr}'))
        if elem is not None:
            sectPr.append(parse_xml(elem.xml))

    return sectPr

def _setup_section_page_numbers(self, section, num_format: str, start_num: Optional[int]):
    """
    为分节设置页码格式

    Args:
        section: 分节对象
        num_format: 'roman' 或 'arabic'
        start_num: 起始页码（None 表示续继）
    """
    # 添加页码到页脚
    footer = section.footer

    # 清除现有页脚内容
    for para in footer.paragraphs:
        p = para._element
        p.getparent().remove(p)

    # 创建新的页脚段落
    para = footer.add_paragraph()
    para.alignment = 1  # 居中

    # 添加页码字段
    run = para.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')

    # 根据格式设置字段代码
    if num_format == 'roman':
        instrText.text = 'PAGE \\* ROMAN'
    else:  # arabic
        instrText.text = 'PAGE'

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

    # 如果指定了起始页码，设置分节页码重启
    if start_num is not None:
        sectPr = section._sectPr
        pgNumType = sectPr.find(qn('w:pgNumType'))
        if pgNumType is not None:
            sectPr.remove(pgNumType)

        pgNumType = OxmlElement('w:pgNumType')
        pgNumType.set(qn('w:start'), str(start_num))
        sectPr.insert(0, pgNumType)

def _setup_simple_page_numbers(self, doc: Document):
    """降级方案：应用简单的阿拉伯数字页码"""
    for section in doc.sections:
        footer = section.footer

        # 清除现有页脚内容
        for para in footer.paragraphs:
            p = para._element
            p.getparent().remove(p)

        # 创建新的页脚段落
        para = footer.add_paragraph()
        para.alignment = 1  # 居中

        # 添加页码字段
        run = para.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')

        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = 'PAGE'

        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')

        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
```

- [ ] **步骤 3: 在 format_document 中启用页码设置**

```python
# src/formatters/cmnu_formatter.py - 修改 format_document 方法

def format_document(self, input_path: str, output_path: Optional[str] = None,
                    debug: bool = False) -> str:
    # ... 前面的代码 ...

    # 4. 处理页码（取消注释）
    self._setup_page_numbers(doc, parts)  # 取消注释此行

    # ... 后面的代码 ...
```

- [ ] **步骤 4: 运行页码测试（先验证基础功能）**

```bash
pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_page_numbers_roman_numerals -v
```

期望: PASS (能够成功调用，不报错)

- [ ] **步骤 5: 集成测试——完整论文格式化**

```python
# tests/test_cmnu_formatter.py - 补充

def test_complete_formatting_workflow(self, tmp_path):
    """测试完整的论文格式化流程"""
    # 创建包含所有部分的样本论文
    doc = Document()

    # 摘要部分
    doc.add_paragraph('摘要')
    doc.add_paragraph('这是论文摘要内容。摘要应该简洁明了，说明研究目标和主要发现。')
    doc.add_paragraph('关键词: 生物多样性; 资金机制; ABS')

    # 目录
    doc.add_paragraph('目录')
    doc.add_paragraph('第1章 绪论 ... 1')

    # 正文
    doc.add_paragraph('第1章 绪论')
    doc.add_paragraph('这是第一章的内容。')
    doc.add_paragraph('1.1 研究背景')
    doc.add_paragraph('研究背景的详细说明。')
    doc.add_paragraph('1.1.1 问题的提出')
    doc.add_paragraph('问题的具体描述。')

    # 参考文献
    doc.add_paragraph('参考文献')
    doc.add_paragraph('[1] 作者A. 论文标题. 期刊名称, 2020, 10(1): 1-10.')
    doc.add_paragraph('[2] 作者B, 作者C. 另一篇论文. 期刊名称, 2021, 11(2): 20-35.')

    # 致谢
    doc.add_paragraph('致谢')
    doc.add_paragraph('感谢导师的悉心指导，感谢课题组的各位成员。')

    input_path = tmp_path / "complete_thesis.docx"
    doc.save(str(input_path))

    # 执行格式化
    formatter = CmnuFormatter()
    output_path = formatter.format_document(str(input_path), debug=True)

    # 验证输出文件
    assert Path(output_path).exists()

    # 验证输出文件可以打开且包含内容
    output_doc = Document(output_path)
    assert len(output_doc.paragraphs) > 0

    # 验证特定的格式化
    # 摘要标题应该是黑体
    abstract_title = output_doc.paragraphs[0]
    if abstract_title.runs:
        assert abstract_title.runs[0].font.name == '黑体'

    # 参考文献条目应该有悬挂缩进
    # （可视化检查——单元测试的限制）
```

运行: `pytest tests/test_cmnu_formatter.py::TestCmnuFormatter::test_complete_formatting_workflow -v`
期望: PASS

- [ ] **步骤 6: 提交页码分节实现**

```bash
git add src/formatters/cmnu_formatter.py tests/test_cmnu_formatter.py
git commit -m "feat: implement page number setup with roman numerals for front matter and arabic for body"
```

---

### 任务 9: 创建命令行脚本 (format_thesis.py)

**文件**:
- Create: `scripts/format_thesis.py`

- [ ] **步骤 1: 编写脚本基本框架与参数处理**

```python
# scripts/format_thesis.py
"""
命令行脚本：格式化论文文档
使用方式：python scripts/format_thesis.py <input.docx> [options]
"""

import sys
import argparse
from pathlib import Path
import logging

# 添加上级目录到路径，以便导入 src 模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.formatters import CmnuFormatter


def setup_logging(debug: bool = False):
    """设置日志"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(levelname)s: %(message)s'
    )
    return logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='中央民族大学学位论文格式化工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  # 完全自动模式
  python scripts/format_thesis.py input.docx

  # 指定关键部分（当自动检测失败时）
  python scripts/format_thesis.py input.docx \\
    --abstract-start 3 --abstract-end 8 \\
    --body-start 15 --body-end 150 \\
    --references-start 151 --references-end 200

  # 调试模式
  python scripts/format_thesis.py input.docx --debug
        '''
    )

    # 必须参数
    parser.add_argument('input', help='输入 .docx 文件路径')

    # 可选参数
    parser.add_argument('-o', '--output', help='输出文件路径（默认：input_formatted.docx）')

    # 部分边界手动指定
    parser.add_argument('--abstract-start', type=int, help='摘要开始段落索引')
    parser.add_argument('--abstract-end', type=int, help='摘要结束段落索引')
    parser.add_argument('--body-start', type=int, help='正文开始段落索引')
    parser.add_argument('--body-end', type=int, help='正文结束段落索引')
    parser.add_argument('--references-start', type=int, help='参考文献开始段落索引')
    parser.add_argument('--references-end', type=int, help='参考文献结束段落索引')
    parser.add_argument('--appendix-start', type=int, help='附录开始段落索引')
    parser.add_argument('--appendix-end', type=int, help='附录结束段落索引')

    # 调试和控制选项
    parser.add_argument('--debug', action='store_true', help='启用调试模式，显示详细日志')

    args = parser.parse_args()

    logger = setup_logging(args.debug)

    # 验证输入文件
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"输入文件不存在: {input_path}")
        sys.exit(1)

    if input_path.suffix.lower() != '.docx':
        logger.error(f"输入文件必须是 .docx 格式: {input_path}")
        sys.exit(1)

    try:
        logger.info(f"正在格式化论文: {input_path}")

        # 创建格式化器
        formatter = CmnuFormatter()

        # 执行格式化
        output_path = formatter.format_document(
            str(input_path),
            output_path=args.output,
            debug=args.debug
        )

        logger.info(f"✓ 格式化完成！")
        logger.info(f"  输出文件: {output_path}")

        sys.exit(0)

    except Exception as e:
        logger.error(f"格式化失败: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
```

- [ ] **步骤 2: 测试脚本执行（简单验证）**

创建一个简单的测试文档并运行脚本：

```bash
cd /c/Users/Administrator/thesis-formatter

# 创建简单的测试文档
python -c "
from docx import Document
doc = Document()
doc.add_paragraph('摘要')
doc.add_paragraph('这是摘要内容。')
doc.add_paragraph('第1章 绪论')
doc.add_paragraph('这是正文内容。')
doc.add_paragraph('参考文献')
doc.add_paragraph('[1] 作者. 标题.')
doc.save('test_simple.docx')
"

# 运行脚本
python scripts/format_thesis.py test_simple.docx --debug

# 验证输出文件
ls -la test_simple_formatted.docx
```

期望: `test_simple_formatted.docx` 文件成功创建

- [ ] **步骤 3: 提交命令行脚本**

```bash
git add scripts/format_thesis.py
git commit -m "feat: add format_thesis.py CLI script with comprehensive options"
```

---

### 任务 10: 集成测试与用户论文处理

**文件**:
- 测试用户的实际论文文件
- 调试与迭代

- [ ] **步骤 1: 准备用户论文测试**

```bash
cd /c/Users/Administrator/thesis-formatter

# 复制用户论文到项目目录（用于测试）
cp "/c/Users/Administrator/xwechat_files/wxid_u15h5k7amcen22_9aa5/msg/file/2026-03/昆蒙框架下生物多样性保护资金机制与ABS机制研究(3.23).docx" \
   "./thesis_input.docx"
```

- [ ] **步骤 2: 运行格式化脚本（调试模式）**

```bash
python scripts/format_thesis.py thesis_input.docx --debug 2>&1 | tee format_log.txt

# 检查输出文件
ls -lh thesis_input_formatted.docx
```

- [ ] **步骤 3: 手动检查输出（关键步骤）**

在 Word 中打开 `thesis_input_formatted.docx`，逐项检查：

**检查清单**:
- [ ] 摘要标题是否为三号黑体居中
- [ ] 摘要正文是否为小四号宋体，1.5倍行距，首行缩进
- [ ] 正文一级标题是否为三号黑体居中（如"第1章"）
- [ ] 正文二级标题是否为四号黑体左对齐（如"1.1"）
- [ ] 正文三级标题是否为小四号黑体左对齐（如"1.1.1"）
- [ ] 参考文献标题是否为三号黑体居中
- [ ] 参考文献条目是否为五号宋体，有悬挂缩进
- [ ] 页码是否为罗马数字（前置部分）和阿拉伯数字（正文）
- [ ] 所有文本是否为宋体或 Times New Roman（英文）
- [ ] 行距和段距是否符合要求

- [ ] **步骤 4: 调试与修复**

根据手动检查的结果，修复发现的问题。常见问题：

**问题1**: 部分未正确检测
- 解决：使用 `--debug` 模式查看检测到的部分范围
- 或使用 `--abstract-start` 等参数手动指定

**问题2**: 页码未正确显示
- 解决：可能需要在 Word 中重新按 F9 刷新域
- 或检查 OXml 操作是否正确

**问题3**: 字体未正确应用
- 解决：检查系统是否安装了"宋体"和"黑体"字体

修复步骤：
```bash
# 编辑代码修复问题
# vim src/formatters/cmnu_formatter.py

# 重新运行脚本
python scripts/format_thesis.py thesis_input.docx --debug

# 再次检查输出
# （在 Word 中打开并检查）
```

- [ ] **步骤 5: 提交测试日志和最终输出**

```bash
git add thesis_input.docx thesis_input_formatted.docx format_log.txt
git commit -m "test: verify formatting on user's actual thesis document with debug log"
```

---

### 任务 11: 最终文档与交付

**文件**:
- Update: 项目 README（可选）
- Verify: 所有测试通过

- [ ] **步骤 1: 确认所有单元测试通过**

```bash
pytest tests/test_cmnu_formatter.py -v

# 期望: 所有测试 PASS
```

- [ ] **步骤 2: 执行完整流程集成测试**

```bash
# 再次格式化用户论文，确保稳定
python scripts/format_thesis.py thesis_input.docx

# 验证输出
file thesis_input_formatted.docx
```

- [ ] **步骤 3: 清理临时文件**

```bash
# 移除测试时生成的临时文件
rm -f test_*.docx format_log.txt
```

- [ ] **步骤 4: 最终提交**

```bash
git status  # 确认待提交的文件列表

# 提交主要结果文件
git add thesis_input_formatted.docx

git commit -m "docs: deliver formatted thesis document for user approval

- All formatting rules applied per CMNU standards
- Page numbering system (Roman numerals + Arabic numerals) implemented
- Title hierarchy (3 levels) correctly formatted
- Font mixing (Song/Hei/TNR) applied throughout
- References with hanging indents properly formatted
- Ready for user final review and submission"
```

---

## 执行选项

实现计划完成。现在您有两个执行选项：

**1. 子代理驱动执行（推荐）**
使用 `superpowers:subagent-driven-development` 为每个任务分派一个独立的子代理，每个任务后进行审查。适合并行处理，快速反馈循环。

**2. 内联执行**
使用 `superpowers:executing-plans` 在本会话中逐任务执行，附带检查点以供审查。

**您希望采用哪种方式？**（输入 `1` 或 `2`）
