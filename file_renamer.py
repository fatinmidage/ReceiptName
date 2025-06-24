"""
文件重命名模块
根据交易记录信息重命名图片文件
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, List

from models import ReceiptInfo

logger = logging.getLogger(__name__)


class FileRenamer:
    """文件重命名器"""
    
    def __init__(self, target_directory: Optional[Path] = None):
        """
        初始化文件重命名器
        
        Args:
            target_directory: 目标目录，默认为当前工作目录
        """
        self.target_directory = target_directory or Path.cwd()
        logger.info(f"文件重命名器初始化，目标目录: {self.target_directory}")
    
    def generate_new_filename(self, receipt_info: ReceiptInfo, original_filename: str) -> str:
        """
        根据交易记录信息生成新的文件名
        
        Args:
            receipt_info: 交易记录信息
            original_filename: 原始文件名
            
        Returns:
            新的文件名
        """
        # 获取原始文件的扩展名
        original_path = Path(original_filename)
        extension = original_path.suffix.lower()
        
        # 如果不是交易记录，保持原文件名
        if not receipt_info.is_receipt:
            logger.debug(f"非交易记录，保持原文件名: {original_filename}")
            return original_filename
        
        # 如果没有金额信息，使用"未知金额"
        if receipt_info.amount is None:
            amount_str = "未知金额"
        else:
            # 格式化金额，保留2位小数
            amount_str = f"{receipt_info.amount:.2f}元"
        
        # 构建基础文件名：金额_支付凭证
        base_name = f"{amount_str}_支付凭证"
        
        # 构建最终文件名
        final_name = f"{base_name}{extension}"
        
        logger.info(f"生成新文件名: {original_filename} -> {final_name}")
        return final_name
    
    def rename_file(self, original_path: Path, receipt_info: ReceiptInfo) -> Optional[Path]:
        """
        重命名单个文件
        
        Args:
            original_path: 原始文件路径
            receipt_info: 交易记录信息
            
        Returns:
            新的文件路径，如果重命名失败则返回None
        """
        try:
            # 检查原始文件是否存在
            if not original_path.exists():
                logger.error(f"原始文件不存在: {original_path}")
                return None
            
            # 生成新文件名
            new_filename = self.generate_new_filename(receipt_info, original_path.name)
            new_path = original_path.parent / new_filename
            
            # 如果新文件名与原文件名相同，不需要重命名
            if new_filename == original_path.name:
                logger.info(f"文件名无需更改: {original_path.name}")
                return original_path
            
            # 检查目标文件是否已存在，如果存在则添加序号
            counter = 1
            base_new_path = new_path
            while new_path.exists():
                stem = base_new_path.stem
                suffix = base_new_path.suffix
                new_path = base_new_path.parent / f"{stem}_{counter:02d}{suffix}"
                counter += 1
                
                # 防止无限循环
                if counter > 999:
                    logger.error(f"无法找到可用的文件名: {base_new_path}")
                    return None
            
            # 执行重命名
            original_path.rename(new_path)
            logger.info(f"文件重命名成功: {original_path.name} -> {new_path.name}")
            return new_path
            
        except Exception as e:
            logger.error(f"重命名文件失败 {original_path}: {e}")
            return None
    
    def batch_rename(self, rename_tasks: Dict[Path, ReceiptInfo]) -> Dict[Path, Optional[Path]]:
        """
        批量重命名文件
        
        Args:
            rename_tasks: 重命名任务字典，键为原始文件路径，值为交易记录信息
            
        Returns:
            重命名结果字典，键为原始文件路径，值为新文件路径（失败时为None）
        """
        results = {}
        success_count = 0
        
        logger.info(f"开始批量重命名，共 {len(rename_tasks)} 个文件")
        
        for original_path, receipt_info in rename_tasks.items():
            new_path = self.rename_file(original_path, receipt_info)
            results[original_path] = new_path
            
            if new_path is not None:
                success_count += 1
        
        logger.info(f"批量重命名完成，成功: {success_count}/{len(rename_tasks)}")
        return results
    
    def get_supported_image_files(self, directory: Optional[Path] = None) -> List[Path]:
        """
        获取目录中支持的图片文件列表
        
        Args:
            directory: 要扫描的目录，默认为target_directory
            
        Returns:
            图片文件路径列表
        """
        scan_directory = directory or self.target_directory
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
        
        image_files = []
        for file_path in scan_directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                image_files.append(file_path)
        
        logger.info(f"在 {scan_directory} 中找到 {len(image_files)} 个图片文件")
        return sorted(image_files)


def test_file_renamer():
    """测试文件重命名器功能"""
    print("--- 测试文件重命名器 ---")
    
    # 创建测试目录
    test_dir = Path("test_rename")
    test_dir.mkdir(exist_ok=True)
    
    try:
        renamer = FileRenamer(test_dir)
        
        # 测试用例1: 生成新文件名 - 微信支付
        receipt1 = ReceiptInfo(
            is_receipt=True,
            platform="微信支付",
            amount=123.45,
            confidence=0.9,
            raw_text="微信支付收款123.45元"
        )
        new_name1 = renamer.generate_new_filename(receipt1, "IMG_001.jpg")
        print(f"测试1 - 微信支付文件名: {new_name1}")
        assert "123.45元" in new_name1
        assert "支付凭证" in new_name1
        assert new_name1.endswith(".jpg")
        
        # 测试用例2: 生成新文件名 - 支付宝
        receipt2 = ReceiptInfo(
            is_receipt=True,
            platform="支付宝",
            amount=88.00,
            confidence=0.95,
            raw_text="支付宝收款88.00元"
        )
        new_name2 = renamer.generate_new_filename(receipt2, "photo.png")
        print(f"测试2 - 支付宝文件名: {new_name2}")
        assert "88.00元" in new_name2
        assert "支付凭证" in new_name2
        assert new_name2.endswith(".png")
        
        # 测试用例3: 非交易记录
        receipt3 = ReceiptInfo(
            is_receipt=False,
            confidence=0.8,
            raw_text="这是一张风景照片"
        )
        new_name3 = renamer.generate_new_filename(receipt3, "landscape.jpg")
        print(f"测试3 - 非交易记录文件名: {new_name3}")
        assert new_name3 == "landscape.jpg"
        
        # 测试用例4: 无金额信息
        receipt4 = ReceiptInfo(
            is_receipt=True,
            platform="微信支付",
            amount=None,
            confidence=0.7,
            raw_text="微信支付收款凭证"
        )
        new_name4 = renamer.generate_new_filename(receipt4, "receipt.jpg")
        print(f"测试4 - 无金额信息文件名: {new_name4}")
        assert "未知金额" in new_name4
        assert "支付凭证" in new_name4
        
        print("✅ 所有测试用例通过！")
        
    finally:
        # 清理测试目录
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir)


if __name__ == '__main__':
    # 配置日志以查看详细信息
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    test_file_renamer() 