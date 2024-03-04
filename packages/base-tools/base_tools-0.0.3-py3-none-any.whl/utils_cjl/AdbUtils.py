import subprocess


def input_text(text: str) -> tuple:
    adb_command = ['adb', 'shell', 'input', 'text']
    text_bytes = text.encode('utf-8')
    process = subprocess.Popen(adb_command, shell=True, stdout=subprocess.PIPE)
    output, error = process.communicate(text_bytes)
    return output, error


def tap(x: float, y: float, device_serial: str = None) -> subprocess.CompletedProcess:
    command = f'adb shell input tap {x} {y}' if device_serial is None else f'adb -s {device_serial} shell input tap {x} {y}'
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def install(apk_path: str) -> subprocess.CompletedProcess:
    """
    在设备上安装应用程序
    :param apk_path: 安装包目录
    :return: 执行结果
    """
    command = f"adb install -r {apk_path}"
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def pull(device_path: str, local_path: str) -> subprocess.CompletedProcess:
    """
    从设备上导出文件
    :param device_path: 文件在设备上的地址
    :param local_path: 文件导出到的地址，此处为执行命令的设备的地址
    :return: 执行结果
    """
    command = f"adb pull {device_path} {local_path}"
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def start_application(package_name: str, activity_name: str) -> subprocess.CompletedProcess:
    """
    启动应用程序
    :param package_name: 应用包名，如com.example.app
    :param activity_name: 启动Activity完整名称，包括包名。如com.example.app.MainActivity
    :return: 执行结果
    """
    command = f"adb shell am start -n {package_name}/{activity_name}"
    return subprocess.run(command, shell=True, check=True, capture_output=True)


def list_packages() -> subprocess.CompletedProcess:
    """
    查看设备上的应用程序列表
    :return: 执行结果
    """
    command = "adb shell pm list packages"
    return subprocess.run(command, shell=True, check=True, capture_output=True)
