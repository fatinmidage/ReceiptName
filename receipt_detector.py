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
    
    # 正则表达式，用于匹配如 "¥123.45" 或 "123.45元" 的金额格式，支持负数
    AMOUNT_PATTERN = re.compile(r"(?:￥|¥|RMB)\s*(-?\d+\.\d{2})|(-?\d+\.\d{2})\s*元")

    def detect(self, ocr_result: ReceiptInfo) -> ReceiptInfo:
        """
        对OCR结果进行二次检测和精炼。
        - 首先检查图片类型，如果是拍照则直接设为非交易记录
        - 如果平台信息缺失，通过关键字识别。
        - 如果金额信息缺失，通过正则表达式提取。
        - 基于提取到的信息，最终确认是否为交易凭证。
        """
        logger.debug(f"开始精炼OCR结果: {ocr_result.raw_text[:50]}...")

        # 0. 首先检查图片类型 - 如果是拍照的图片，直接设为非交易记录
        if ocr_result.image_type == "拍照":
            ocr_result.is_receipt = False
            logger.info("检测到拍照图片，设置为非交易记录")
            return ocr_result

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
        
        # 3. 对识别到的金额进行绝对值处理（处理负数情况）
        if ocr_result.amount is not None and ocr_result.amount < 0:
            original_amount = ocr_result.amount
            ocr_result.amount = abs(ocr_result.amount)
            logger.info(f"检测到负数金额 {original_amount}，转换为绝对值: {ocr_result.amount}")
        
        # 4. 根据平台和金额信息，最终确认是否为交易记录（仅对截图有效）
        if ocr_result.image_type == "截图" and ocr_result.platform and ocr_result.amount is not None:
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
        如果金额为负数，将返回其绝对值。
        """
        matches = self.AMOUNT_PATTERN.finditer(text)
        for match in matches:
            # group(1) 对应 ¥12.34, group(2) 对应 12.34元
            amount_str = match.group(1) or match.group(2)
            if amount_str:
                try:
                    amount = float(amount_str)
                    # 对负数取绝对值
                    if amount < 0:
                        logger.info(f"提取到负数金额 {amount}，转换为绝对值: {abs(amount)}")
                        amount = abs(amount)
                    return amount
                except (ValueError, TypeError):
                    continue
        return None

def test_detector():
    """测试检测器功能"""
    print("--- 测试交易记录检测器 ---")
    detector = ReceiptDetector()
    
    # 测试用例1: 支付宝截图，OCR未能提取任何信息
    text1 = "【支付宝】收款到账123.45元。付款方：张三"
    info1 = ReceiptInfo(is_receipt=False, image_type="截图", confidence=0.8, raw_text=text1)
    result1 = detector.detect(info1)
    print(f"测试1 - 原始文本: {text1}")
    print(f"测试1 - 检测结果: is_receipt={result1.is_receipt}, image_type='{result1.image_type}', platform='{result1.platform}', amount={result1.amount}")
    assert result1.is_receipt is True
    assert result1.platform == "支付宝"
    assert result1.amount == 123.45

    # 测试用例2: 微信支付截图，OCR只识别出是凭证，但未提取平台和金额
    text2 = "微信支付收款凭证\\n收款金额\\n¥88.00\\n当前状态\\n已收款\\n付款方\\n李四"
    info2 = ReceiptInfo(is_receipt=True, image_type="截图", platform=None, amount=None, confidence=0.9, raw_text=text2)
    result2 = detector.detect(info2)
    print(f"测试2 - 原始文本: {text2[:25]}...")
    print(f"测试2 - 检测结果: is_receipt={result2.is_receipt}, image_type='{result2.image_type}', platform='{result2.platform}', amount={result2.amount}")
    assert result2.is_receipt is True
    assert result2.platform == "微信支付"
    assert result2.amount == 88.00

    # 测试用例3: 非交易记录截图
    text3 = "这是一张普通的风景照片，没有任何交易信息。"
    info3 = ReceiptInfo(is_receipt=False, image_type="截图", confidence=0.95, raw_text=text3)
    result3 = detector.detect(info3)
    print(f"测试3 - 原始文本: {text3}")
    print(f"测试3 - 检测结果: is_receipt={result3.is_receipt}, image_type='{result3.image_type}', platform='{result3.platform}', amount={result3.amount}")
    assert result3.is_receipt is False

    # 测试用例4: 拍照的支付凭证（应该被拒绝）
    text4 = "微信支付收款凭证\\n收款金额\\n¥99.99\\n当前状态\\n已收款"
    info4 = ReceiptInfo(is_receipt=True, image_type="拍照", platform="微信支付", amount=99.99, confidence=0.9, raw_text=text4)
    result4 = detector.detect(info4)
    print(f"测试4 - 原始文本: {text4[:25]}...")
    print(f"测试4 - 检测结果: is_receipt={result4.is_receipt}, image_type='{result4.image_type}', platform='{result4.platform}', amount={result4.amount}")
    assert result4.is_receipt is False  # 拍照的图片应该被拒绝

    # 测试用例5: 负数金额处理测试
    text5 = "支付宝退款凭证\\n退款金额\\n¥-66.50\\n状态\\n已退款"
    info5 = ReceiptInfo(is_receipt=True, image_type="截图", platform="支付宝", amount=-66.50, confidence=0.9, raw_text=text5)
    result5 = detector.detect(info5)
    print(f"测试5 - 原始文本: {text5}")
    print(f"测试5 - 检测结果: is_receipt={result5.is_receipt}, image_type='{result5.image_type}', platform='{result5.platform}', amount={result5.amount}")
    assert result5.is_receipt is True
    assert result5.platform == "支付宝"
    assert result5.amount == 66.50  # 负数应该被转换为正数

    # 测试用例6: 数据模型验证器测试
    print("测试6 - 数据模型验证器测试")
    info6 = ReceiptInfo(is_receipt=True, image_type="截图", platform="微信支付", amount=-100.00, confidence=0.9, raw_text="测试负数")
    print(f"测试6 - 通过验证器处理的负数金额: {info6.amount}")
    assert info6.amount == 100.00  # 验证器应该自动转换为正数

    # 测试用例7: 正则表达式提取负数金额测试
    text7 = "微信支付退款凭证 退款金额 ¥-55.88 已退回原付款账户"
    info7 = ReceiptInfo(is_receipt=False, image_type="截图", confidence=0.8, raw_text=text7)
    result7 = detector.detect(info7)
    print(f"测试7 - 原始文本: {text7}")
    print(f"测试7 - 检测结果: is_receipt={result7.is_receipt}, image_type='{result7.image_type}', platform='{result7.platform}', amount={result7.amount}")
    assert result7.platform == "微信支付"
    assert result7.amount == 55.88  # 负数应该被转换为正数

    print("✅ 所有测试用例通过！")

if __name__ == '__main__':
    # 配置日志以查看详细信息
    logging.basicConfig(level=logging.INFO)
    test_detector() 