"""
ReceiptName 配置管理模块
按照MVP原则，提供基础的环境变量配置功能
支持 PyInstaller 封装后的配置文件读取
"""

import os
import sys
from typing import Optional
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    # 如果python-dotenv未安装，使用简单的解析方法作为fallback
    def load_dotenv(dotenv_path=None, override=False):
        """简单的.env文件加载函数"""
        env_file = Path(dotenv_path or ".env")
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        # 只有当 override=True 或者环境变量不存在时才设置
                        if override or key not in os.environ:
                            os.environ[key] = value


def get_executable_dir():
    """获取可执行文件所在目录"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 封装后的情况
        return Path(sys.executable).parent
    else:
        # 开发环境
        return Path(__file__).parent


class Config:
    """配置管理类"""
    
    def __init__(self):
        self._load_env_file()
    
    def _load_env_file(self):
        """加载 .env 文件（如果存在）
        优先级：
        - PyInstaller 打包环境：可执行文件目录 > 当前工作目录 > 脚本所在目录
        - 开发环境：当前工作目录 > 可执行文件目录 > 脚本所在目录
        """
        # 判断是否为 PyInstaller 打包环境
        if getattr(sys, 'frozen', False):
            # PyInstaller 打包环境：优先使用可执行文件目录
            possible_paths = [
                get_executable_dir() / ".env",  # 可执行文件目录（最高优先级）
                Path.cwd() / ".env",  # 当前工作目录
                Path(__file__).parent / ".env",  # 脚本所在目录
            ]
        else:
            # 开发环境：优先使用当前工作目录
            possible_paths = [
                Path.cwd() / ".env",  # 当前工作目录（最高优先级）
                get_executable_dir() / ".env",  # 可执行文件目录
                Path(__file__).parent / ".env",  # 脚本所在目录
            ]
        
        # 尝试加载第一个存在的 .env 文件
        for env_path in possible_paths:
            if env_path.exists():
                print(f"📁 加载配置文件：{env_path}")
                load_dotenv(env_path, override=True)  # 强制覆盖已存在的环境变量
                break
        else:
            print("⚠️  未找到 .env 配置文件，将使用环境变量")
    
    @property
    def ark_api_key(self) -> Optional[str]:
        """获取火山引擎方舟 API Key"""
        return os.environ.get("ARK_API_KEY")
    
    @property
    def ark_model_id(self) -> Optional[str]:
        """获取模型 ID"""
        return os.environ.get("ARK_MODEL_ID")
    
    @property
    def log_level(self) -> str:
        """获取日志级别，默认为 INFO"""
        return os.environ.get("LOG_LEVEL", "INFO")
    
    @property
    def max_retries(self) -> int:
        """获取最大重试次数，默认为 3"""
        return int(os.environ.get("MAX_RETRIES", "3"))
    
    @property
    def retry_delay(self) -> int:
        """获取重试延迟（秒），默认为 1"""
        return int(os.environ.get("RETRY_DELAY", "1"))
    
    def validate(self) -> bool:
        """验证必要的配置项"""
        if not self.ark_api_key:
            print("❌ 错误：未设置 ARK_API_KEY 环境变量")
            print("   请参考 env.example 文件进行配置")
            print(f"   配置文件应放在：{get_executable_dir() / '.env'}")
            return False
        
        if not self.ark_model_id:
            print("❌ 错误：未设置 ARK_MODEL_ID 环境变量")
            print("   请参考 env.example 文件进行配置")
            print(f"   配置文件应放在：{get_executable_dir() / '.env'}")
            return False
        
        print("✅ 配置验证通过")
        return True
    
    def print_config(self):
        """打印当前配置（隐藏敏感信息）"""
        print("📋 当前配置：")
        print(f"   可执行文件目录：{get_executable_dir()}")
        print(f"   ARK_API_KEY: {'*' * 8 + self.ark_api_key[-4:] if self.ark_api_key else '未设置'}")
        print(f"   ARK_MODEL_ID: {self.ark_model_id or '未设置'}")
        print(f"   LOG_LEVEL: {self.log_level}")
        print(f"   MAX_RETRIES: {self.max_retries}")
        print(f"   RETRY_DELAY: {self.retry_delay}")


# 全局配置实例
config = Config()
