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
                'uri': 'core/setting',  # 설정 화면 URI
                'name': '설정',
            },
            {
                'uri': 'core/history',  # 거래 히스토리 화면 URI
                'name': '거래 기록',
            },
            {
                'uri': 'core/manual',  # 메뉴얼 화면 URI
                'name': '메뉴얼',
                'list': [
                    {'uri': 'README.md', 'name': 'README.md'},  # README 파일 링크
                ]
            },
            {
                'uri': 'core/log',  # 로그 화면 URI
                'name': '로그',
            },
        ]
    },
    'setting_menu': None,
    'default_route': 'core/setting',  # 기본 화면
}

# 플러그인 인스턴스 생성
P = create_plugin_instance(setting)

# 모듈 등록
try:
    from .mod_core import ModuleCore  # core 모듈을 만들어야 함
    P.set_module_list([ModuleCore])
except Exception as e:
    P.logger.error(f'Exception:{str(e)}')
    P.logger.error(traceback.format_exc())
