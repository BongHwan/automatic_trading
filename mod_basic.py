# mod_basic.py
import traceback
from flask import render_template, jsonify
from plugin import PluginModuleBase
from .setup import *

import os
import time
from io import BytesIO

# Binance 연동 및 메시지 알림 라이브러리 예시
from .trading_engine import TradingEngine
from .tool import ToolNotify

class ModuleBasic(PluginModuleBase):

    def __init__(self, P):
        super(ModuleBasic, self).__init__(
            P, name='basic', first_menu='setting', scheduler_desc="자동 트레이딩"
        )

        self.db_default = {
            'db_version': '1',
            f'{self.name}_auto_start': 'False',
            f'{self.name}_interval': '0 */1 * * *',  # 예시: 1시간마다 실행
            f'{P.package_name}_trade_amount_percent': 10,
            f'{P.package_name}_leverage': 1,
            f'{P.package_name}_take_profit_percent': 1,
            f'{P.package_name}_stop_loss_percent': 1,
            f'{P.package_name}_max_holding_minutes': 60,
            f'{P.package_name}_mode': 'simulation',
            f'{P.package_name}_telegram_api_key': '',
            f'{P.package_name}_telegram_chat_id': '',
        }

    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        return render_template(f'{P.package_name}_{sub}.html', arg=arg)

    def process_command(self, command, arg1, arg2, arg3, req):
        ret = {'ret': 'success'}
        try:
            engine = TradingEngine(P)
            if command == 'test_trade':
                result = engine.test_trade()
                ret['data'] = result
                ret['modal'] = f"시뮬레이션 결과: {result}"
        except Exception as e:
            ret['ret'] = 'fail'
            ret['modal'] = str(e)
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
        return jsonify(ret)

    def scheduler_function(self):
        try:
            auto_start = P.ModelSetting.get_bool('basic_auto_start')
            if not auto_start:
                return

            engine = TradingEngine(P)
            result = engine.execute_trade()
            msg = f"자동 트레이딩 실행 결과\n{result}"
            
            telegram_key = P.ModelSetting.get('telegram_api_key')
            telegram_chat = P.ModelSetting.get('telegram_chat_id')
            if telegram_key and telegram_chat:
                ToolNotify.send_message(msg, 'trading', api_key=telegram_key, chat_id=telegram_chat)

        except Exception as e:
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())

