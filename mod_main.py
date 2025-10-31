import subprocess

# third-party
from flask import render_template, jsonify

# pylint: disable=import-error
from plugin import PluginModuleBase

from .setup import P

plugin = P
logger = plugin.logger
package_name = plugin.package_name
ModelSetting = plugin.ModelSetting
plugin_info = plugin.plugin_info

class ModuleMain(PluginModuleBase):

    db_default = {
        "default_interface_id": "",
        "default_traffic_view": "months",
        "traffic_unit": "iec",
        "traffic_list": "24,24,30,12,0,10",
        "vnstat_bin": "vnstat",
        "vnstat_dbdir": "",
    }

    def __init__(self, PM):
        super(ModuleMain, self).__init__(PM, name='main', first_menu='setting', scheduler_desc='코인자동매매')

    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        if sub == 'setting':
            arg['_status'] = self.process != None
        return render_template('{package_name}_{module_name}_{sub}.html'.format(package_name=P.package_name, module_name=self.name, sub=sub), arg=arg)
            
    def plugin_load(self):
        pass

    def process_command(self, command, arg1, arg2, arg3, req):
        ret = {'ret':'success', 'json':None}
        if command == 'execute':
            if arg1 == 'true':
                self.start()
            else:
                self.stop()
        return jsonify(ret)

    def socketio_connect(self):
        self.send_data()

    def send_data(self):
        F.socketio.emit("status", self.trade_data, namespace=f'/{self.P.package_name}/{self.name}')



