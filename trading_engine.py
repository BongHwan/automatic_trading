from .model import ModelSetting
from .logic_normal import LogicNormal

class TradingEngine:

    def __init__(self, P):
        self.P = P

    def test_trade(self):
        # 테스트용 시뮬레이션
        return {"result": "테스트 트레이딩 완료"}

    def execute_trade(self):
        # 실제 트레이딩 또는 시뮬레이션
        symbol = "BTCUSDT"
        side = "BUY"
        amount = float(ModelSetting.get('basic_trade_amount_percent') or 10)
        leverage = int(ModelSetting.get('basic_leverage') or 1)
        price = 50000  # 예시 가격
        LogicNormal.execute_trade(symbol, side, amount, leverage, price)
        return f"{side} {symbol} {amount} @ {price}"
