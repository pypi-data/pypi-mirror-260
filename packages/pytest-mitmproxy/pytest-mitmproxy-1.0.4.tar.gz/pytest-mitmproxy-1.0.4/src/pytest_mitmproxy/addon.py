import logging
import sys
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)
mitm_log = Path(tempfile.gettempdir()) / 'mitmdump.log'


class MyAddon:
    def __init__(self):
        self.log_file = mitm_log
        self.clear_log()
        self.url_filter = None
        # print(f"{sys.argv=}")
        for arg in sys.argv:
            if arg.startswith('url_filter='):
                self.url_filter = arg.split('=')[1]
                break

    def clear_log(self):
        with open(self.log_file, 'w', encoding="utf-8") as f:
            f.truncate()

    def write_log(self, data):
        with open(self.log_file, 'a', encoding="utf-8") as f:
            f.write(f"{data}\n")

    def request(self, flow):
        request_url = flow.request.url
        # print(f"{self.url_filter=}")
        if self.url_filter in request_url:
            self.write_log(request_url)
            print("*" * 80)
            print(request_url)
            print("*" * 80)


addons = [MyAddon()]
