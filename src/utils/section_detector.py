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
