
Implement system to async states by updating the JSON. Obviously, this isn't quite working with local files, see below. 


PS C:\CodingProjects\Games\RPGEngine> & C:/CodingProjects/Games/RPGEngine/venv/Scripts/python.exe c:/CodingProjects/Games/RPGEngine/main.py
pygame 2.6.1 (SDL 2.28.4, Python 3.12.6)
Hello from the pygame community. https://www.pygame.org/contribute.html
Error saving world config: [WinError 32] Der Prozess kann nicht auf die Datei zugreifen, da sie von einem anderen Prozess verwendet wird: 'C:\\Users\\Janal\\AppData\\Local\\Temp\\tmpm2ylnft1'
Error saving characters config: [WinError 32] Der Prozess kann nicht auf die Datei zugreifen, da sie von einem anderen Prozess verwendet wird: 'C:\\Users\\Janal\\AppData\\Local\\Temp\\tmphokqje8a'
Error saving world config: [WinError 32] Der Prozess kann nicht auf die Datei zugreifen, da sie von einem anderen Prozess verwendet wird: 'C:\\Users\\Janal\\AppData\\Local\\Temp\\tmpgw3xxck7'
Error saving characters config: [WinError 32] Der Prozess kann nicht auf die Datei zugreifen, da sie von einem anderen Prozess verwendet wird: 'C:\\Users\\Janal\\AppData\\Local\\Temp\\tmp3_rsly2c'

Implement database to handle the state data.
(How would I handle savestates? Can I still? Is it one or the other?)
(Should be fine to implement two modes? Savestates for SP should be much simpler)
(Online tactical arena game would be kinda fun actually?)

OR
Simply remove the updating states and implement this for a later iteration this was a stupid idea to implement now.