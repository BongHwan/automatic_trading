import base64

from support import SupportSubprocess

from .setup import *

class ModuleMain(PluginModuleBase):

    def __init__(self, P):
        super(ModuleMain, self).__init__(P, name='main', first_menu='setting', scheduler_desc='자동매매')
        self.db_default = {
            f'{self.name}_db_version' : '1',
            f'{self.name}_auto_start' : 'False',
            f'{self.name}_bot_token' : '',
        }
        self.process = None


    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        if sub == 'setting':
            arg['_status'] = self.process != None
        return render_template('{package_name}_{module_name}_{sub}.html'.format(package_name=P.package_name, module_name=self.name, sub=sub), arg=arg)

    def plugin_load(self):
        pass

    def socketio_connect(self):
        self.send_data()

    def send_data(self):
        F.socketio.emit("status", self.trade_data, namespace=f'/{self.P.package_name}/{self.name}')







