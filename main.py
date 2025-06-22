"""
ReceiptName 主程序
按照MVP原则，提供基础的配置验证功能
"""

from config import config


def main():
    """主程序入口"""
    print("🧾 ReceiptName - 交易记录文件重命名工具")
    print("=" * 50)
    
    # 验证配置
    if not config.validate():
        print("\n📝 配置说明：")
        print("1. 复制 env.example 为 .env")
        print("2. 在 .env 中填入您的火山引擎 API Key 和模型 ID")
        print("3. 重新运行程序")
        return
    
    # 显示当前配置
    config.print_config()
    
    print("\n✅ 配置就绪，准备进行下一步开发...")
    print("   下一步：OCR服务集成")


if __name__ == "__main__":
    main()
