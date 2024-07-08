"""/\/\/\/\/\/\/\/\/\/      SERVER      /\/\/\/\/\/\/\/\/\/"""

import sys
from random import randint
from socket import socket, gethostbyname, gethostname,SOCK_DGRAM, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_BROADCAST, inet_aton, error as socket_error
from threading import Thread
from os import makedirs, path
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from gui_server2 import Ui_MainWindow

BROADCAST_PORT = 10101

class BroadcastThread(QThread):
    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = port

    def run(self):
        with socket(AF_INET, SOCK_DGRAM) as broadcast_socket:
            broadcast_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            message = f"{self.ip}:{self.port}".encode()
            while True:
                broadcast_socket.sendto(message, ('<broadcast>', BROADCAST_PORT))
                self.sleep(5)  # Phát sóng mỗi 5 giây

    def sleep(self, seconds):
        QThread.sleep(seconds)

class ServerThread(QThread):
    file_saved = pyqtSignal(str)
    client_connected = pyqtSignal(str, int)
    error_occurred = pyqtSignal(str)

    def __init__(self, ip, port):
        super().__init__()
        self.ip = ip
        self.port = int(port)

    def run(self):
        try:
            self.server()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def handle_client(self, connection, address):
        try:
            client_ip, client_port = address
            print(f"Connected by {client_ip}:{client_port}")
            self.client_connected.emit(client_ip, client_port)

            file_name_length = int.from_bytes(connection.recv(4), 'big')
            file_name = connection.recv(file_name_length).decode()
            makedirs('file_in_server', exist_ok=True)
            file_path = path.join('file_in_server', file_name)
            with open(file_path, "wb") as file:
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    file.write(data)
            print(f"File {file_name} has been saved to {file_path}")
            self.file_saved.emit(file_name)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def server(self):
        try:
            host = self.ip
            port = self.port
            with socket(AF_INET, SOCK_STREAM) as server_socket:
                server_socket.bind((host, port))
                server_socket.listen()
                print("Server is listening...")

                # Start broadcasting
                self.broadcast_thread = BroadcastThread(host, port)
                self.broadcast_thread.start()

                while True:
                    connection, address = server_socket.accept()
                    thread = Thread(target=self.handle_client, args=(connection, address))
                    thread.start()
        except Exception as e:
            self.error_occurred.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.start.clicked.connect(self.start_server)
        self.uic.auto_2.clicked.connect(self.auto_fill_ip_and_port)

    def start_server(self):
        self.uic.abc.setText("Đang tìm kiếm client...")
        ip = self.uic.ip_address.text()
        port = self.uic.port.text()
        if not self.validate_ip_port(ip, port):
            QMessageBox.critical(self, "Error", "Invalid IP address or port")
            return
        self.server_thread = ServerThread(ip, port)
        self.server_thread.file_saved.connect(self.update_list_file)
        self.server_thread.client_connected.connect(self.update_client_list)
        self.server_thread.error_occurred.connect(self.display_error)
        self.server_thread.start()

    def auto_fill_ip_and_port(self):
        try:
            ip_address = gethostbyname(gethostname())
            port = randint(1024, 65535)  # Tạo một cổng ngẫu nhiên từ 1024 đến 65535
            self.uic.ip_address.setText(ip_address)
            self.uic.port.setText(str(port))
            QMessageBox.information(self, "Auto Fill IP and Port", f"Đã tự động điền IP: {ip_address} và Port: {port}")
        except socket_error as e:
            QMessageBox.critical(self, "Error", f"Lỗi khi lấy địa chỉ IP: {str(e)}")

    def update_list_file(self, file_name):
        self.uic.list_file.addItem(file_name)

    def update_client_list(self, ip, port):
        self.uic.list_client.addItem(f"Client IP: {ip}, Port: {port}")

    def display_error(self, error_message):
        QMessageBox.critical(self, "Server Error", f"An error occurred: {error_message}")

    def validate_ip_port(self, ip, port):
        try:
            inet_aton(ip)  # Kiểm tra xem IP có hợp lệ không
            int(port)  # Kiểm tra xem port có phải là số nguyên hợp lệ không
            return True
        except (socket_error, ValueError):
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
