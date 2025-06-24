"""
交易记录检测模块
- 验证和精炼从OCR服务获取的交易信息
- 使用关键字和正则表达式作为补充手段
"""

import re
import logging
from typing import Optional

from models import ReceiptInfo

logger = logging.getLogger(__name__)

class ReceiptDetector:
    """交易记录检测和信息提取器"""

    PLATFORM_KEYWORDS = {
        "微信支付": ["微信支付", "微信收款", "WeChat Pay"],
        "支付宝": ["支付宝", "Alipay", "收钱码"],
    }
    
    # 正则表达式，用于匹配如 "¥123.45" 或 "123.45元" 的金额格式
    AMOUNT_PATTERN = re.compile(r"(?:￥|¥|RMB)\s*(\d+\.\d{2})|(\d+\.\d{2})\s*元")

    def detect(self, ocr_result: ReceiptInfo) -> ReceiptInfo:
        """
        对OCR结果进行二次检测和精炼。
        - 如果平台信息缺失，通过关键字识别。
        - 如果金额信息缺失，通过正则表达式提取。
        - 基于提取到的信息，最终确认是否为交易凭证。
        """
        logger.debug(f"开始精炼OCR结果: {ocr_result.raw_text[:50]}...")

        # 1. 如果平台未识别，则尝试通过关键字识别
        if not ocr_result.platform:
            platform = self._detect_platform(ocr_result.raw_text)
            if platform:
                ocr_result.platform = platform
                logger.info(f"通过关键字检测到平台: {platform}")

        # 2. 如果金额未识别，则尝试通过正则提取
        if ocr_result.amount is None:
            amount = self._extract_amount(ocr_result.raw_text)
            if amount is not None:
                ocr_result.amount = amount
                logger.info(f"通过正则表达式提取到金额: {amount}")
        
        # 3. 根据平台和金额信息，最终确认是否为交易记录
        if ocr_result.platform and ocr_result.amount is not None:
            if not ocr_result.is_receipt:
                ocr_result.is_receipt = True
                logger.info("根据平台和金额信息，更新识别结果为'交易记录'")

        logger.debug("精炼完成")
        return ocr_result

    def _detect_platform(self, text: str) -> Optional[str]:
        """通过关键词检测支付平台"""
        for platform, keywords in self.PLATFORM_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return platform
        return None

    def _extract_amount(self, text: str) -> Optional[float]:
        """
        从文本中提取交易金额。
        """
        matches = self.AMOUNT_PATTERN.finditer(text)
        for match in matches:
            # group(1) 对应 ¥12.34, group(2) 对应 12.34元
            amount_str = match.group(1) or match.group(2)
            if amount_str:
                try:
                    return float(amount_str)
                except (ValueError, TypeError):
                    continue
        return None

def test_detector():
    """测试检测器功能"""
    print("--- 测试交易记录检测器 ---")
    detector = ReceiptDetector()
    
    # 测试用例1: 支付宝，OCR未能提取任何信息
    text1 = "【支付宝】收款到账123.45元。付款方：张三"
    info1 = ReceiptInfo(is_receipt=False, confidence=0.8, raw_text=text1)
    result1 = detector.detect(info1)
    print(f"测试1 - 原始文本: {text1}")
    print(f"测试1 - 检测结果: is_receipt={result1.is_receipt}, platform='{result1.platform}', amount={result1.amount}")
    assert result1.is_receipt is True
    assert result1.platform == "支付宝"
    assert result1.amount == 123.45

    # 测试用例2: 微信支付，OCR只识别出是凭证，但未提取平台和金额
    text2 = "微信支付收款凭证\\n收款金额\\n¥88.00\\n当前状态\\n已收款\\n付款方\\n李四"
    info2 = ReceiptInfo(is_receipt=True, platform=None, amount=None, confidence=0.9, raw_text=text2)
    result2 = detector.detect(info2)
    print(f"测试2 - 原始文本: {text2[:25]}...")
    print(f"测试2 - 检测结果: is_receipt={result2.is_receipt}, platform='{result2.platform}', amount={result2.amount}")
    assert result2.is_receipt is True
    assert result2.platform == "微信支付"
    assert result2.amount == 88.00

    # 测试用例3: 非交易记录
    text3 = "这是一张普通的风景照片，没有任何交易信息。"
    info3 = ReceiptInfo(is_receipt=False, confidence=0.95, raw_text=text3)
    result3 = detector.detect(info3)
    print(f"测试3 - 原始文本: {text3}")
    print(f"测试3 - 检测结果: is_receipt={result3.is_receipt}, platform='{result3.platform}', amount={result3.amount}")
    assert result3.is_receipt is False

    print("✅ 所有测试用例通过！")

if __name__ == '__main__':
    # 配置日志以查看详细信息
    logging.basicConfig(level=logging.INFO)
    test_detector() 