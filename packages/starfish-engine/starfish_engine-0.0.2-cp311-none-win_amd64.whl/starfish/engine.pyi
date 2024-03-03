from enum import Enum
from datetime import datetime
from typing import List, Optional, Tuple
from decimal import Decimal

class RunMode(Enum):
    """运行模式"""

    Backtest = RunMode
    """回测"""
    Sandbox = RunMode
    """模拟盘"""
    Live = RunMode
    """实盘"""

class TradeType(Enum):
    """交易类型"""

    Market = TradeType
    """市价交易"""
    Limit = TradeType
    """限价交易"""

class TradeSide(Enum):
    """交易方向"""

    Buy = TradeSide
    """买入"""
    Sell = TradeSide
    """卖出"""

class OrderStatus(Enum):
    """订单状态"""

    Preparing = OrderStatus
    """准备中"""
    PendingOrder = OrderStatus
    """挂单中"""
    Rejected = OrderStatus
    """订单被拒"""
    Fulled = OrderStatus
    """已完成"""
    Canceled = OrderStatus
    """已取消"""

class Order:
    """订单"""

    id: int
    """订单ID"""
    exid: str
    """交易所订单ID"""
    symbol: str
    """标的"""
    trade_type: TradeType
    """交易类型"""
    trade_side: TradeSide
    """交易方向"""
    time: datetime
    """下单时间"""
    status: OrderStatus
    """订单状态"""
    volume: Decimal
    """数量"""
    price: Decimal
    """价格"""
    amount: Decimal
    """金额"""
    average_price: Decimal
    """均价"""
    deal_volume: Decimal
    """成交数量"""
    deal_amount: Decimal
    """成交金额"""
    cost_volume: Decimal
    """手续费数量"""
    cost_amount: Decimal
    """手续费金额"""
    remark: str
    """备注"""

class Candle:
    """K线"""

    symbol: str
    """标的"""
    time: datetime
    """开盘时间"""
    open: Decimal
    """开盘价"""
    high: Decimal
    """最高价"""
    low: Decimal
    """最低价"""
    close: Decimal
    """收盘价"""
    volume: Decimal
    """成交量"""

class Pair:
    """交易对"""

    symbol: str
    """标的"""
    base: str
    """基础货币"""
    quote: str
    """计价货币"""
    take_fee_rate: Decimal
    """吃单费率"""
    maker_fee_rate: Decimal
    """挂单费率"""
    min_volume: Decimal
    """最小下单数量"""
    min_move_volume: Decimal
    """最小数量波动"""
    min_price: Decimal
    """最小下单金额"""
    min_move_price: Decimal
    """最小价格波动"""
    min_amount: Decimal
    """最小下单金额"""
    max_pending_order: int
    """最大挂单数量"""
    last_price: Decimal
    """最新成交价"""
    index_price: Decimal
    """指数价"""

class Cash:
    """资金"""

    code: str
    """资金代码"""
    total: Decimal
    """总资金"""
    available: Decimal
    """可用资金"""

def launcher(config: dict):
    """运行程序"""

def stop(msg: Optional[str] = None):
    """停止运行"""

def ts_to_date(ts: str) -> datetime:
    """时间戳转UTC时间"""

def str_to_date(s: str) -> datetime:
    """字符串转UTC时间"""

def uuid() -> int:
    """生成UUID"""

def debug(msg: str):
    """输出调试日志"""

def info(msg: str):
    """输出信息日志"""

def warn(msg: str):
    """输出警告日志"""

def error(msg: str):
    """输出错误日志"""

def current_trade_time() -> datetime:
    """获取当前交易时间"""

def get_pair(symbol: str) -> Pair:
    """获取交易对"""

def get_orders(symbol: str) -> List[Order]:
    """获取订单"""

def get_order(symbol: str, id: int) -> Order:
    """获取订单"""

def limit_buy(
    symbol: str,
    price: Decimal | str,
    volume: Decimal | str,
    remark: str = "",
) -> Optional[int]:
    """限价买入"""

def market_buy(
    symbol: str,
    amount: Decimal | str,
    remark: str = "",
) -> Optional[int]:
    """市价买入"""

def limit_sell(
    symbol: str,
    price: Decimal | str,
    volume: Decimal | str,
    remark: str = "",
) -> Optional[int]:
    """限价卖出"""

def market_sell(
    symbol: str,
    volume: Decimal | str,
    remark: str = "",
) -> Optional[int]:
    """市价卖出"""

def get_cash(code: str) -> Cash:
    """获取资金"""

def get_candles(
    symbol: str, limit: int = 1000
) -> List[Tuple[datetime, Decimal, Decimal, Decimal, Decimal, Decimal]]:
    """获取K线"""
