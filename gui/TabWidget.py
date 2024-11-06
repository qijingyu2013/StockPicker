from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel


class TabWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("多标签页页面")
        self.setGeometry(100, 100, 600, 400)

        # 创建 QVBoxLayout 并设置为窗口的布局
        self.layout = QVBoxLayout(self)

        # 创建 QTabWidget
        self.tabs = QTabWidget()

        # 创建第一个标签页
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab1_content = QLabel("这是第一个标签页的内容")
        self.tab1_layout.addWidget(self.tab1_content)
        self.tab1.setLayout(self.tab1_layout)
        self.tabs.addTab(self.tab1, "标签页 1")

        # 创建第二个标签页
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_content = QLabel("这是第二个标签页的内容")
        self.tab2_layout.addWidget(self.tab2_content)
        self.tab2.setLayout(self.tab2_layout)
        self.tabs.addTab(self.tab2, "标签页 2")

        # 创建第三个标签页
        self.tab3 = QWidget()
        self.tab3_layout = QVBoxLayout()
        self.tab3_content = QLabel("这是第三个标签页的内容")
        self.tab3_layout.addWidget(self.tab3_content)
        self.tab3.setLayout(self.tab3_layout)
        self.tabs.addTab(self.tab3, "标签页 3")

        # 将 QTabWidget 添加到布局
        self.layout.addWidget(self.tabs)