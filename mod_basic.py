# mod_basic.py
import traceback, os, time
from flask import render_template, jsonify, request
from plugin import PluginModuleBase
from .setup import *
from .trading_engine import TradingEngine
from .notifier import send_telegram_message
from .model import ModelSetting

class ModuleBasic(PluginModuleBase):

    def __init__(self, P):
        super().__init__(P, name='basic', first_menu='setting', scheduler_desc="자동 트레이딩")
        
        self.db_default = {
            'db_version': '1',
            f'{self.name}_auto_start': 'False',
            f'{self.name}_interval': '0 */1 * * *',
            f'{self.name}_trade_amount_percent': 10,
            f'{self.name}_leverage': 1,
            f'{self.name}_take_profit_percent': 1,
            f'{self.name}_stop_loss_percent': 1,
            f'{self.name}_max_holding_minutes': 60,
            f'{self.name}_mode': 'simulation',
            f'{self.name}_telegram_enabled': False,
            f'{self.name}_telegram_api_key': '',
            f'{self.name}_telegram_chat_id': '',
        }

    def process_menu(self, sub, req):
        """UI 렌더링 시 설정값과 스케줄러 상태 전달"""
        arg = P.ModelSetting.to_dict()
        if sub == 'setting':
            # 스케줄러 상태 반영 (lotto 모듈처럼)
            arg['is_include'] = F.scheduler.is_include(self.get_scheduler_name()) if 'F' in globals() else False
            arg['is_running'] = F.scheduler.is_running(self.get_scheduler_name()) if 'F' in globals() else False
        return render_template(f'{P.package_name}_{self.name}_{sub}.html', arg=arg)

    def process_command(self, command, arg1, arg2, arg3, req):
        """UI에서 명령 처리 (테스트 트레이딩)"""
        ret = {'ret': 'success'}
        try:
            engine = TradingEngine(P)
            if command == 'test_trade':
                result = engine.test_trade()
                ret['data'] = result
                ret['modal'] = f"시뮬레이션 결과: {result}"
            elif command == 'save_settings':
                # 설정 저장 처리
                for key, value in req.form.items():
                    if key in ['scheduler', 'is_running']:
                        continue
                    ModelSetting.set(key, value)
                ret['modal'] = "설정이 저장되었습니다."
        except Exception as e:
            ret['ret'] = 'fail'
            ret['modal'] = str(e)
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
        return jsonify(ret)

    def scheduler_function(self):
        """자동 트레이딩 스케줄러 실행"""
        try:
            auto_start = P.ModelSetting.get_bool(f'{self.name}_auto_start')
            if not auto_start:
                return

            engine = TradingEngine(P)
            result = engine.execute_trade()
            msg = f"자동 트레이딩 실행 결과\n{result}"

            # Telegram 전송
            send_telegram_message(msg)

        except Exception as e:
            P.logger.error(f'Exception:{str(e)}')
            P.logger.error(traceback.format_exc())
