from .setup import *

class ModuleMain(PluginModuleBase):

    def __init__(self, P):
        super(ModuleMain, self).__init__(P, name='main', first_menu='setting', scheduler_desc="코인 자동 매매")
        self.db_default = {
            f'db_version': '1',
            f'{self.name}_auto_start': 'False',
            f'{self.name}_interval': '0 8 * * *',
            f'{self.name}_db_delete_day': '30',
            f'{self.name}_db_auto_delete': 'False',
            f'{P.package_name}_item_last_list_option': '',
        }        

    def process_menu(self, sub, req):
        arg = P.ModelSetting.to_dict()
        if sub == 'setting':
            arg['is_include'] = F.scheduler.is_include(self.get_scheduler_name())
            arg['is_running'] = F.scheduler.is_running(self.get_scheduler_name())
        return render_template(f'{P.package_name}_{self.name}_{sub}.html', arg=arg)
    
    def process_command(self, command, arg1=None, arg2=None, arg3=None, req=None):
        """
        버튼 클릭 등 명령 처리 (실제 기능 구현 없이 화면/소켓 테스트용)
        """
        ret = {"ret": "success", "msg": ""}
        if command == "dummy_update":
            self.trade_data["orders"].append({"symbol": arg1, "qty": arg2})
            ret["msg"] = f"주문 추가됨: {arg1}, 수량: {arg2}"
            self.send_data()
        return jsonify(ret)

    def socketio_connect(self):
        """
        SocketIO 연결 시 데이터 전송
        """
        self.send_data()

    def send_data(self):
        """
        SocketIO로 현재 더미 데이터를 화면으로 전송
        """
        F.socketio.emit("status", self.trade_data, namespace=f'/{P.package_name}/{self.name}')


