import base64
from contextlib import redirect_stdout
import importlib.machinery
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "autoxray-user"


class UserCommandsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.module = importlib.machinery.SourceFileLoader("autoxray_user_test", str(SCRIPT)).load_module()
        self.module.CONFIG = self.root / "config.json"
        self.module.STATE = self.root / "users.json"
        self.module.NGINX = self.root / "nginx.conf"
        self.module.ACCESS_LOG = self.root / "access.log"
        self.calls = []
        self.module.subprocess.run = self.run_command
        self.fail_restart = False
        self.uuid = "11111111-1111-4111-8111-111111111111"
        config = {
            "inbounds": [
                {"tag": "vsRAWtlsVISION", "settings": {"clients": [{"id": self.uuid}]}},
                {"tag": "vsXHTTPtls", "settings": {"clients": [{"id": self.uuid}]},
                 "streamSettings": {"xhttpSettings": {"path": "/abc123"}}},
                {"tag": "Hysteria2", "settings": {"clients": [{"auth": "aabbccdd"}]},
                 "streamSettings": {"tlsSettings": {"serverName": "example.com"}}},
            ],
            "outbounds": [{"tag": "direct", "protocol": "freedom"}],
        }
        self.module.CONFIG.write_text(json.dumps(config))
        self.module.NGINX.write_text("server {\n    # XHTTP endpoint\n}\n")
        self.web = self.root / "www"
        self.web.mkdir()
        owner_links = f"vless://{self.uuid}@example.com:443?fp=chrome\nhy2://aabbccdd@example.com:443\n"
        (self.web / "legacy.json").write_bytes(base64.b64encode(owner_links.encode()))

    def run_command(self, argv, **kwargs):
        self.calls.append(argv)
        if self.fail_restart and argv == ["systemctl", "restart", "xray"] and kwargs.get("check"):
            raise subprocess.CalledProcessError(1, argv)

    def initialize(self):
        self.module.init(SimpleNamespace(domain="example.com", web_path=str(self.web),
                                         path_xhttp=None, fingerprint=None, subscription_token=None))

    def test_add_status_remove_and_original_link(self):
        self.initialize()
        state = self.module.read_json(self.module.STATE)
        self.assertEqual(self.module.subscription_url(state, state["users"][0]),
                         "https://example.com/legacy.json")
        self.module.add(SimpleNamespace(name="Маша"), state)
        state = self.module.read_json(self.module.STATE)
        friend = self.module.find_user(state, "маша")
        subscription = self.web / "s" / f"{friend['token']}.json"
        content = base64.b64decode(subscription.read_bytes()).decode()
        self.assertEqual(content.count("vless://"), 2)
        self.assertEqual(content.count("hy2://"), 1)
        self.assertNotIn("routing", content)
        config = self.module.read_json(self.module.CONFIG)
        self.assertNotIn("routing", config)
        for inbound in config["inbounds"]:
            clients = inbound["settings"]["clients"]
            self.assertEqual(len(clients), 2)
            self.assertTrue(all(client.get("email") for client in clients))
        self.module.ACCESS_LOG.write_text(
            "2026/10/04 12:30:00 from 1.2.3.4 accepted tcp:example.org:443 "
            f"[vsXHTTPtls -> direct] email: {friend['emails']['xhttp']}\n")
        self.assertEqual(self.module.latest_access(friend["emails"].values()),
                         ("2026/10/04 12:30:00", True))
        self.module.remove(SimpleNamespace(name="Маша"), state)
        self.assertFalse(subscription.exists())
        self.assertEqual(len(self.module.read_json(self.module.STATE)["users"]), 1)

    def test_restart_failure_restores_config_and_files(self):
        self.initialize()
        original_config = self.module.CONFIG.read_bytes()
        original_state = self.module.STATE.read_bytes()
        self.fail_restart = True
        with self.assertRaises(subprocess.CalledProcessError):
            self.module.add(SimpleNamespace(name="Маша"), self.module.read_json(self.module.STATE))
        self.assertEqual(self.module.CONFIG.read_bytes(), original_config)
        self.assertEqual(self.module.STATE.read_bytes(), original_state)
        self.assertEqual(list((self.web / "s").glob("*")), [])

    def test_list_command_shows_each_user_and_link(self):
        self.initialize()
        self.module.add(SimpleNamespace(name="Маша"), self.module.read_json(self.module.STATE))
        self.module.LOCK = self.root / "users.lock"
        output = io.StringIO()
        with patch.object(self.module, "check_root"), patch("sys.argv", ["autoxray-user", "list"]):
            with redirect_stdout(output):
                self.module.main()
        self.assertIn("Владелец: https://example.com/legacy.json", output.getvalue())
        self.assertIn("Маша: https://example.com/s/", output.getvalue())


if __name__ == "__main__":
    unittest.main()
