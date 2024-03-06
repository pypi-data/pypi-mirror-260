# Import third-party modules
import pytest

# Import local modules
from arthub_login_widgets.core import LoginWindow
from arthub_login_widgets.core import LoginBackend
from arthub_login_widgets.test.ipc import IPCServer


class FakeAPI:
    def __init__(self, mocker, login_status=True):
        self.login_status = login_status
        self.mocker = mocker

    def login(self, account, password, save_token_to_cache):
        return self.mocker.MagicMock(
            is_succeeded=self.mocker.MagicMock(return_value=self.login_status),
            error_message=self.mocker.MagicMock(return_value="login failed."),
        )


class TestLoginWindow:
    @pytest.fixture(autouse=True)
    def setup(self, mocker, qtbot):
        self.widget = LoginWindow(api=FakeAPI(mocker))
        qtbot.addWidget(self.widget)

    def test_show_widget(self):
        self.widget.line_edit_password.setText("xxxx")
        assert self.widget.line_edit_password.text() == "xxxx"

    def test_run_callback(self):
        def _custom_callback(api):
            print("run custom callback...")
            api._custom_callback = "custom callback"
            assert True

        self.widget.line_edit_account.setText("abc")
        self.widget.line_edit_password.setText("abc")
        self.widget.set_callback(_custom_callback)
        self.widget.login()
        assert self.widget._custom_callback == "custom callback"

    def test_login_failed(self, mocker):
        widget = LoginWindow(FakeAPI(mocker=mocker, login_status=False))
        widget.line_edit_account.setText("abc")
        widget.line_edit_password.setText("abc")

        widget.login()
        assert widget.label_prompt.text() == "login failed."


def test_task_pad():
    # init account backend
    backend = LoginBackend(
        terminal_type="dcc",
        business_type="default",
        dev_mode=True,
    )
    if not backend.is_login():
        assert backend.popup_login()

    def process_client_request(m):
        print("receive message from client! {}".format(m))
        # Will not response if return None
        return None

    # init ipc server
    server = IPCServer()
    # set request process function
    server.set_receive_callback(process_client_request)
    print("start server..")
    # listen at port {0} will find a usable port
    port = server.init(0)
    print("listen at {}".format(port))

    # show task pad window
    window = backend.popup_task_pad(port)

    while True:
        text = input("input command: ")
        if text == "e":
            break

        message = {
            "command": text,
            "filepath": "G:/MotionBuillderFiles/A_S2_Idle_to_RunL180_PI_o_001_walk_stand_none_two_layer.fbx"
        }
        server.send_message(json.dumps(message).encode('utf-8'))

    print("server closing..")
    server.close_server()

    print("window closing..")
    window.close()
