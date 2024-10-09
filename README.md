# Projet Embarqué - SI1151




## Description du Projet :
Ce projet consiste à développer une interface de mesure de la lumière en utilisant le capteur SI1151. Le projet inclut une API développée en C pour interfacer le capteur avec l'environnement ENIB et une Interface Homme-Machine (IHM) développée en PyQt5.




## Prérequis :

### Pour l'API en C
- Compilateur GCC
- Environnement ENIB installé et configuré (ou l'IDE STM32CubeIDE)
- Un émulateur de terminal série (minicom ou gtkterm)

### Pour l'IHM en PyQt5
- Python 3.x
- pip (gestionnaire de paquets pour Python)
- Autres dépendances (voir requirements.txt)
- Un IDE tel que PyCharm, VSCode, ou tout autre IDE de votre choix




## Installation et Utilisation

### API en C :

1. **Compilation de l'API :(si vous êtes sur l'environement ENIB sur linux)**
   - Naviguez vers le répertoire `.../Connected-Sensor` et ouvrez-le dans un terminal.
   - Compilez le code en utilisant le Makefile : make
   - tapez **ocd &** 
   - tapez **dbg main.elf** pour ouvrir le débogueur et lancer le programme.
   - Si vous souhaitez visualiser le contenu de la communication série, vous pouvez ouvrir un terminal n'importe où 
     et taper`minicom -D /dev/ttyACM0 -b 115200`  ou avec `gtkterm`   pour les installer tapez :
     (sudo apt install minicom) ou (sudo apt install gtkterm)
   
   **Compilation de l'API :(si vous êtes sur STM32CubeIDE)**
   - Lancez l'IDE.
   - Ouvrez le projet depuis vos répertoires.
   - Cliquez sur le bouton **Build & Debug**
   - Si vous souhaitez visualiser le contenu de la communication série, vous devriez trouver le port COM correspondant
     à cette liaison (généralement c'est le port COM3 ou COM4).
   - Ouvrez **PuTTY**(vous pouvez utiliser également Tera Term ou minicom via WSL).
   - Sélectionnez Serial comme type de connexion.
   - Entrez le port COM (dans le champ Serial line), par exemple : 'COM3'.
   - Définissez la vitesse (baud rate).
   - Cliquez sur Open pour ouvrir la connexion série.
   
  
### IHM en PyQt5
1. **Installation des dépendances :**
   - Créez un environnement virtuel et activez-le : 
     **python -m venv venv**
     **source venv/bin/activate**  # Sur Windows, utilisez `venv\Scripts\activate`
   - Assurez-vous d'avoir Python 3.x installé.
   - Installez les dépendances en utilisant le fichier `requirements.txt` :tapez `cd ~/Downloads/Connected-Sensor`
     puis `pip install -r requirements.txt` 
   

2. **Lancement de l'IHM :**
   - Assurez-vous que la carte est bien câblée avec le PC et que le capteur est bien lié à la carte via le bus I2C,
     et que vous avez lancé le programme via le débogueur ou via STM32CubeIDE.
   - Naviguez vers le répertoire : `...../Connected-Sensor/IHM`
   - Exécutez le script Python principal : **python3 main.py**
   
   
 
   
        -
## Prise en Main du Capteur et du Projet
Pour une prise en main détaillée du capteur et du projet, veuillez consulter le document `Guide_Prise_en_Main.pdf` dans le répertoire `documentation`.
Une démonstration du projet est également disponible sous forme de vidéo dans le répertoire `Video` (fichier `Demo.mp4`).

## Diagramme de Gantt
Le diagramme de Gantt détaillant la planification du projet est disponible dans le fichier `gantt.pdf` situé dans le répertoire `documentation`.






