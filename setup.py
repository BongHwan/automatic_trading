# -*- coding: utf-8 -*-
#import traceback
#from plugin import *
#from .config_loader import load_config

__menu = {
    'uri': __package__,
    'name': '자동 트레이딩',
    'list': [
        {
            'uri': 'setting',
            'name': 'Main',
        },
        {
            'uri': 'log',
            'name': '로그',
        },
    ]
}

setting = {
    'filepath' : __file__,
    'use_db': False,
    'use_default_setting': False,
    'home_module': None,
    'menu': __menu,
    'setting_menu': None,
    'default_route': 'normal',
}

from plugin import *

P = create_plugin_instance(setting)

from .mod_basic import ModuleBasic

P.set_module_list([ModuleBasic])





