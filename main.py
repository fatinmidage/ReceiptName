"""
ReceiptName 主程序
交易记录图片识别和自动重命名工具
"""

import logging
from pathlib import Path
from typing import Dict, List

from config import config, get_executable_dir
from ocr_service import OCRService
from file_renamer import FileRenamer
from models import ReceiptInfo

# 配置日志
logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)


def print_banner():
    """打印程序横幅"""
    print("🧾 ReceiptName - 交易记录文件重命名工具")
    print("=" * 50)
    print("📋 功能：自动识别交易记录并重命名文件")
    print("💰 支持：微信支付、支付宝等交易凭证")
    print("=" * 50)


def print_statistics(results: Dict[Path, ReceiptInfo], rename_results: Dict[Path, Path]):
    """打印处理统计信息"""
    total_files = len(results)
    receipt_count = sum(1 for info in results.values() if info.is_receipt)
    renamed_count = sum(1 for new_path in rename_results.values() if new_path is not None)
    
    print("\n📊 处理统计")
    print("=" * 30)
    print(f"总文件数量: {total_files}")
    print(f"识别为交易记录: {receipt_count}")
    print(f"成功重命名: {renamed_count}")
    print(f"识别成功率: {receipt_count/total_files*100:.1f}%" if total_files > 0 else "识别成功率: 0%")
    print(f"重命名成功率: {renamed_count/receipt_count*100:.1f}%" if receipt_count > 0 else "重命名成功率: 0%")


def print_details(results: Dict[Path, ReceiptInfo], rename_results: Dict[Path, Path]):
    """打印详细处理结果"""
    print("\n📋 详细结果")
    print("=" * 50)
    
    for original_path, receipt_info in results.items():
        new_path = rename_results.get(original_path)
        
        if receipt_info.is_receipt:
            status = "✅ 交易记录"
            amount_str = f"{receipt_info.amount:.2f}元" if receipt_info.amount else "未知金额"
            platform = receipt_info.platform or "未知平台"
            
            if new_path and new_path != original_path:
                print(f"{status} | {original_path.name}")
                print(f"    💰 金额: {amount_str} | 🏪 平台: {platform}")
                print(f"    📝 重命名: {new_path.name}")
                print(f"    🎯 置信度: {receipt_info.confidence:.2f}")
            else:
                print(f"{status} | {original_path.name}")
                print(f"    💰 金额: {amount_str} | 🏪 平台: {platform}")
                print(f"    ⚠️  重命名失败或无需重命名")
                print(f"    🎯 置信度: {receipt_info.confidence:.2f}")
        else:
            print(f"❌ 非交易记录 | {original_path.name}")
            print(f"    🎯 置信度: {receipt_info.confidence:.2f}")
        
        print()


def main():
    """主程序入口"""
    print_banner()
    
    # 验证配置
    if not config.validate():
        print("\n❌ 配置验证失败")
        print("\n📝 配置说明：")
        print("1. 复制 env.example 为 .env")
        print("2. 在 .env 中填入您的火山引擎 API Key 和模型 ID")
        print("3. 重新运行程序")
        return
    
    # 显示当前配置
    config.print_config()
    
    try:
        # 获取可执行文件所在目录作为工作目录
        work_directory = get_executable_dir()
        
        # 初始化服务
        print("\n🔧 初始化服务...")
        ocr_service = OCRService()
        file_renamer = FileRenamer(target_directory=work_directory)
        
        # 扫描图片文件
        print("\n📂 扫描图片文件...")
        image_files = file_renamer.get_supported_image_files()
        
        if not image_files:
            print("⚠️  当前目录下没有找到支持的图片文件")
            print("支持的格式: .jpg, .jpeg, .png, .bmp, .gif, .tiff, .webp")
            print(f"📁 扫描目录: {work_directory}")
            return
        
        print(f"✅ 找到 {len(image_files)} 个图片文件")
        
        # 显示找到的文件
        print("\n📄 发现的图片文件:")
        for i, img_path in enumerate(image_files, 1):
            print(f"  {i}. {img_path.name}")
        
        print(f"\n🚀 开始处理 {len(image_files)} 个文件...")
        
        # OCR识别
        print("\n🔍 开始OCR识别...")
        ocr_results = ocr_service.batch_recognize(image_files)
        
        # 过滤出交易记录
        receipt_files = {path: info for path, info in ocr_results.items() if info.is_receipt}
        
        if not receipt_files:
            print("⚠️  没有识别到交易记录")
            print_statistics(ocr_results, {})
            return
        
        print(f"✅ 识别到 {len(receipt_files)} 个交易记录")
        
        # 文件重命名
        print(f"\n📝 开始重命名 {len(receipt_files)} 个交易记录文件...")
        rename_results = file_renamer.batch_rename(receipt_files)
        
        # 显示结果
        print_statistics(ocr_results, rename_results)
        print_details(ocr_results, rename_results)
        
        print("🎉 处理完成！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断操作")
    except Exception as e:
        logger.error(f"程序执行出错: {e}")
        print(f"\n❌ 程序执行出错: {e}")
        print("请检查日志文件获取详细错误信息")


if __name__ == "__main__":
    main()
