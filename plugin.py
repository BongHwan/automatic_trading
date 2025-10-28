# -*- coding: utf-8 -*-
import os
import traceback
from flask import Blueprint, request, render_template, redirect, jsonify
from flask_login import login_required

from framework.logger import get_logger
from framework import app, db, scheduler, check_api
from .logic import Logic
from .model import ModelSetting

package_name = __name__.split('.')[0]
logger = get_logger(package_name)

# Blueprint 설정
blueprint = Blueprint(package_name, package_name, url_prefix='/%s' % package_name,
                      template_folder=os.path.join(os.path.dirname(__file__), 'templates'))

# SJVA 메뉴
menu = {
    'main': [package_name, 'Binance Auto Trading'],
    'sub': [['setting', '설정'], ['history', '거래 기록'], ['log', '로그'], ['manual', '메뉴얼']],
    'category': 'trading'
}

plugin_info = {
    'version': '0.1.0',
    'name': 'Binance Auto Trading',
    'category_name': 'trading',
    'developer': 'CT_B',
    'description': 'Binance 자동매매 및 시뮬레이션 플러그인',
    'home': '',
    'more': ''
}

def plugin_load():
    Logic.plugin_load()

def plugin_unload():
    Logic.plugin_unload()

@blueprint.route('/')
def home():
    return redirect('/%s/setting' % package_name)

@blueprint.route('/<sub>')
@login_required
def first_menu(sub):
    if sub == 'setting':
        arg = ModelSetting.to_dict()
        arg['package_name'] = package_name
        return render_template(f'{package_name}_{sub}.html', arg=arg)
    elif sub == 'history':
        return render_template(f'{package_name}_{sub}.html', arg={'package_name': package_name})
    elif sub == 'log':
        return render_template('log.html', package=package_name)
    elif sub == 'manual':
        return render_template(f'{package_name}_{sub}.html', arg={'package_name': package_name})
    return render_template('sample.html', title=f'{package_name} - {sub}')

@blueprint.route('/ajax/<sub>', methods=['GET', 'POST'])
@login_required
def ajax(sub):
    try:
        if sub == 'setting_save':
            ret = ModelSetting.setting_save(request)
            return jsonify(ret)
        elif sub == 'history_load':
            from .logic_normal import LogicNormal
            return jsonify(LogicNormal.get_history())
    except Exception as e:
        logger.error('Exception:%s', e)
        logger.error(traceback.format_exc())
