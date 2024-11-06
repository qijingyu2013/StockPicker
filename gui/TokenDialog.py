from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton


class TokenDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("输入新的 Token")
        self.layout = QVBoxLayout()

        self.token_input = QLineEdit(self)
        self.layout.addWidget(self.token_input)

        self.button_box = QHBoxLayout()

        self.save_button = QPushButton("保存", self)
        self.save_button.clicked.connect(self.accept)
        self.button_box.addWidget(self.save_button)

        self.cancel_button = QPushButton("取消", self)
        self.cancel_button.clicked.connect(self.reject)
        self.button_box.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_box)
        self.setLayout(self.layout)

    def getNewToken(self):
        return self.token_input.text()