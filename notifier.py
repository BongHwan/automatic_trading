from plugin import P, ToolNotify

def send_telegram_message(msg: str):
    """Telegram 설정에 따라 메시지를 전송"""
    try:
        enabled = P.ModelSetting.get_bool('basic_telegram_enabled')
        api_key = P.ModelSetting.get('basic_telegram_api_key')
        chat_id = P.ModelSetting.get('basic_telegram_chat_id')

        if not enabled:
            P.logger.debug("Telegram 알림 비활성화 상태. 메시지 전송 생략.")
            return False

        if not api_key or not chat_id:
            P.logger.warning("Telegram API key 또는 chat_id 설정 없음.")
            return False

        ToolNotify.send_message(msg, 'trading', api_key=api_key, chat_id=chat_id)
        return True
    except Exception as e:
        P.logger.error(f"Telegram 메시지 전송 실패: {str(e)}")
        return False
