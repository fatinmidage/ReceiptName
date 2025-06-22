#!/usr/bin/env python3
"""
OCR服务测试脚本
用于验证OCR服务是否正常工作
"""

import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from ocr_service import OCRService, ReceiptInfo


def test_config():
    """测试配置"""
    print("🔧 测试配置...")
    if config.validate():
        config.print_config()
        return True
    else:
        print("❌ 配置验证失败")
        return False


def test_ocr_initialization():
    """测试OCR服务初始化"""
    print("\n🚀 测试OCR服务初始化...")
    try:
        ocr = OCRService()
        print("✅ OCR服务初始化成功")
        return ocr
    except Exception as e:
        print(f"❌ OCR服务初始化失败: {e}")
        return None


def test_image_processing():
    """测试图片处理功能"""
    print("\n🖼️  测试图片处理功能...")
    
    # 查找测试图片
    test_images = [
        Path("test_image.jpg"),
        Path("test_image.png"),
        Path("test_image.jpeg"),
    ]
    
    test_image = None
    for img_path in test_images:
        if img_path.exists():
            test_image = img_path
            break
    
    if not test_image:
        print("⚠️  未找到测试图片，跳过图片处理测试")
        print("   请将测试图片命名为 test_image.jpg/png/jpeg")
        return False
    
    print(f"📷 找到测试图片: {test_image}")
    
    # 测试OCR服务
    ocr = test_ocr_initialization()
    if not ocr:
        return False
    
    try:
        print("🔍 开始识别图片...")
        result = ocr.recognize_receipt(test_image)
        
        print("📊 识别结果:")
        print(f"   是否为交易记录: {result.is_receipt}")
        if result.is_receipt:
            print(f"   支付平台: {result.platform}")
            print(f"   交易金额: {result.amount} {result.currency}")
            print(f"   交易时间: {result.transaction_time}")
            print(f"   商户名称: {result.merchant}")
            print(f"   置信度: {result.confidence}")
        print(f"   原始文本: {result.raw_text[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 图片识别失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🧪 ReceiptName OCR服务测试")
    print("=" * 50)
    
    # 测试配置
    if not test_config():
        return
    
    # 测试OCR初始化
    if not test_ocr_initialization():
        return
    
    # 测试图片处理
    test_image_processing()
    
    print("\n✅ 测试完成")


if __name__ == "__main__":
    main() 