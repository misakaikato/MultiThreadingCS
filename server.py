import threading
import socket
import sys
import os

#ｗｅｂ　ｓｅｒｖｅｒ
class Server:
    serverPort = 0
    serverAddress = "127.0.0.1"
    serverSocket = None

    clientPool = []
    threadPool = []
    exit = False

    def __init__(self, serverPort):
        self.exit = False
        self.serverPort = serverPort
        # 初始化服务器连接
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.serverAddress, self.serverPort))
        except:
            exit()

    def recvFromClient(self, client, addr):
        while client in self.clientPool:
            tcpClisock = client
            try:
                BUFSIZE = 1024
                print('Waiting for the connection：', addr)
                data = client.recv(BUFSIZE).decode()
                filename = data.split()[1]
                filename = filename[1:]
            # 突发意外情况，来自客户端的连接关闭
            except Exception as e:
                if client in self.clientPool:
                    client.close()
                return
            else:
                '''当网络质量差没有收到浏览器的访问数据时执行'''
                if filename == "":
                    tcpClisock.close()
                    print("请输入要访问的文件")

                base_dir = os.getcwd()
                file_dir = os.path.join(base_dir, filename)

                # # 请求行（还有POST请求方式）
                # GET / HTTP / 1.1\r\n
                # # 请求体
                # Host: www.itcast.cn\r\n
                # Connection: keep - alive\r\n
                # Upgrade - Insecure - Requests: 1\r\n
                # User - Agent: Mozilla / 5.0(Macintosh;
                # Intel
                # Mac
                # OS
                # X
                # 10_12_4) AppleWebKit / 537.36(KHTML, like
                # Gecko) Chrome / 69.0
                # .3497
                # .100
                # Safari / 537.36\r\n
                # Accept: text / html, application / xhtml + xml, application / xml;
                # q = 0.9, image / webp, image / apng, /;q = 0.8\r\n
                # Accept - Encoding: gzip, deflate\r\n
                # Accept - Language: zh - CN, zh;
                # q = 0.9\r\n
                # Cookie: pgv_pvi = 1246921728; \r\n
                # # 空行（不能省略）
                # \r\n
                '''当访问的文件在本地服务器存在时执行'''
                if os.path.exists(file_dir):
                    f = open(file_dir, encoding='utf-8')
                    SUCCESS_PAGE = "HTTP/1.1 200 OK\r\n\r\n" + f.read()
                    print(SUCCESS_PAGE)
                    tcpClisock.sendall(SUCCESS_PAGE.encode())
                    tcpClisock.close()
                else:
                    FAIL_PAGE = "HTTP/1.1 404 NotFound\r\n\r\n" + open(os.path.join(base_dir, "fail.html"),
                                                                       encoding="utf-8").read()
                    print(FAIL_PAGE)
                    tcpClisock.sendall(FAIL_PAGE.encode())
                    tcpClisock.close()

   #  客户端已连接: ('127.0.0.1', 53729)
   #  客户端已连接: ('127.0.0.1', 53730)
   #  GET / index2.html
   #  HTTP / 1.1  # 请求行
   #  Host: 127.0
   #  .0
   #  .1: 8090
   #  Connection: keep - alive
   #  Cache - Control: max - age = 0
   #  Upgrade - Insecure - Requests: 1
   #  User - Agent: Mozilla / 5.0(Windows
   #  NT
   #  10.0;
   #  Win64;
   #  x64) AppleWebKit / 537.36(KHTML, like
   #  Gecko) Chrome / 73.0
   #  .3683
   #  .103
   #  Safari / 537.36
   #  Accept: text / html, application / xhtml + xml, application / xml;
   #  q = 0.9, image / webp, image / apng, /;q = 0.8, application / signed - exchange;
   #  v = b3
   #  Accept - Encoding: gzip, deflate, br
   #  Accept - Language: zh - CN, zh;
   #  q = 0.9

   #  GET / web.jpg
   #  HTTP / 1.1
   #  Host: 127.0
   #  .0
   #  .1: 8090
   #  Connection: keep - alive
   #  User - Agent: Mozilla / 5.0(Windows
   #  NT
   #  10.0;
   #  Win64;
   #  x64) AppleWebKit / 537.36(KHTML, like
   #  Gecko) Chrome / 73.0
   #  .3683
   #  .103
   #  Safari / 537.36
   #  Accept: image / webp, image / apng, image /, / *;q = 0.8
   #  Referer: http: // 127.0
   #  .0
   #  .1: 8090 / index2.html
   #  Accept - Encoding: gzip, deflate, br
   #  Accept - Language: zh - CN, zh;

    def acceptLoop(self):
        self.serverSocket.listen(20)
        while True:
            client, _ = self.serverSocket.accept()
            self.clientPool.append(client)
            thread = threading.Thread(target=self.recvFromClient, args=(client, _))
            thread.setDaemon(True)
            thread.start()

    def start(self):
        thread = threading.Thread(target=self.acceptLoop)
        thread.setDaemon(True)
        thread.start()
        while True:
            if self.exit:
                return

if __name__ == "__main__":
    server_port = int(sys.argv[1])
    server = Server(server_port)
    server.start()
