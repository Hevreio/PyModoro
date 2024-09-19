from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QPainterPath, QPen, QColor, QBrush, QFont
from PySide6.QtWidgets import QVBoxLayout, QSlider, QWidget, QApplication

class CPBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.p = 0 # p为归一化的进度值

    def upd(self, pp):
        if self.p == pp:
            return
        self.p = pp
        self.update()

    def paintEvent(self, e, is_working=True):

        # 强制令进度条为圆形
        if self.height() > self.width():
            self.setFixedWidth(self.height())

        if self.width() > self.height():
            self.setFixedHeight(self.width())

        pd = self.p * 360
        rd = 360 - pd

        # 调用QPainter进行画图
        p = QPainter(self)
        p.fillRect(self.rect(), Qt.white)
        p.translate(4, 4)
        p.setRenderHint(QPainter.Antialiasing)
        path, path2 = QPainterPath(), QPainterPath()

        circle_width = self.width() - self.width() / 10
        widht_half = circle_width/2

        path.moveTo(widht_half, 0)
        # 定义了所在矩形区域
        circle_rect = QRectF(self.rect().left() / 2, self.rect().top() / 2, circle_width, self.height() - self.height() / 10)

        path.arcTo(circle_rect, 90, -pd) # 绘制全部的弧线
        pen, pen2 = QPen(), QPen() # pen负责部分弧线，pen2负责全部弧线

        pen.setCapStyle(Qt.FlatCap)
        if is_working:
            pen.setColor(QColor("#e04728"))
        else:
            pen.setColor(QColor("#50c21b"))
        pen_width = self.width()/25
        pen.setWidth(pen_width)
        p.strokePath(path, pen)

        # 灰色的pen2负责背景
        path2.moveTo(widht_half, 0)
        pen2.setWidth(pen_width)
        pen2.setColor(QColor("#d7d7d7"))
        pen2.setCapStyle(Qt.FlatCap)

        # pen2.setDashPattern([0.5, 1.105]) # remove this line to have continue cercle line
        path2.arcTo(circle_rect, 90, rd)
        # pen2.setDashOffset(2.2) # this one too
        p.strokePath(path2, pen2)
        p.setPen(pen)

        # 绘制进度百分比文本
        font = QFont()
        percent_size = self.height() / 7
        font.setPointSizeF(percent_size)
        p.setFont(font)
        percent_text_position = self.rect().center()
        p_in_percent = self.p * 100 # 换算

        # 设置中间标签位置
        percent_text_position.setX(percent_text_position.x() - (
                percent_size + (self.width()/6 if p_in_percent >= 100 else self.width()/10 if p_in_percent >= 10 else +self.width()/40)))
        percent_text_position.setY(percent_text_position.y() + percent_size * 2 / 5)

        # 绘制标签
        p.drawText(percent_text_position, f"{round(self.p * 100, 0)}%")


class Test(QWidget):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout(self)
        p = CPBar(self)
        # p.resize(100,100)
        s = QSlider(Qt.Horizontal, self)
        s.setMinimum(0)
        s.setMaximum(100)
        l.addWidget(p)
        l.addWidget(s)
        self.setLayout(l)
        s.valueChanged.connect(lambda: p.upd(s.value() / s.maximum()))
        # connect(s, &QSlider::valueChanged, [=](){ p->upd((qreal)s->value() / s->maximum());});


if __name__ == '__main__':
    app = QApplication()
    main_widget = Test()
    main_widget.show()
    app.exec_()