from .model import ModelSetting
from .logic_normal import LogicNormal

class TradingEngine:

    def __init__(self, P):
        self.P = P

    def test_trade(self):
        return {"result": "테스트 트레이딩 완료"}

    def execute_trade(self):
        symbol = "BTCUSDT"
        side = "BUY"
        amount = float(ModelSetting.get('basic_trade_amount_percent') or 10)
        leverage = int(ModelSetting.get('basic_leverage') or 1)
        price = 50000
        LogicNormal.execute_trade(symbol, side, amount, leverage, price)
        return f"{side} {symbol} {amount} @ {price}"
