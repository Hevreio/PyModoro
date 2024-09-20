import sys 
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtWidgets import QGridLayout, QHBoxLayout
from PySide6.QtCore import QThread, Signal, QTimer, Qt
from PySide6.QtGui import QFont
from pgbar import CPBar
from info_block import InfoBlock


class TomatoTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QGridLayout()
        self.clockLayout = QVBoxLayout()
        self.infoLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.clockLayout, 0, 0, 1, 2)
        self.mainLayout.addLayout(self.infoLayout, 0, 2, 1, 1)
        self.setLayout(self.mainLayout)

        # self.work_duration = 25 * 60
        self.work_duration = 5
        self.break_duration = 5 
        self.time_left = self.work_duration
        self.is_running = False
        self.is_work_time = True

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint) # 隐藏标题栏


    def time_convert(self, time):
        mins, secs = divmod(time, 60)
        return f"{mins:02d}:{secs:02d}"

    def init_ui_clock(self):
        
        self.timer_label = QLabel(self)
               
        # 固定尺寸并居中
        self.resize(480, 320)
        screen = app.primaryScreen()
        center = screen.availableGeometry().center()
        self.move(center.x() - self.width() / 2, center.y() - self.height() / 2)

        # 进度条
        self.prog_bar = CPBar(self)
        self.clockLayout.addWidget(self.prog_bar, alignment=Qt.AlignmentFlag.AlignCenter)   
        self.prog_bar.setFixedSize(200, 200)
        self.prog_bar.upd(1)
        
        # 信息块
        self.infoblock = InfoBlock()
        self.infoLayout.addWidget(self.infoblock)

        # 按钮（一个平行的boxlayout）
        btn_grp = QHBoxLayout()
        btn_tg = QPushButton("Toggle", self)
        btn_tg.clicked.connect(self.toggle_timer)
        btn_rst = QPushButton("Reset", self)
        btn_rst.clicked.connect(self.reset_timer)
        btn_plus = QPushButton("+", self)
        btn_plus.clicked.connect(lambda: self.adjust_time(1))
        btn_minus = QPushButton("-", self)  
        btn_minus.clicked.connect(lambda: self.adjust_time(-1))
        
        # 计时器初始化
        self.clockLayout.addWidget(self.timer_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setText(self.time_convert(self.time_left)) 

        font = QFont()
        font.setPointSize(40)
        self.timer_label.setFont(font)

        btn_grp.addWidget(btn_tg)
        btn_grp.addWidget(btn_rst)
        btn_grp.addWidget(btn_plus)
        btn_grp.addWidget(btn_minus)
        self.clockLayout.addLayout(btn_grp)

    def toggle_timer(self):
        if self.is_running:
            self.timer.stop()
        else:
            self.timer.start(1000)
        self.is_running = not self.is_running

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(self.time_convert(self.time_left))
            if self.is_work_time:
                self.prog_bar.upd(self.time_left / self.work_duration)
            else:
                self.prog_bar.upd(self.time_left / self.break_duration)

        else:
            # 进入记时末尾
            self.timer.stop()
            self.is_running = False
            self.is_work_time = not self.is_work_time
            self.prog_bar.is_working = self.is_work_time

            # 已经调整完了工作状，重新初始化记时状态
            if self.is_work_time:
                self.time_left = self.work_duration
                self.prog_bar.upd(1)
                min, sec = divmod(self.time_left, 60)
                self.timer_label.setText(f"{min:02d}:{sec:02d}")               
                
            else:
                self.time_left = self.break_duration
                self.prog_bar.upd(1)
                min, sec = divmod(self.time_left, 60)
                self.timer_label.setText(f"{min:02d}:{sec:02d}")
                
    def adjust_time(self, direction):
        if self.is_work_time:
            self.work_duration += direction * 60
            if self.work_duration < 60:
                self.work_duration = 60
            self.time_left = self.work_duration
        else:
            self.break_duration += direction * 60
            if self.break_duration < 60:
                self.break_duration = 60
            self.time_left = self.break_duration
            self.prog_bar.is_working = self.is_work_time
        # mins, secs = divmod(self.time_left, 60)
        # self.timer_label.setText(f"{mins:02d}:{secs:02d}")
        self.timer_label.setText(self.time_convert(self.time_left))

    def reset_timer(self):
        '''reset the timer to initial state i.e. 25 minutes work time and 5 minutes break time'''
        print("reset")
        self.timer.stop()
        self.is_running = False
        self.is_work_time = True
        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.time_left = self.work_duration
        self.prog_bar.is_working = True
        minu, secs = divmod(self.time_left, 60)
        self.timer_label.setText(f"{minu:02d}:{secs:02d}")
        self.prog_bar.upd(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TomatoTimer()
    window.init_ui_clock()
    window.show()
    sys.exit(app.exec())


    

    