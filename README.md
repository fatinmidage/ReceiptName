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
   - 访问[方舟控制台-API Key 管理](https://console.volcengine.com/ark/key)
   - 创建新的 API Key
   - 复制到 `.env` 文件的 `ARK_API_KEY` 字段

2. **获取模型 ID**：
   - 访问[模型列表](https://console.volcengine.com/ark/model)
   - 选择合适的OCR模型（推荐：通用OCR模型）
   - 复制模型ID到 `.env` 文件的 `ARK_MODEL_ID` 字段

### 3. 使用
```bash
# 在当前目录运行
python main.py
```

## 核心功能

### ✅ 已完成功能
- [x] 配置管理模块
- [x] 环境变量验证
- [x] 多环境配置文件支持（开发/打包）
- [x] 基础项目架构
- [x] 依赖配置和代码质量工具
- [x] OCR服务集成（ocr_service.py）
- [x] 火山引擎方舟API调用
- [x] Base64编码图片输入
- [x] 结构化输出支持
- [x] 重试机制和错误处理

### 🔄 开发中功能
- [ ] 扫描当前目录下的图片文件
- [ ] 识别微信支付、支付宝交易记录
- [ ] 提取交易金额
- [ ] 重命名为"金额_支付凭证"格式

### 📋 计划功能
- 支持更多交易类型（信用卡、银行转账）
- 批量文件夹处理
- 处理进度显示
- 图形界面

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
- **python-dotenv** - 环境变量管理
- **PyInstaller** - 可执行文件打包

## 开发状态

### ✅ 已完成
- [x] 项目基础架构
- [x] 依赖配置（uv + pyproject.toml）
- [x] 配置管理模块（config.py）
- [x] 环境变量验证
- [x] 代码质量工具配置（black, isort, mypy, ruff）
- [x] 测试框架配置（pytest）
- [x] 打包配置（PyInstaller）
- [x] OCR服务集成（ocr_service.py）
- [x] 火山引擎方舟API调用
- [x] Base64编码图片输入
- [x] 结构化输出支持
- [x] 重试机制和错误处理

### 🔄 当前开发
- [ ] 交易记录识别（receipt_detector.py）
- [ ] 文件重命名（file_renamer.py）
- [ ] 主程序集成

### 📋 下一步
- [ ] 功能测试
- [ ] 错误处理完善
- [ ] 性能优化

## 配置说明

### 环境变量
| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `ARK_API_KEY` | 火山引擎方舟API Key | ✅ | - |
| `ARK_MODEL_ID` | 模型ID | ✅ | - |
| `LOG_LEVEL` | 日志级别 | ❌ | INFO |
| `MAX_RETRIES` | 最大重试次数 | ❌ | 3 |
| `RETRY_DELAY` | 重试延迟（秒） | ❌ | 1 |

### 配置文件优先级
1. 当前工作目录的 `.env`
2. 可执行文件目录的 `.env`
3. 脚本所在目录的 `.env`

## 开发指南

### 代码质量
项目配置了完整的代码质量工具：
- **Black** - 代码格式化
- **isort** - import排序
- **mypy** - 类型检查
- **ruff** - 快速linting
- **pytest** - 测试框架

### 运行代码质量检查
```bash
# 格式化代码
black .
isort .

# 类型检查
mypy .

# 代码检查
ruff check .

# 运行测试
pytest
```

## 示例代码

项目包含火山引擎方舟的使用示例：
- `示例代码/大模型快速入门.md` - 基础API调用
- `示例代码/大模型Base64 编码输入.md` - 图片输入处理
- `示例代码/大模型结构化输出.md` - 结构化输出处理

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License