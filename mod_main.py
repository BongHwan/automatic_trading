from .setup import *

name = 'main'

class ModuleMain(PluginModuleBase):

     def __init__(self, P):
        super(ModuleMain, self).__init__(P, name=name)
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
        return render_template(f'{self.P.package_name}_{self.name}_{page}.html', arg=arg)
    except Exception:
        return render_template("sample.html", title=f"{self.P.package_name} - {page}")


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

