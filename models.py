"""
数据模型模块
定义项目中使用的Pydantic数据模型
"""

from typing import Optional
from pydantic import BaseModel, Field


class ReceiptInfo(BaseModel):
    """交易记录信息结构"""
    is_receipt: bool = Field(description="是否为交易记录")
    platform: Optional[str] = Field(description="支付平台（微信支付/支付宝/其他）", default=None)
    amount: Optional[float] = Field(description="交易金额（元）", default=None)
    currency: str = Field(description="货币单位", default="元")
    transaction_time: Optional[str] = Field(description="交易时间", default=None)
    merchant: Optional[str] = Field(description="商户名称", default=None)
    confidence: float = Field(description="识别置信度（0-1）")
    raw_text: str = Field(description="识别的原始文本") 