import logging
import socket
import subprocess

from pathlib import Path

import psutil
import pytest

from .addon import mitm_log
from .system_proxy import set_proxy

logger = logging.getLogger(__name__)


class MitmProxyManager:
    def __init__(self):
        self._mitmproxy_process = None
        self._addon_file = Path(__file__).parent / 'addon.py'
        self.url_filter = None

    def __setattr__(self, name, value):
        if name == 'url_filter' and value:
            super().__setattr__(name, value)
            self._start_mitmproxy()
        super().__setattr__(name, value)

    @staticmethod
    def _kill_existing_mitmproxy_processes():
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'mitmdump.exe':
                proc.terminate()
                proc.wait()

    def _get_available_port(self, start_port=8080):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        _, port = sock.getsockname()
        sock.close()
        return port if port != start_port else self._get_available_port(start_port=start_port + 1)

    def _start_mitmproxy(self):
        self._kill_existing_mitmproxy_processes()
        proxy_port = self._get_available_port()
        set_proxy(enable_proxy=True, proxy_address=f"http://127.0.0.1:{proxy_port}")
        mitmproxy_command = ['mitmdump', '-p', str(proxy_port), '-s', self._addon_file, '-q', '--set',
                             f'url_filter={self.url_filter}']
        # 启动mitmproxy
        logger.debug("启动mitmproxy")
        self._mitmproxy_process = subprocess.Popen(mitmproxy_command)

    def _stop_mitmproxy(self):
        if self._mitmproxy_process:
            self._mitmproxy_process.terminate()
            self._mitmproxy_process.wait()
            set_proxy(enable_proxy=False)

    @staticmethod
    def get_urls():
        with open(mitm_log, 'r') as f:
            urls = [line.strip() for line in f.readlines()]
            return urls


@pytest.fixture
def mitmdump_proxy(request):
    """启用mitmdump抓取数据"""
    manager = MitmProxyManager()

    def finalize():
        manager._stop_mitmproxy()

    request.addfinalizer(finalize)
    return manager
