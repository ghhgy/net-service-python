import requests, time, platform, os, traceback, subprocess, sys

_CurrentDir = os.path.dirname(os.path.abspath(sys.argv[0]))

service_name, extension = os.path.splitext(os.path.basename(os.path.abspath(sys.argv[0])))
service_file_path = os.path.join("/etc/systemd/system/", service_name + ".service") if os.name == 'posix' \
    else os.path.join(_CurrentDir, "service.xml")

_Description = 'Automatically authenticate campus network'

# 这是windows和ubuntu的服务相关的配置文件
def getConfig(usernum, password):
    return f'''[Unit]
    Description={_Description}
    After=network.target
    StartLimitIntervalSec=0
    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    User=root
    ExecStart={os.path.abspath(sys.argv[0])} {usernum} {password}
    
    [Install]
    WantedBy=multi-user.target
    ''' if os.name == 'posix' else f'''<?xml version="1.0" encoding="UTF-8" ?>
    <service>
      <id>{service_name}</id>
      <name>{service_name}</name>
      <description>{_Description}</description>
      <executable>{os.path.abspath(sys.argv[0])}</executable>
      <arguments>{usernum} {password}</arguments>
      <logpath>{os.path.join(_CurrentDir, "service-log")}</logpath>
      <logmode>roll</logmode>
    </service>
    '''


def isConnected():
    if platform.system() == "Windows":
        res = os.system(u"ping www.baidu.com -n 1 >nul")
    else:
        res = os.system(u"ping www.baidu.com -c 1 >nul")
    if res == 0:
        print("网络正常,无需认证")
        return True
    else:
        print("网络异常，开始认证")
        return False

# 此处代码请根据自己的环境自行实现
def login(usernum, password, times=3):
    url = "http://172.10.255.9/eportal/InterFace.do"
    if times <= 0:
        return
    print(f"开始认证,学号:{usernum} 密码:{password}")
    querystring = {"method": "login"}
    payload = f"userId={usernum}&password={password}&service=%25E5%2586%2585%25E7%25BD%2591%252B%25E5%25A4%2596%25E7%25BD%2591&queryString=wlanuserip%253D68b8767138c3b65a16e2693a7d8f0c89%2526wlanacname%253D97ab810d5fdf6cc9b8af3e881b6615fd%2526ssid%253D%2526nasip%253D6be7b81ce0ec6345fcc85877bf5905dc%2526snmpagentip%253D%2526mac%253D5a0a19c91d0886a11aa90b75e18ab03f%2526t%253Dwireless-v2%2526url%253D709db9dc9ce334aada6aa2cce9879f742edec66103693b4a7900df8742ec041b1f9551812448fcdd%2526apmac%253D%2526nasid%253D97ab810d5fdf6cc9b8af3e881b6615fd%2526vid%253De5fcf68a6dc3c3e5%2526port%253D5955338eaca2a84e%2526nasportid%253D5b9da5b08a53a540e26b350a596c2af8e875de291dec11f1a92ed4623d9741fe&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, headers=headers, data=payload, params=querystring)
    response.encoding = 'utf8'
    if response.status_code == 200:
        res = response.json()
        if res["result"] == "success":
            print("认证成功!" if res["message"] == "" else res["message"])
        else:
            print(res["message"])
            login(usernum, password, times - 1)
    else:
        print(response.text)

def main(usernum, password, interval=60):
    print(f"开始监控,学号:{usernum} 密码:{password}")
    while True:
        try:
            if not isConnected():
                login(usernum, password)
        except Exception:
            print(f"{traceback.format_exc()}")
        time.sleep(interval)
        print("持续监控中...")


def executeShell(shell):
    process = subprocess.Popen(shell, shell=True)
    output, error = process.communicate(input='\n')


commands = {
    "install": "安装服务",
    "uninstall": "卸载服务",
    "start": "启动服务",
    "restart": "重启服务",
    "stop": "停止服务",
    "status": "查看服务状态",
    "help": "加载帮助",
    "version": "查看版本"
}


def version():
    print("1.0.0")


def install(usernum, password):
    print(f"开始写文件{service_file_path}...")
    with open(service_file_path, "w", encoding="utf-8") as file:
        file.write(getConfig(usernum, password))
    if os.name == 'posix':
        print(f"增加执行权限{service_file_path}...")
        executeShell(f"sudo chmod +x {service_file_path}")
        print(f"重载系统服务...")
        executeShell("sudo systemctl daemon-reload")
        print(f"设置开机自启动...")
        executeShell(f"sudo systemctl enable {service_name}")
        print(f"启动服务...")
        executeShell(f"sudo systemctl start {service_name}")
    else:
        print(f"注册系统服务...")
        executeShell(f"service.exe install")
        print(f"启动服务...")
        executeShell(f"service.exe start")


def formatCommands():
    max_key_length = max(len(key) for key in commands.keys())
    max_value_length = max(len(value) for value in commands.values())
    return '\n'.join([f"{key:{max_key_length}}       {value:{max_value_length}}" for key, value in commands.items()])


def help():
    print(f'''usage: {service_name}[.exe] [{' | '.join(commands.keys())}] [学号 密码]

安装示例:{service_name}[.exe] install 123 456
卸载示例:{service_name}[.exe] uninstall
直接运行示例:{service_name}[.exe] 123 456

optional arguments:
{formatCommands()}
''')


def uninstall():
    if os.name == 'posix':
        print(f"停止服务...")
        executeShell(f"sudo systemctl stop {service_name}")
        print(f"移除文件{service_file_path}...")
        executeShell(f"sudo rm -f {service_file_path}")
        print(f"重载系统服务...")
        executeShell("sudo systemctl daemon-reload")
    elif os.name == 'nt':
        print(f"停止服务...")
        executeShell(f"service.exe stop")
        print(f"注销服务...")
        executeShell(f"service.exe uninstall")
        print(f"移除文件{service_file_path}...")
        executeShell(f"del \"{service_file_path}\"")


def stop():
    if os.name == 'posix':
        executeShell(f"sudo systemctl stop {service_name}")
    elif os.name == 'nt':
        executeShell(f"service.exe stop")


def status():
    if os.name == 'posix':
        executeShell(f"sudo systemctl status {service_name}")
    elif os.name == 'nt':
        executeShell(f"sc query {service_name}")


def start():
    if os.name == 'posix':
        executeShell(f"sudo systemctl start {service_name}")
    elif os.name == 'nt':
        executeShell(f"service.exe start")


def restart():
    if os.name == 'posix':
        executeShell(f"sudo systemctl restart {service_name}")
    elif os.name == 'nt':
        executeShell(f"service.exe stop")
        executeShell(f"service.exe start")


def handleCommand(name, *args):
    if commands.__contains__(name):
        print(f"正在{commands[name]}...")
        function = globals().get(name)
        if function:
            function(*args)
        else:
            print("Function not found.")
        print("完成!")
        sys.exit(0)


if __name__ == '__main__':
    if os.name != 'posix' and os.name != 'nt':
        print("仅支持Windows和Linux系统!")
        sys.exit(0)
    if len(sys.argv) == 4 and sys.argv[1] == "install":
        handleCommand("install", sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
        sys.exit(0)
    elif len(sys.argv) == 2 and sys.argv[1] != "install":
        handleCommand(sys.argv[1])
    print(f"不合法的命令: {' '.join(sys.argv)}")
