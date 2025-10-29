# -*- coding: utf-8 -*-
import traceback
from plugin import *

# 플러그인 메뉴 설정
setting = {
    'filepath': __file__,  # 현재 파일 경로
    'use_db': True,        # DB 사용 여부
    'use_default_setting': True,  # 기본 설정값 사용 여부
    'home_module': None,   # 초기 화면 모듈
    'menu': {
        'uri': __package__,  # 패키지 이름 사용
        'name': '자동 트레이딩',  # 플러그인 이름
        'list': [
            {
                'uri': 'setting',  # 설정 화면 URI
                'name': '설정',
            },
            {
                'uri': 'history',  # 거래 히스토리 화면 URI
                'name': '거래 기록',
            },
            {
                'uri': 'manual',
                'name': '매뉴얼',
                'list': [
                    {'uri': 'README.md', 'name': 'README.md'},
                ]
            },
            {
                'uri': 'log',
                'name': '로그',
            },
        ]
    },
    'setting_menu': None,
    'default_route': 'setting',
}

from plugin import *

P = create_plugin_instance(setting)

try:
    from .mod_basic import ModuleBasic
    P.set_module_list([ModuleBasic])
except Exception as e:
    P.logger.error(f'Exception:{str(e)}')
    P.logger.error(traceback.format_exc())



