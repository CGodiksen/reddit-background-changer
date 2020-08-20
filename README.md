# Reddit Background Changer
Automatically changes the desktop background to an image from the subreddits of your choice.


## Design
The project is made using an object-oriented design where program execution starts from the **main.py** file. The main UI is implemented
in the **resources/mainwindow.ui** file and all UI functionallity related to the main window is implemented in the **main_window.py** file.
The latter connects all elements of the main window UI with their corresponding functions. The main window is built around a list containing the
subreddits chosen by the user. This list is implemented in the **subreddit_model.py** file. All functionallity that is related to the list of subreddits, like
getting the images from the subreddits and deleting images, is implemented in this file. Note that this class inherits from
***QAbstractListModel*** which means that we can use it directly as the internal model for the **QListView** that is used in the UI. The UI for the settings
dialog window is implemented in the **resources/settingsdialog.ui** file and all UI functionallity related to the settings dialog window is implemented in
the **settings_dialog.py** file. This dialog window supports changing the settings which are implemented as a class in the **settings.py** file for increased accessibility throughout the application.

Choosing an image and changing the background is handled by the **background_changer.py** file. This class is built around a basic
timer that is used to implement the frequency at which we change the background. The background can also be changed manually through the 
system tray icon which is implemented in the **system_tray.py** file. This file sets up the different actions that are possible when
right-clicking the system tray icon. Finally, the concurrency that ensures that the UI is responsive is implemented in the **worker.py** file.
This concurrency is rather important since without it, the UI would be unresponsive when retrieving images from the given subreddits 
which can be a time consuming task.

## Graphical user interface
The user interface was created using the Qt framework.
### Main window
![Example of main window](https://i.imgur.com/cQa5CMc.png)

### Settings dialog window
![Example of settings dialog window](https://i.imgur.com/VwRF7mD.png)

## Installation
If you wish to use this application for yourself some setup is required.

In the settings you need to input your own client ID, client secret and user agent which is needed for reddit API access. The application was not designed with 
the intention of distribution, which is why it is necessary for each user to individually set up the reddit API access.
For more information on how to set up reddit API access see: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

### Requirements
A conventional requirements file is included which means that all dependencies can be installed by navigating to the project directory and typing the following in your cmd:
```
$ pip install -r requirements.txt
```
