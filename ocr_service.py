"""
ReceiptName OCR服务模块
使用火山引擎方舟API进行图片识别，支持Base64编码输入和结构化输出
"""

import base64
import logging
import time
from pathlib import Path
from typing import Dict, Any, List

try:
    from volcenginesdkarkruntime import Ark
except ImportError:
    print("❌ 错误：未安装火山引擎方舟SDK")
    print("   请运行：pip install volcengine-python-sdk[ark]")
    raise

from config import config
from models import ReceiptInfo

# 配置日志
logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)


class OCRService:
    """OCR服务类"""
    
    def __init__(self):
        """初始化OCR服务"""
        self.client = Ark(api_key=config.ark_api_key)
        self.model_id = config.ark_model_id
        self.max_retries = config.max_retries
        self.retry_delay = config.retry_delay
        
        logger.info(f"OCR服务初始化完成，模型ID: {self.model_id}")
    
    def encode_image(self, image_path: Path) -> str:
        """将图片转换为Base64编码"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"图片编码失败 {image_path}: {e}")
            raise
    
    def get_image_format(self, image_path: Path) -> str:
        """获取图片格式"""
        suffix = image_path.suffix.lower()
        format_map = {
            '.jpg': 'jpeg',
            '.jpeg': 'jpeg',
            '.png': 'png',
            '.gif': 'gif',
            '.webp': 'webp',
            '.bmp': 'bmp'
        }
        return format_map.get(suffix, 'jpeg')
    
    def create_base64_url(self, base64_image: str, image_format: str) -> str:
        """创建Base64编码的图片URL"""
        return f"data:image/{image_format};base64,{base64_image}"
    
    def recognize_receipt(self, image_path: Path) -> ReceiptInfo:
        """识别交易记录图片"""
        logger.info(f"开始识别图片: {image_path}")
        
        # 验证文件存在
        if not image_path.exists():
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        # 编码图片
        base64_image = self.encode_image(image_path)
        image_format = self.get_image_format(image_path)
        image_url = self.create_base64_url(base64_image, image_format)
        
        # 构建提示词
        prompt = """
请分析这张图片，判断是否为交易记录（如微信支付、支付宝等），并提取相关信息。

如果是交易记录，请提取以下信息：
- 支付平台（微信支付/支付宝/其他）
- 交易金额
- 交易时间
- 商户名称

如果不是交易记录，请将is_receipt设为false，其他字段设为null。

请仔细分析图片中的所有文字内容，确保信息准确。
"""
        
        # 重试机制
        for attempt in range(self.max_retries):
            try:
                logger.info(f"OCR识别尝试 {attempt + 1}/{self.max_retries}")
                
                # 调用火山引擎API
                completion = self.client.beta.chat.completions.parse(
                    model=self.model_id,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": image_url,
                                        "detail": "high"  # 使用高分辨率模式
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ],
                    response_format=ReceiptInfo,  # 使用结构化输出
                    extra_body={
                        "thinking": {
                            "type": "disabled"  # 不使用深度思考能力
                        }
                    }
                )
                
                # 提取结果
                result = completion.choices[0].message.parsed
                logger.info(f"OCR识别成功: {result.is_receipt}")
                return result
                
            except Exception as e:
                logger.warning(f"OCR识别失败 (尝试 {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"OCR识别最终失败: {e}")
                    # 返回默认结果
                    return ReceiptInfo(
                        is_receipt=False,
                        confidence=0.0,
                        raw_text="识别失败"
                    )
    
    def batch_recognize(self, image_paths: List[Path]) -> Dict[Path, ReceiptInfo]:
        """批量识别图片"""
        results = {}
        total = len(image_paths)
        
        logger.info(f"开始批量识别 {total} 张图片")
        
        for i, image_path in enumerate(image_paths, 1):
            try:
                logger.info(f"处理进度: {i}/{total} - {image_path.name}")
                result = self.recognize_receipt(image_path)
                results[image_path] = result
                
                # 添加延迟避免API限制
                if i < total:
                    time.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"处理图片失败 {image_path}: {e}")
                results[image_path] = ReceiptInfo(
                    is_receipt=False,
                    confidence=0.0,
                    raw_text=f"处理失败: {str(e)}"
                )
        
        logger.info(f"批量识别完成，成功处理 {len(results)} 张图片")
        return results


def test_ocr_service():
    """测试OCR服务"""
    try:
        ocr = OCRService()
        print("✅ OCR服务初始化成功")
        
        # 测试图片路径（需要实际存在的图片）
        test_image = Path("/Users/wuyingheng/项目/ReceiptName/IMG_F56683927094-1.jpeg")
        if test_image.exists():
            result = ocr.recognize_receipt(test_image)
            print(f"测试结果: {result.model_dump_json(indent=2)}")
        else:
            print("⚠️  测试图片不存在，跳过测试")
            
    except Exception as e:
        print(f"❌ OCR服务测试失败: {e}")


if __name__ == "__main__":
    test_ocr_service() 