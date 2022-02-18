#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import QApplication
from Controlador.ctrPrincipal import ctrPrincipal

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ctrPrincipal()
    window.show()
    app.exec()