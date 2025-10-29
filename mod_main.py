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
        super().__init__(PM, None)

    def plugin_load(self):
        pass

    def process_menu(self, sub, req):
        _ = req
        try:
            arg = ModelSetting.to_dict()
            return render_template(f"{package_name}_{sub}.html", arg=arg)
        except Exception:
            return render_template("sample.html", title=f"{package_name} - {sub}")

    def process_command(self, command, arg1=None, arg2=None, arg3=None, req=None):
        ret = {"ret": "success", "msg": ""}
        if command == "dummy_update":
            self.trade_data["orders"].append({"symbol": arg1, "qty": arg2})
            ret["msg"] = f"주문 추가됨: {arg1}, 수량: {arg2}"
            self.send_data()
        return jsonify(ret)

    def socketio_connect(self):
        self.send_data()

    def send_data(self):
        F.socketio.emit("status", self.trade_data, namespace=f'/{self.P.package_name}/{self.name}')

