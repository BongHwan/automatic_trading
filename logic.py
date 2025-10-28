import os, traceback, threading, time
from framework import db, scheduler
from framework.job import Job
from framework.util import Util
from .plugin import logger, package_name
from .model import ModelSetting

class Logic:
    db_default = {
        'db_version': '1',
        'trade_amount_percent': '10',
        'leverage': '1',
        'take_profit_percent': '1',
        'stop_loss_percent': '1',
        'max_holding_minutes': '60',
        'mode': 'simulation',
        'telegram_api_key': '',
        'telegram_chat_id': ''
    }

    @staticmethod
    def db_init():
        try:
            for key, value in Logic.db_default.items():
                if db.session.query(ModelSetting).filter_by(key=key).count() == 0:
                    db.session.add(ModelSetting(key, value))
            db.session.commit()
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def plugin_load():
        try:
            Logic.db_init()
            from .plugin import plugin_info
            Util.save_from_dict_to_json(plugin_info, os.path.join(os.path.dirname(__file__), 'info.json'))
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def plugin_unload():
        try:
            logger.debug('%s plugin_unload', package_name)
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())

    @staticmethod
    def process_telegram_data(data):
        try:
            logger.debug(data)
        except Exception as e:
            logger.error('Exception:%s', e)
            logger.error(traceback.format_exc())
