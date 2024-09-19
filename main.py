import sys 
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import QThread, Signal, QTimer, Qt
from pgbar import CPBar

class TomatoTimer(QWidget):
    def __init__(self):
        super().__init__()

        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.time_left = self.work_duration
        self.is_running = False
        self.is_work_time = True

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


    
    def init_ui(self):
        self.setWindowTitle("Tomato Timer")
        self.timer_label = QLabel("25:00", self)
        self.timer_label.setStyleSheet("font-size: 50px")
        self.resize(100,200)
        screen = app.primaryScreen()
        center = screen.availableGeometry().center()
        self.move(center.x() - self.width() / 2, center.y() - self.height() / 2)

        

        btn = QPushButton("Toggle", self)
        btn.clicked.connect(self.toggle_timer)

        btn_plus = QPushButton("+", self)
        btn_plus.clicked.connect(lambda: self.adjust_time(1))
        btn_minus = QPushButton("-", self)  
        btn_minus.clicked.connect(lambda: self.adjust_time(-1))

        self.prog_bar = CPBar(self)


        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(btn)
        layout.addWidget(btn_plus)
        layout.addWidget(btn_minus)
        layout.addWidget(self.prog_bar)

        self.setLayout(layout)
        self.show()

    def toggle_timer(self):
        if self.is_running:
            self.timer.stop()
        else:
            self.timer.start(1000)
        self.is_running = not self.is_running

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            mins, secs = divmod(self.time_left, 60)
            self.timer_label.setText(f"{mins:02d}:{secs:02d}")
            self.prog_bar.upd(self.time_left / self.work_duration)

        else:
            self.timer.stop()
            self.is_running = False
            self.is_work_time = not self.is_work_time
            if self.is_work_time:
                self.time_left = self.work_duration
            else:
                self.time_left = self.break_duration
    
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
        mins, secs = divmod(self.time_left, 60)
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.is_work_time = True
        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        self.time_left = self.work_duration
        min, secs = divmod(self.time_left, 60)
        self.timer_label.setText(f"{min:02d}:{secs:02d}")


            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TomatoTimer()
    window.init_ui()
    sys.exit(app.exec())


    

    