"""/\/\/\/\/\/\/\/\/\/      CLIENT      /\/\/\/\/\/\/\/\/\/"""

from sys import argv, exit
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM, SOL_SOCKET, SO_BROADCAST, SO_REUSEADDR, inet_aton, error as socket_error
import os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from gui_client1 import Ui_MainWindow

BROADCAST_PORT = 10101

class BroadcastListenerThread(QThread):
    server_info_received = pyqtSignal(str, int)

    def run(self):
        with socket(AF_INET, SOCK_DGRAM) as listener_socket:
            listener_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            listener_socket.bind(('', BROADCAST_PORT))
            while True:
                message, _ = listener_socket.recvfrom(1024)
                server_ip, server_port = message.decode().split(':')
                self.server_info_received.emit(server_ip, int(server_port))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.uic.chon_file.clicked.connect(self.choose)
        self.uic.send.clicked.connect(self.gui)
        self.selected_file_path = None

        # Start listening for server broadcasts
        self.broadcast_listener = BroadcastListenerThread()
        self.broadcast_listener.server_info_received.connect(self.on_server_info_received)
        self.broadcast_listener.start()

    def choose(self):
        options = QFileDialog.Options()
        self.selected_file_path, _ = QFileDialog.getOpenFileName(self, "Chọn một file", "", "All Files (*);;Text Files (*.txt)", options=options)
        if self.selected_file_path:
            self.uic.dd_file.setText(self.selected_file_path)

    def on_server_info_received(self, ip, port):
        self.uic.ip_server.setText(ip)
        self.uic.port_server.setText(str(port))

    def gui(self):
        if self.selected_file_path:
            server_ip = self.uic.ip_server.text()
            server_port = self.uic.port_server.text()
            if not self.validate_ip_port(server_ip, server_port):
                QMessageBox.critical(self, "Error", "Hãy kiểm tra lại IP address hoặc port")
                return
            try:
                server_port = int(server_port)
                self.send_file(self.selected_file_path, server_ip, server_port)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Warning", "Hãy thêm một file")

    def send_file(self, file_path, server_ip, server_port):
        client_socket = socket(AF_INET, SOCK_STREAM)
        try:
            client_socket.connect((server_ip, server_port))
            file_name = os.path.basename(file_path)
            file_name_encoded = file_name.encode()
            file_name_length = len(file_name_encoded)
            client_socket.sendall(file_name_length.to_bytes(4, 'big'))
            client_socket.sendall(file_name_encoded)
            with open(file_path, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.sendall(data)
                    data = file.read(1024)
            QMessageBox.information(self, "Success", "File gửi thành công !!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during file transfer: {e}")
        finally:
            client_socket.close()

    def validate_ip_port(self, ip, port):
        try:
            inet_aton(ip)  # Kiểm tra xem IP có hợp lệ không
            int(port)  # Kiểm tra xem port có phải là số nguyên hợp lệ không
            return True
        except (socket_error, ValueError):
            return False

if __name__ == "__main__":
    app = QApplication(argv)
    main_win = MainWindow()
    main_win.show()
    exit(app.exec_())
