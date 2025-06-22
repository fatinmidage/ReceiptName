# OCR服务使用示例

本文档展示如何使用 `ocr_service.py` 模块进行交易记录识别。

## 基础使用

### 1. 初始化OCR服务

```python
from ocr_service import OCRService
from pathlib import Path

# 初始化OCR服务
ocr = OCRService()
```

### 2. 识别单张图片

```python
# 识别交易记录图片
image_path = Path("receipt.jpg")
result = ocr.recognize_receipt(image_path)

# 查看识别结果
print(f"是否为交易记录: {result.is_receipt}")
if result.is_receipt:
    print(f"支付平台: {result.platform}")
    print(f"交易金额: {result.amount} {result.currency}")
    print(f"交易时间: {result.transaction_time}")
    print(f"商户名称: {result.merchant}")
    print(f"置信度: {result.confidence}")
print(f"原始文本: {result.raw_text}")
```

### 3. 批量识别图片

```python
# 批量识别多张图片
image_paths = [
    Path("receipt1.jpg"),
    Path("receipt2.png"),
    Path("receipt3.jpeg"),
]

results = ocr.batch_recognize(image_paths)

# 处理结果
for image_path, result in results.items():
    print(f"\n图片: {image_path.name}")
    print(f"识别结果: {result.is_receipt}")
    if result.is_receipt:
        print(f"金额: {result.amount} {result.currency}")
```

## 结构化输出

OCR服务使用Pydantic模型进行结构化输出，确保返回数据的类型安全：

```python
from ocr_service import ReceiptInfo

# ReceiptInfo 模型结构
class ReceiptInfo(BaseModel):
    is_receipt: bool                    # 是否为交易记录
    platform: Optional[str]             # 支付平台
    amount: Optional[float]             # 交易金额
    currency: str                       # 货币单位
    transaction_time: Optional[str]     # 交易时间
    merchant: Optional[str]             # 商户名称
    confidence: float                   # 识别置信度
    raw_text: str                       # 原始文本
```

## 错误处理

OCR服务包含完善的错误处理机制：

```python
try:
    result = ocr.recognize_receipt(image_path)
    if result.is_receipt:
        print(f"识别成功: {result.amount}元")
    else:
        print("不是交易记录")
except FileNotFoundError:
    print("图片文件不存在")
except Exception as e:
    print(f"识别失败: {e}")
```

## 配置选项

OCR服务支持以下配置选项（通过环境变量或.env文件设置）：

```bash
# 必需配置
ARK_API_KEY=your_api_key_here
ARK_MODEL_ID=your_model_id_here

# 可选配置
LOG_LEVEL=INFO                    # 日志级别
MAX_RETRIES=3                     # 最大重试次数
RETRY_DELAY=1                     # 重试延迟（秒）
```

## 测试

运行测试脚本验证OCR服务：

```bash
# 运行测试
python test_ocr.py

# 或者直接测试OCR服务
python ocr_service.py
```

## 支持的图片格式

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)
- BMP (.bmp)

## 性能优化

1. **批量处理**：使用 `batch_recognize()` 方法进行批量处理
2. **重试机制**：自动重试失败的请求
3. **延迟控制**：批量处理时自动添加延迟避免API限制
4. **高分辨率模式**：使用 `detail: "high"` 提高识别精度

## 注意事项

1. 确保已正确配置火山引擎API密钥和模型ID
2. 图片文件必须存在且可读
3. 网络连接稳定，避免API调用失败
4. 大量图片处理时注意API调用频率限制 