#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-07-13 12:09:49
LastEditors  : Kofi
LastEditTime : 2023-07-13 12:09:50
Description  : 
"""
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,QScrollArea,QGridLayout,QSizePolicy
class PaperWidget(QWidget):
    Signal_ImageChanged = pyqtSignal(str)
    Signal_ZoomClicked = pyqtSignal()
    Signal_InfoClicked = pyqtSignal()

    def __init__(self, name: str = "paper_widget", width: int = 240, height: int = 340, **kwargs) -> None:
        super().__init__()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.zoom_button = QPushButton("放大")
        self.zoom_button.clicked.connect(self.Signal_ZoomClicked.emit)

        self.info_button = QPushButton("信息")
        self.info_button.clicked.connect(self.Signal_InfoClicked.emit)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.zoom_button)
        button_layout.addWidget(self.info_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setObjectName(name)
        self.setFixedSize(width, height)
        self.set_image("./1.jpg")

    def set_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)
        self.Signal_ImageChanged.emit(image_path)



class PaperListWidget(QWidget):
    def __init__(self, num_papers: int = 6, num_columns: int = 3, parent=None,**kwargs):
        super().__init__(parent)
        
        self.paper_widgets = []
        self.num_columns = num_columns
        self.num_rows = (num_papers + num_columns - 1) // num_columns
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.scroll_widget = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll_area)
        
        self.set_num_papers(num_papers)

    def set_num_papers(self, num_papers: int):
        while len(self.paper_widgets) < num_papers:
            paper_widget = PaperWidget()
            self.paper_widgets.append(paper_widget)
        
        while len(self.paper_widgets) > num_papers:
            paper_widget = self.paper_widgets.pop()
        
        for i, paper_widget in enumerate(self.paper_widgets):
            row = i // self.num_columns
            column = i % self.num_columns
            self.scroll_layout.addWidget(paper_widget, row, column)
        
        for i in range(num_papers, self.num_rows * self.num_columns):
            empty_widget = QWidget()
            empty_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll_layout.addWidget(empty_widget, i // self.num_columns, i % self.num_columns)