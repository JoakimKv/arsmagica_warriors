
# ArsMagica Warriors


## Desktop Applications – ArsMagica Warriors

Two 'Desktop Applications' are created with this 'Python' program: 'WarriorTournament.exe' and 'WarriorTournamentInspector.exe'. The main idea behind the project is to rate different warriors according to the chess rating system. To achieve this the different warriors meet each other in a tournament hence the name of the program. The data from each warrior is retrieved from an excel file with for instance the warriors start rating, which often are set to 1000. In a tournament each warrior meet all other warriors in a fight exactly once per tournament. This means that there are n * (n - 1) / 2 fights in a tournament, if there are n warriors. 

The combat system is based on the role playing game called 'ArsMagica'. A few changes are made to this combat system: no die roll is used on the defense (instead a static value of +6 is used) and a new advantage called 'Berserker' is added to the combat system which contain some new combat rules. No 'magic' is used in the fights. Different fighting styles (weapon combinations) gets a small advantage or disadvantage depending on what fighting style the opponent uses. After 100 rounds in a fight, the fight automatically stops, and if both fighters still stands a draw is obtained.

The point with the program is to fill an excel file, 'warriors_start.xlsx', with warrior stats and start ratings. These warriors will meet each other in 'n' number of tournaments and thus get their ratings updated according to their losses, wins and draws. This value 'n' can be chosen in the 'Desktop Application'. The result of the tournament with the warriors new ratings are then stored to yet another excel file. For the 'WarriorTournament.exe' the updated excel file is 'warriors_updated.xlsx' and for the 'WarriorTournamentInspector.exe' the updated excel file is 'warriors_inspector_updated.xlsx'. The 'WarriorTournamentInspector.exe' is more of a debug or inspector program, where you in detail can study what happened in each fight and the recommendation for this program is that you do not use so many tournaments for these simulations. The program prints out the obtained combat information in the text area in the Desktop Application.

The programs can take some time to run so have some patience and start with smaller values on 'n' especially for the 'inspector' program ('WarriorTournamentInspector.exe').

---


## Project Structure for running the program  

A simplified overview (the same structure as in the 'dist' folder):

- In the installation folder: -> 'WarriorTournamentInspector.exe', 'WarriorTournament.exe' and the folder 'warriors'.

- In the 'warriors' folder: -> 'warriors_start.xlsx'.

- Now you can run the programs 'WarriorTournamentInspector.exe' and 'WarriorTournament.exe' by 'double clicking' on them (the 'warriors' folder is in the same place as the '.exe' files and the 'warriors_start.xlsx' file is in the 'warriors' folder). The results of the new ratings can be seen in the 'warriors' folder in one of the excel files: 'warriors_updated.xlsx' or 'warriors_inspector_updated.xlsx'.

- The two mentioned '.exe' files above and the 'warriors' folder with the excel file 'warriors_start.xlsx' can all be found in the 'dist' folder in the project.


## Installation guide

On windows 11:

- To start the virtual environment: python -m venv venvtournament

- To enable scripts (if necessary): Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

- To activate script and environment: venvtournament\Scripts\activate

- To install packages: pip install -r requirements.txt

- If you want to install all the package manually then the file 'pip_install_info.txt' can be of use. 

- Go to the projects main folder and in powershell run the following command to create an .exe file:

- For 'WarriorTournament.exe' (in 'main.py' set 'bIsDebugMode = False'):

pyinstaller --onefile --windowed --exclude PyQt5 --name WarriorTournament --add-data "images\ArsMagica_Logo_11.png;images" --add-data "images\ArsMagica_Logo_3.png;images" main.py

- For 'WarriorTournamentInspector.exe' (in 'main.py' set 'bIsDebugMode = True'):

pyinstaller --onefile --windowed --exclude PyQt5 --name WarriorTournamentInspector --add-data "images\ArsMagica_Logo_11.png;images" --add-data "images\ArsMagica_Logo_3.png;images" main.py


## Author

This project is made by Joakim Kvistholm.
