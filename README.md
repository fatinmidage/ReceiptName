# ReceiptName - 智能交易记录重命名工具

> 🚀 **MVP版本** - 快速验证核心价值的最小可行产品

## 核心价值

ReceiptName 解决了一个简单但常见的问题：**自动识别交易记录图片并提取金额进行重命名**。

不再需要手动查看每张图片来重命名文件，让文件管理更高效。

## 快速开始

### 1. 安装
```bash
# 克隆项目
git clone <repository-url>
cd ReceiptName

# 安装依赖
uv sync
```

### 2. 配置
```bash
# 复制环境变量模板
cp env.example .env

# 编辑 .env 文件，添加火山引擎方舟API配置
ARK_API_KEY=your_ark_api_key_here
ARK_MODEL_ID=your_model_id_here
```

#### 获取火山引擎配置
1. **获取 API Key**：
   - 访问[方舟控制台-API Key 管理](URL_placeholder)
   - 创建新的 API Key
   - 复制到 `.env` 文件的 `ARK_API_KEY` 字段

2. **获取模型 ID**：
   - 访问[模型列表](URL_placeholder)
   - 选择合适的OCR模型
   - 复制模型ID到 `.env` 文件的 `ARK_MODEL_ID` 字段

### 3. 使用
```bash
# 在当前目录运行
python main.py
```

## 核心功能

### ✅ MVP功能（已实现）
- [x] 配置管理模块
- [x] 环境变量验证
- [ ] 扫描当前目录下的图片文件
- [ ] 识别微信支付、支付宝交易记录
- [ ] 提取交易金额
- [ ] 重命名为"金额_支付凭证"格式

### 🔄 即将实现
- OCR服务集成
- 交易记录识别
- 文件重命名
- 支持更多交易类型（信用卡、银行转账）
- 批量文件夹处理
- 处理进度显示

## 使用示例

**处理前：**
```
IMG_001.jpg  (微信支付 128.50元)
IMG_002.png  (支付宝 56.80元)
IMG_003.jpeg (普通照片)
```

**处理后：**
```
128.50元_支付凭证.jpg
56.80元_支付凭证.png
IMG_003.jpeg  (保持不变)
```

## 技术栈

- **Python 3.13+** - 核心语言
- **火山引擎方舟 ARK** - OCR识别服务
- **Pillow** - 图像处理

## 开发状态

- [x] 项目基础架构
- [x] 依赖配置
- [x] 配置管理模块
- [x] 环境变量验证
- [ ] OCR服务集成
- [ ] 交易记录识别
- [ ] 文件重命名
- [ ] 错误处理

## 配置说明

### 环境变量
| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `ARK_API_KEY` | 火山引擎方舟API Key | ✅ | - |
| `ARK_MODEL_ID` | 模型ID | ✅ | - |
| `LOG_LEVEL` | 日志级别 | ❌ | INFO |
| `MAX_RETRIES` | 最大重试次数 | ❌ | 3 |
| `RETRY_DELAY` | 重试延迟（秒） | ❌ | 1 |

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License