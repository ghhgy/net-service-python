# net-service-python(基于Python的自动认证校园网系统服务)

## 1. 功能

自动认证校园网，一键打包，一键安装为系统服务。

通过注册为系统服务，不需要额外配置开机自启等功能，一次配置，永久可用。

支持平台：Windows,Linux

本工具在win11和Ubuntu20测试正常，其它Linux版本不确定是否正常工作，您可根据源码自行修改打包

发行版为西安理工大学校园网直接可用版本（适用于Windows和Linux），可以直接下载；

其它校园网只需自行修改源码中的登录代码，并一键打包。

## 2. 打包与部署

请在该服务的目标系统中打包，如：若该服务的目标系统为Ubuntu，请在Ubuntu系统中打包

### 2.1 Ubuntu

#### 2.1.1 打包

把`build.sh`和源文件`school-net.py`放入同一目录，执行下面的命令

```bash
# 打包
sh build.sh
```

可执行文件在`dist`目录下生成，您可将其移入任意位置

#### 2.1.2 部署

可执行文件支持的命令，最好所有命令前加上sudo，因为要修改系统文件

```bash
# 安装服务,指定学号密码,安装后会自动启动服务,并开机自启动
school-net.exe install 123 456
# 卸载服务
school-net.exe uninstall
# 查看服务状态
school-net.exe status
# 启动服务
school-net.exe start
# 停止服务
school-net.exe stop
# 重启服务
school-net.exe restart
# 仅运行
school-net.exe  123 456
# 帮助
school-net.exe help
```

### 2.2 Windows

#### 2.2.1 打包

把`build.cmd`和源文件`school-net.py`放入同一目录，直接双击`build.cmd`

可执行文件在dist目录下生成，打包后的文件需要与`dist\service.exe`在同一文件夹中使用，您可将二者移入任意位置

#### 2.2.2 部署

可执行文件支持的命令，注意打包后的文件需要与`dist\service.exe`在同一文件夹中使用

```bash
# 安装服务,指定学号密码,安装后会自动启动服务,并开机自启动
school-net.exe install 123 456
# 卸载服务
school-net.exe uninstall
# 查看服务状态
school-net.exe status
# 启动服务
school-net.exe start
# 停止服务
school-net.exe stop
# 重启服务
school-net.exe restart
# 仅运行
school-net.exe  123 456
# 帮助
school-net.exe help
```

