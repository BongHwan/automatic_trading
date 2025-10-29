from .setup import *

name = 'main'

class ModuleMain(PluginModuleBase):
    
    def __init__(self, P):
        super(ModuleMain, self).__init__(P, name=name)
        default_route_socketio_module(self)
        # 트레이딩용 더미 데이터 구조
        self.trade_data = {
            "positions": [],
            "orders": [],
            "account": {"balance": 1000000, "equity": 1000000}
        }

    def process_menu(self, sub, req):
        _ = req
        try:
            arg = ModelSetting.to_dict()
            return render_template(f"{package_name}_{sub}.html", arg=arg)
        except Exception:
            return render_template("sample.html", title=f"{package_name} - {sub}")
        
    def process_command(self, command, arg1, arg2, arg3, req):
        # 기능 구현 없이 화면/소켓 테스트용
        ret = {"ret": "success", "msg": ""}
        if command == "dummy_update":
            # 예: 주문 추가/제거 등 UI 테스트용
            self.trade_data["orders"].append({"symbol": arg1, "qty": arg2})
            ret["msg"] = f"주문 추가됨: {arg1}, 수량: {arg2}"
            self.send_data()
        return jsonify(ret)

    def socketio_connect(self):
        # 연결 시 현재 데이터 전송
        self.send_data()
    
    def send_data(self):
        # SocketIO로 화면 전송
        F.socketio.emit("status", self.trade_data, namespace=f'/{P.package_name}/{name}')

