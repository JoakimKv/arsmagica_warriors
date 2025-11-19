
# tournament_app_class.py


from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QTextEdit
)
from PyQt6.QtGui import QIntValidator
import sys

from handle_warriors_class import HandleWarriors
from combat_tournament_class import CombatTournament


class TournamentApp(QWidget):
    
    def __init__(self, bIsDebugMode = False):

        super().__init__()

        self.bIsDebugMode = bIsDebugMode

        if self.bIsDebugMode:
           self.setWindowTitle("Warrior Tournament Inspector")
           self.resize(750, 450)
        else:
           self.setWindowTitle("Warrior Tournament")
           self.resize(550, 300) 

        self.strStoredText = ""

        # Set background color of the whole window
        self.setStyleSheet("background-color: #ffffee;")

        # Layout
        layout = QVBoxLayout()

        handleWarriors = HandleWarriors(debugMode = self.bIsDebugMode)
        filenameStart = handleWarriors.getOnlyFilenameStartFromPath()
        filenameUpdated = handleWarriors.getOnlyFilenameUpdatedFromPath()

        # Info Label (multi-line)
        self.infoLabel = QLabel(
            f"\n"
            f"This program runs a tournament between warriors with the following steps:\n"
            f""
            f"1. Load warrior data from the Excel file (in the 'warriors' folder): '{filenameStart}'.\n"
            f"2. Simulate tournament rounds the number of times chosen (everyone meets each other).\n"
            f"3. Saves the updated ratings to a new Excel file (in the 'warriors' folder): '{filenameUpdated}'."
            f"\n\n\n"
        )
        self.infoLabel.setWordWrap(True)

        # Set custom text color (blue here)
        self.infoLabel.setStyleSheet("color: blue;")

        layout.addWidget(self.infoLabel)

        # Debug/Output area

        self.debugOutput = QTextEdit()
        self.debugOutput.setReadOnly(True)
        self.debugOutput.setStyleSheet("background-color: #ffffee; color: black;")
        self.debugOutput.setMinimumHeight(400)

        if self.bIsDebugMode:          
           layout.addWidget(self.debugOutput)

        # Label and Input.
        self.label = QLabel("Number of Tournament Rounds:")
        layout.addWidget(self.label)

        self.roundsInput = QLineEdit()

        if self.bIsDebugMode:          
           self.roundsInput.setText("10")
        else:            
           self.roundsInput.setText("12")

        self.roundsInput.setValidator(QIntValidator(1, 1000000))
        self.roundsInput.setStyleSheet("background-color: white; color: red;")
        layout.addWidget(self.roundsInput)

        # Run button
        self.runButton = QPushButton("Run Tournament")

        self.runButton.setStyleSheet("""
            QPushButton {
                background-color: #0000FF;   /* blue */
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0000DD;  /* lighter blue */
            }
        """)

        self.runButton.clicked.connect(self.runTournament)
        layout.addWidget(self.runButton)

        # Status Label (multi-line)
        self.statusLabel = QLabel("Status: Idle.")
        self.statusLabel.setWordWrap(True)

        # Set status text color (blue here)
        self.statusLabel.setStyleSheet("color: red;")

        layout.addWidget(self.statusLabel)

        self.setLayout(layout)

    def showWithFocus(self):

        self.show()            # Show the window
        self.raise_()          # Raise it above other windows
        self.activateWindow()  # Give it keyboard focus

    def appendDebugText(self, strText):
       
       self.debugOutput.append(strText)

    def runTournament(self):

        try:
            rounds = int(self.roundsInput.text())
            if rounds < 1:
                raise ValueError("Rounds must be >= 1")
        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter a valid number of rounds (at least 1).")
            return

        # Update status
        self.statusLabel.setText("Status: Working ...")
        QApplication.processEvents()  # Force update UI immediately

        # Create loader object of warriors.
        handleWarriors = HandleWarriors(debugMode = self.bIsDebugMode)

        # Load data from the Excel file.
        handleWarriors.loadDataFromExcelFile()

        # Get the list of Warrior objects.
        warriors = handleWarriors.getWarriorList()

        # Create tournaments between the fighters and update ratings.
        combatTournament = CombatTournament(warriors)
        combatTournament.setNrOfTournamentRounds(rounds)
        combatTournament.makeAllRoundsOfTournament()
        self.strStoredText = combatTournament.strStoredText

        if self.bIsDebugMode:

           self.appendDebugText(self.strStoredText) 

        # Get the list of updated warriors to be saved.
        newWarriorList = combatTournament.getWarriorList()
        handleWarriors.setWarriorList(newWarriorList)

        # Save the new ratings to the updated ("new") excel file.
        handleWarriors.saveDataToExcelFile()

        # Update status back to idle
        self.statusLabel.setText("Status: Idle.")

        QMessageBox.information(self, "Success", f"Tournament finished with {rounds} rounds.\nExcel file updated!")
        self.activateWindow()
