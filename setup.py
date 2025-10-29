# -*- coding: utf-8 -*-
import traceback
from plugin import *
from .config_loader import load_config

# 플러그인 메뉴 설정
setting = {
    'filepath': __file__,
    'use_db': True,
    'use_default_setting': True,
    'home_module': None,
    'menu': {
        'uri': __package__,
        'name': '자동 트레이딩',
        'list': [
            {'uri': 'setting', 'name': '설정'},
            {'uri': 'history', 'name': '거래 기록'},
            {'uri': 'manual', 'name': '매뉴얼', 'list': [{'uri': 'README.md', 'name': 'README.md'}]},
            {'uri': 'log', 'name': '로그'},
        ]
    },
    'setting_menu': None,
    'default_route': 'normal',
}

P = create_plugin_instance(setting)

# config.yaml 로드
load_config()

try:
    from .mod_basic import ModuleBasic
    P.set_module_list([ModuleBasic])
except Exception as e:
    P.logger.error(f'Exception:{str(e)}')
    P.logger.error(traceback.format_exc())



