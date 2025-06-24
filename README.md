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

### 3. 测试
```bash
# 测试OCR服务
python test_ocr.py
```

### 4. 使用
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
- [x] 批量处理功能
- [x] 交易记录识别算法
- [x] 金额提取功能
- [x] OCR测试脚本

### 🔄 开发中功能
- [ ] 扫描当前目录下的图片文件
- [ ] 文件重命名为"金额_支付凭证"格式
- [ ] 主程序集成和用户交互

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
- **Pydantic** - 数据验证和结构化输出
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
- [x] 批量处理功能
- [x] 交易记录识别算法
- [x] 金额提取功能
- [x] OCR测试脚本（test_ocr.py）
- [x] 测试图片准备

### 🔄 当前开发
- [ ] 文件重命名模块（file_renamer.py）
- [ ] 主程序集成和文件扫描逻辑
- [ ] 完整的用户交互流程

### 📋 下一步
- [ ] 功能测试
- [ ] 错误处理完善
- [ ] 性能优化
- [ ] 用户文档完善

## 技术特性

### 核心算法
- **智能识别** - 使用火山引擎方舟API进行高精度OCR识别
- **结构化输出** - 使用Pydantic模型确保结果一致性
- **交易判断** - 自动识别微信支付、支付宝等交易记录
- **金额提取** - 精确提取交易金额和相关信息

### 可靠性保障
- **重试机制** - 自动处理API调用失败
- **错误处理** - 完善的异常处理和日志记录
- **批量处理** - 支持多图片同时处理
- **配置验证** - 启动时验证所有必要配置

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

### 测试OCR服务
```bash
# 运行OCR测试
python test_ocr.py
```

## 示例代码

项目包含火山引擎方舟的使用示例：
- `示例代码/大模型快速入门.md` - 基础API调用
- `示例代码/大模型Base64 编码输入.md` - 图片输入处理
- `示例代码/大模型结构化输出.md` - 结构化输出处理

## 项目结构

```
ReceiptName/
├── main.py                 # 主程序入口
├── config.py               # 配置管理
├── ocr_service.py          # OCR服务 ✅
├── models.py               # 数据模型 ✅
├── receipt_detector.py     # 交易记录检测 ✅
├── test_ocr.py             # OCR测试脚本 ✅
├── file_renamer.py         # 文件重命名
├── pyproject.toml          # 项目配置
├── README.md              # 项目文档
├── env.example            # 环境变量示例
├── pyinstaller_config.spec # 打包配置
├── test_image.jpeg        # 测试图片 ✅
└── 示例代码/              # 火山引擎示例
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License