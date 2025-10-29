from .setup import *

class ModuleMain(PluginModuleBase):

    def __init__(self, P):
        #super(ModuleMain, self).__init__(P, None)
        super(ModuleMain, self).__init__(P, name='main', first_menu='setting')
        default_route_socketio_module(self)
        # 화면/소켓용 더미 데이터
        self.trade_data = {
            "positions": [],
            "orders": [],
            "account": {"balance": 1000000, "equity": 1000000}
        }

def process_menu(self, page, req):
    arg = ModelSetting.to_dict()

    # page가 None이면 기본 페이지로 변경
    if page is None:
        page = "setting"  # 기본 화면 html 이름

    try:
        return render_template(f'{P.package_name}_{self.name}_{page}.html', arg=arg)
    except Exception:
        return render_template("sample.html", title=f"{self.P.package_name} - {page}")
  

    def process_command(self, command, arg1, arg2, arg3, req):
        ret = {"ret": "success", "msg": ""}
        if command == "dummy_update":
            self.trade_data["orders"].append({"symbol": arg1, "qty": arg2})
            ret["msg"] = f"주문 추가됨: {arg1}, 수량: {arg2}"
            self.send_data()
        return jsonify(ret)

    def socketio_connect(self):
        self.send_data()

    def send_data(self):
        F.socketio.emit("status", self.trade_data, namespace=f'/{P.package_name}/{name}')



