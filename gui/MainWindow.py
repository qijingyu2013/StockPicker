import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget

from gui.TokenDialog import TokenDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.setWindowTitle("PyQt5 窗口")
        self.setGeometry(100, 100, 600, 400)  # 设置窗口的位置和大小

        # 设置中心窗口组件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)


        # 创建一个标签并设置 token 作为其文本
        self.token_label = QLabel(self)
        token = self.getToken()
        self.token_label.setText(f"当前的 Token: {token}")
        self.token_label.adjustSize()  # 自动调整标签的大小以适应内容
        self.token_label.move(50, 50)  # 移动标签的位置

        # 创建一个按钮并设置文本
        self.button = QPushButton("输入新的 Token", self)
        self.button.adjustSize()  # 自动调整标签的大小以适应内容
        self.button.move(50, 70)  # 设置按钮的位置
        # 将按钮的点击事件连接到一个槽函数
        self.button.clicked.connect(self.show_token_dialog)


        # 创建 "进入新页面" 按钮并将其添加到布局
        self.entry_button = QPushButton("进入新页面", self.central_widget)
        self.entry_button.setFixedSize(200, 50)

    def show_token_dialog(self):
        dialog = TokenDialog()
        if dialog.exec_():  # 如果用户点击了保存按钮
            new_token = dialog.getNewToken()
            if new_token:  # 确保输入的 token 非空
                self.setToken(new_token)
                self.token_label.setText(f"当前的 Token: {new_token}")
                self.token_label.adjustSize()  # 自动调整标签的大小以适应新内容

    def getToken(self):
        try:
            XQ_TOKEN_FILE = open('../xueqiu_token.txt', 'r+')
            XQ_A_TOKEN = XQ_TOKEN_FILE.readline().strip()
            XQ_TOKEN_FILE.close()
        except FileNotFoundError as e:
            open('../xueqiu_token.txt', 'w+')
            XQ_A_TOKEN = ''
        return XQ_A_TOKEN

    def setToken(self, new_token):
        try:
            XQ_TOKEN_FILE = open('../xueqiu_token.txt', 'w+')
            XQ_A_TOKEN = XQ_TOKEN_FILE.readline().strip()
            XQ_TOKEN_FILE.write(new_token+'\n')
            XQ_TOKEN_FILE.close()
        except FileNotFoundError as e:
            open('../xueqiu_token.txt', 'w+')
            XQ_A_TOKEN = ''
        return XQ_A_TOKEN

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
