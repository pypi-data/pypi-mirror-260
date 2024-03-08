import pytest
import os

pytest_plugins = ("pytest_jupyter.jupyter_server", )

os.environ["RS_SERVER_URL"] = "https://dev1.workbench.example"
os.environ["RS_URI_SCHEME"] = "https"
os.environ["RS_SESSION_URL"] = "/s/d5de821f2ed72294f5ffc/"
os.environ["RS_PORT_TOKEN"] = "a433e59dc087"

@pytest.fixture
def jp_server_config(jp_server_config):
    return {
        "ServerApp": {
            "jpserver_extensions": {
                "pwb_jupyterlab": True
            }
        }
   }

def pytest_addoption(parser):
    parser.addoption(
        "--jenkins",
        action="store_true",
        default=False,
        help="Enable jenkins environment")
