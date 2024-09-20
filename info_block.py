from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import QTimer, QDateTime, Qt
from PySide6.QtGui import QFont
from weather import fetchWeather
import requests
from const_value import LOCATION, API, KEY, UNIT, LANGUAGE


class InfoBlock(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        font = QFont("Microsoft YaHei", 13)
        self.setFont(font)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.weather_timer = QTimer()
        self.weather_timer.timeout.connect(self.update_weather)
        self.weather_timer.start(1000 * 60) # 1 minute

        self.lb_time = QLabel("1970-01-01", self)
        self.lb_weather = QLabel("Weather", self)
        self.lb_temp = QLabel("Temperature", self)
        self.lb_tomato = QLabel("Tomato Timer", self)
        self.lb_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_weather.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lb_tomato.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.lb_time)
        self.layout.addWidget(self.lb_weather)
        self.layout.addWidget(self.lb_temp)
        self.layout.addWidget(self.lb_tomato)

        # 在显示之前先更新一次
        self.update_time()
        self.update_weather()

    def update_time(self):
        time = QDateTime.currentDateTime()
        self.lb_time.setText(f"{time.toString('yyyy-MM-dd hh:mm:ss')}")

    def update_weather(self, location=LOCATION):
        wt = fetchWeather(location)
        self.lb_weather.setText(f"{wt['results'][0]['location']['name']}   " + f"{wt['results'][0]['now']['text']}")
        # print(wt['results'][0]['now']['temperature'])
        self.lb_temp.setText(f"{wt['results'][0]['now']['temperature']}" + "°C")
        # print(wt['results'][0]['now']['text'])
 

if __name__ == '__main__':
    app = QApplication([])
    ib = InfoBlock()
    ib.show()
    app.exec()
