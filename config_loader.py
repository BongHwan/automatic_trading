import yaml, os
from .plugin import P, logger

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def load_config():
    try:
        if not os.path.exists(CONFIG_PATH):
            logger.warning(f"config.yaml not found at {CONFIG_PATH}")
            return

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        # 자동매매 모드
        P.ModelSetting.set('basic_mode', cfg.get('TRADING_MODE', 'SIMULATION'))
        P.ModelSetting.set('basic_trade_amount_percent', int(cfg.get('POSITION_RATIO', 0.1) * 100))
        P.ModelSetting.set('basic_leverage', cfg.get('LEVERAGE', 1))
        P.ModelSetting.set('basic_take_profit_percent', cfg.get('TAKE_PROFIT', 1))
        P.ModelSetting.set('basic_stop_loss_percent', cfg.get('STOP_LOSS', 1))
        P.ModelSetting.set('basic_max_holding_minutes', int(cfg.get('MAX_HOLD_SECONDS', 3600)/60))
        P.ModelSetting.set('basic_strategy_priority', cfg.get('STRATEGY_PRIORITY', 'TRIGGER'))

        # Telegram
        telegram_cfg = cfg.get('TELEGRAM', {})
        P.ModelSetting.set('basic_telegram_enabled', telegram_cfg.get('ENABLED', False))
        P.ModelSetting.set('basic_telegram_api_key', telegram_cfg.get('BOT_TOKEN', ''))
        P.ModelSetting.set('basic_telegram_chat_id', telegram_cfg.get('CHAT_ID', ''))

        # PostgreSQL (선택적)
        P.ModelSetting.set('postgres_host', cfg.get('POSTGRES', {}).get('HOST', 'localhost'))
        P.ModelSetting.set('postgres_port', cfg.get('POSTGRES', {}).get('PORT', 5432))
        P.ModelSetting.set('postgres_user', cfg.get('POSTGRES', {}).get('USER', 'postgres'))
        P.ModelSetting.set('postgres_password', cfg.get('POSTGRES', {}).get('PASSWORD', 'password'))
        P.ModelSetting.set('postgres_db', cfg.get('POSTGRES', {}).get('DB', 'auto_trader'))

        logger.info("config.yaml loaded successfully")

    except Exception as e:
        logger.error(f"Failed to load config.yaml: {str(e)}")
