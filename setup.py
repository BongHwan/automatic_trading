__menu = {
    'uri': __package__,
    'name': '자동 트레이딩',
    'list': [
        {
            'uri': 'main',
            'name': 'Main',
        },
        {
             'uri': 'monitoring',
             'name': '모니터링',
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
}

setting = {
    'filepath' : __file__,
    'use_db': True,
    'use_default_setting': False,
    'home_module': None,
    'menu': __menu,
    'setting_menu': None,
    'default_route': 'normal',
}

from plugin import *

P = create_plugin_instance(setting)

from .mod_main import ModuleMain

P.set_module_list([ModuleMain])









