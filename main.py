import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, qApp, QApplication, QStackedWidget, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QColor


model = load_model("avocado_price.h5")

class Main(QMainWindow):

    def __init__(self):

        super().__init__()
        loadUi("main.ui", self)
        self.etat = 0
        self.validButton.clicked.connect(self.prediction)
        self.exitButton.clicked.connect(qApp.quit)
        self.maximizeButton.clicked.connect(self.maximizeominimize)
        self.reduceButton.clicked.connect(widget.showMinimized)

        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(50)
        self.shadow.setColor(QColor("#f576db"))
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.validButton.setGraphicsEffect(self.shadow)

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Une erreur est survenu, impossible de réaliser les prédictions.")
        self.msg.setWindowTitle("Erreur")

    def maximizeominimize(self):

        if self.etat == 0:
            widget.showMaximized()
            self.etat = 1
        else:
            widget.showNormal()
            self.etat = 0

    def prediction(self):
        self.total_volume = self.totalVolume.text()
        self.sb = self.small_bag.text()
        self.lb = self.large_bag.text()
        self.p4097 = self.plu_4097.text()
        self.p4226 = self.plu_4226.text()
        self.p4770 = self.plu_4770.text()
        self.tb = self.total_bag.text()

        try:
            self.total_volume = float(self.total_volume)
            self.sb = float(self.sb)
            self.lb = float(self.lb)
            self.p4097 = float(self.p4097)
            self.p4226 = float(self.p4226)
            self.p4770 = float(self.p4770)
            self.tb = float(self.tb)

            X_new = np.array([[self.total_volume, self.p4097, self.p4226, self.p4770, self.tb, self.sb, self.lb]])
            prediction = model.predict(X_new)
            prediction = str(prediction)
            self.showResult(prediction)

        except Exception as e:
            self.msg.show()

    def showResult(self, result):
        self.result = QMessageBox()
        self.result.setIcon(QMessageBox.Information)
        self.result.setText(f"Le prix des avocat est de: {result}")
        self.result.setWindowTitle("Résultat de la prédiction")
        self.result.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    widget = QStackedWidget()
    main = Main()
    widget.setAttribute(Qt.WA_TranslucentBackground)
    widget.setWindowFlag(Qt.FramelessWindowHint)
    widget.addWidget(main)
    widget.resize(1006, 754)
    widget.show()
    sys.exit(app.exec())
