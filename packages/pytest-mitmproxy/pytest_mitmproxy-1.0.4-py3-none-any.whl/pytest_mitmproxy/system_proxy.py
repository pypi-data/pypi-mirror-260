import ctypes
import logging
import winreg

logger = logging.getLogger(__name__)


def set_proxy(enable_proxy, proxy_address="http://127.0.0.1:8080"):
    try:
        # 代理服务器地址和端口
        proxy_server = proxy_address

        # 打开注册表键
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)

        # 设置代理服务器
        if enable_proxy:
            winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, proxy_server)
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
        else:
            # 关闭代理
            winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)

        # 刷新代理设置
        INTERNET_OPTION_REFRESH = 37
        INTERNET_OPTION_SETTINGS_CHANGED = 39
        internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
        internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
        internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)

        # 关闭注册表键
        winreg.CloseKey(key)
        logger.debug("系统代理设置成功！")
    except Exception as e:
        logger.error(f"设置系统代理失败: {e}")


if __name__ == "__main__":
    # 设置代理（启用代理）
    set_proxy(enable_proxy=True, proxy_address="http://127.0.0.1:8080")
    # 设置代理（关闭代理）
    # set_proxy(enable_proxy=False)
