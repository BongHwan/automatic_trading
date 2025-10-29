import datetime
from .model import ModelSetting
from .notifier import send_telegram_message

history_db = []

class LogicNormal:

    @staticmethod
    def execute_trade(symbol, side, amount, leverage, price):
        mode = ModelSetting.get('basic_mode')
        record = {
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'symbol': symbol,
            'side': side,
            'amount': amount,
            'leverage': leverage,
            'price': price,
            'mode': mode
        }
        history_db.append(record)
        send_telegram_message(f"[{mode}] {side} {symbol} {amount} @ {price}")

    @staticmethod
    def get_history():
        now = datetime.datetime.now()
        last_24h = [h for h in history_db if datetime.datetime.strptime(h['time'], "%Y-%m-%d %H:%M:%S") > now - datetime.timedelta(hours=24)]
        return last_24h
