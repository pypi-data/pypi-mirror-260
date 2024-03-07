import subprocess
import platform
from pathlib import Path


def is_mitmproxy_cert_installed():
    try:
        # 使用 PowerShell 检查证书是否存在
        res = subprocess.check_output(['powershell',
                                       'Get-ChildItem -Path Cert:\CurrentUser\Root | Where-Object {$_.Subject -like "*mitmproxy*"}'])
        if res:
            return True
        return False
    except subprocess.CalledProcessError as e:
        return False


def install_mitmproxy_certificate(cert_path):
    system_platform = platform.system()
    if system_platform == "Windows":
        # Windows系统下使用certutil命令
        try:
            res = subprocess.run(["certutil.exe", "-addstore", "root", cert_path], check=True, capture_output=True,
                                 text=True)
            print(res)
            print("Mitmproxy证书已成功安装到根证书存储中。")
        except subprocess.CalledProcessError as e:
            print(f"安装Mitmproxy证书失败: {e}")


def install():
    """安装证书"""
    if is_mitmproxy_cert_installed():
        print("Mitmproxy证书已安装")
    else:
        print("Mitmproxy证书未安装")
        # 替换为实际的证书路径
        certificate_path = Path(__file__).parent / "certs" / "mitmproxy-ca-cert.cer"

        install_mitmproxy_certificate(certificate_path)

# "certmgr.msc"
