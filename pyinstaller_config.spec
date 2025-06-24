# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('env.example', '.'),  # 将示例配置文件打包到可执行文件目录
    ],
    hiddenimports=[
        # 环境变量和配置相关
        'dotenv',
        'pathlib',
        'typing',
        # Pydantic相关
        'pydantic',
        'pydantic.fields',
        'pydantic.main',
        'pydantic.types',
        # 火山引擎SDK相关
        'volcenginesdkarkruntime',
        'volcenginesdkcore',
        # 图像处理相关
        'PIL',
        'PIL.Image',
        'PIL.ImageFile',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        # 编码相关
        'base64',
        'json',
        # 日志相关
        'logging',
        'logging.handlers',
        # 系统和文件相关
        'sys',
        'os',
        'pathlib',
        'time',
        # 类型注解相关
        'typing_extensions',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ReceiptName',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 保留控制台输出，方便调试
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
) 