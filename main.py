
# main.py


import os
import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
from tournament_app_class import TournamentApp


def main():

   app = QApplication(sys.argv)

   bIsDebugMode = True

   tournamentApp = TournamentApp(bIsDebugMode=bIsDebugMode)

    
   if bIsDebugMode:
      
      imageFile = resourcePath("images/ArsMagica_Logo_11.png")
      width = 700
      height = 450

   else:
      
      imageFile = resourcePath("images/ArsMagica_Logo_3.png")
      width = 600
      height = 400   

   splashImage = QPixmap(imageFile).scaled(
      width, height,                 
      Qt.AspectRatioMode.KeepAspectRatio,
      Qt.TransformationMode.SmoothTransformation
   )

   splash = QSplashScreen(splashImage)

   splash.show()

   QTimer.singleShot(
      2000,
      lambda: show_main_window(app, splash, tournamentApp)
   )

   sys.exit(app.exec())


def show_main_window(app, splash, tournamentApp):
    
    """Called when the QTimer finishes."""

    # Make sure splash updates visually.
    app.processEvents()

    tournamentApp.showWithFocus()

    splash.finish(tournamentApp)


def resourcePath(relativePath):
    
    """Get absolute path to resource (for dev and PyInstaller)."""

    if hasattr(sys, '_MEIPASS'):
        
        return os.path.join(sys._MEIPASS, relativePath)
    
    return os.path.join(os.path.abspath("."), relativePath)


if __name__ == "__main__":
    
    main()
     