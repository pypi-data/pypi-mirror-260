import socket
import struct
import time
import subprocess
import shlex
import platform

def kill_matlab_processes():
    # 获取当前操作系统类型
    os_type = platform.system()

    try:
        if os_type == "Windows":
            # 对于Windows系统，使用taskkill
            subprocess.run(["taskkill", "/F", "/IM", "MATLAB.exe"], check=True)
            print("所有MATLAB进程已被成功终止。")
        elif os_type == "Linux" or os_type == "Darwin":
            # 对于Linux和MacOS系统，使用pkill
            # MacOS系统也被视为类Unix系统，通常使用和Linux相同的命令
            subprocess.run(["pkill", "matlab"], check=True)
            print("所有MATLAB进程已被成功终止。")
        else:
            print(f"不支持的操作系统: {os_type}")
    except subprocess.CalledProcessError as e:
        print(f"终止MATLAB进程时发生错误：{e}")



x=0 #全局X坐标
y=0 #全局Y坐标
head=0 #初始车辆朝向角
v0=0 #场景初速度




# 创建一个临时的MATLAB脚本
with open('tempScript.m', 'w') as f:
    f.write(f"x={x};\n")
    f.write(f"y={y};\n")
    f.write(f"head={head};\n")
    f.write(f"v0={v0};\n")
    f.write("acc=0.0;\n") #初始加速度
    f.write("gear=2;\n")#初始档位：1-前进档；2-驻车档；3-倒车档
    f.write("yaw=0.0;\n") #初始前轮转角
    f.write("load('a_brake.mat');\n")
    f.write("load('a_thr.mat');\n")
    f.write("load('brake.mat');\n")
    f.write("load('thr.mat');\n")
    f.write("modelName='VehicleModel';\n")
    f.write("run('control_simulink_with_udp.m');\n")
    #f.write("control_simulink_with_udp();\n")

# command =  f"matlab -r \"run('./control_simulink_with_udp.m')\""
command =  f"matlab -r \"run('./tempScript.m')\""
result = subprocess.run(shlex.split(command),capture_output=True)
print("输出：", result.stdout.decode())
print("\n错误:",result.stderr.decode())


# 设置UDP通信参数
UDP_IP = "127.0.0.1"
UDP_SEND_PORT = 25001  # MATLAB监听的端口
UDP_RECEIVE_PORT = 25000  # Python监听的端口
MESSAGE = "get"

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定到接收端口上以监听传入消息
sock.bind((UDP_IP, UDP_RECEIVE_PORT))

data, _ = sock.recvfrom(1024)  # 假设信号很小，不需要大缓冲区
if data.decode() == 'ready':
    print("MATLAB就绪，继续执行")

# 发送 "get" 消息给 MATLAB，让 MATLAB 知道 Python 的 IP 和端口
#sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_SEND_PORT))

# 定义值的序列
gear_sequence = [1,1,1,1,1]
acceleration_sequence = [1.2,1.2,1.2,1.2,1.2]
steering_angle_sequence = [1.0472,1.0472,1.0472,1.0472,1.0472]

try:
    for gear, acceleration, steering_angle in zip(gear_sequence, acceleration_sequence, steering_angle_sequence):

        # 打包数据
        message = struct.pack('>3d',gear, acceleration,steering_angle)
        # 发送数据到 MATLAB
        sock.sendto(message, (UDP_IP, UDP_SEND_PORT))
        print("指令已发送，等待下一个消息...")
        # 等待接收一条消息
        data, addr = sock.recvfrom(1024)  # 缓冲大小1024字节
        print("接受到回传消息")
        if data:
        # 解析接收到的数据为double类型
            unpacked_data = struct.unpack('>4d', data)  # 使用'>d'表示大端格式的double

        print("Received message:", unpacked_data)
        # 接收到X,Y,速度和朝向角
except KeyboardInterrupt:
    print("程序已停止")
finally:
    sock.close()
    kill_matlab_processes()