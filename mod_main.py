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

def process_menu(self, sub, req):
    arg = ModelSetting.to_dict()

    # sub가 None이면 기본 화면 설정
    if sub is None or sub == "main":
        sub = "setting"  # 기본 화면 파일 이름

    # html 파일 렌더링
    try:
        return render_template(f"{__package__}_{sub}.html", arg=arg)
    except Exception:
        # 없으면 기본 샘플 페이지
        return render_template("sample.html", title=f"{__package__} - {sub}")
   

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

