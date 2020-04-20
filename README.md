# Reddit Background Changer
Automatically changes the desktop background to an image from the subreddits of your choice.


## Design
The project is made using an object-oriented design where program execution starts from the **main.py** file. The UI is implemented
in the **resources/mainwindow.ui** file and all UI functionallity is implemented in the **main_window.py** file. The latter connects
all elements of the UI with their corresponding functions. The UI is built around a list containing the subreddits chosen by the user.
This list is implemented in the **subreddit_model.py** file. All functionallity that is related to the list of subreddits, like
getting the images from the subreddits and deleting images, is implemented in this file. Note that this class inherits from
***QAbstractListModel*** which means that we can use it directly as the internal model for the **QListView** that is used in the UI.

Choosing an image and changing the background is handled by the **background_changer.py** file. This class is built around a basic
timer that is used to implement the frequency at which we change the background. The background can also be changed manually through the 
system tray icon which is implemented in the **system_tray.py** file. This file sets up the different actions that are possible when
right-clicking the system tray icon. Finally, the concurrency that ensures that the UI is responsive is implemented in the **worker.py** file.
This concurrency is rather important since without it, the UI would be unresponsive when retrieving images from the given subreddits 
which can be a time consuming task.

## Installation
If you wish to use this application for yourself some setup is required. This application is currently not configured to support
distribution which is why i don't recommend that you use it at this time. It is however not impossible.

The basic folder structure of the project is already complete, all you need to do is to visit the ***configuration/*** and ***data/*** 
folders and follow the instructions given in the internal README.md files. Each folder contains a README file that explains which files are
needed in that folder and how to set them up.

In the configuration folder a config file for reddit API access is needed. 
For more information on how to set up reddit API access see: https://praw.readthedocs.io/en/latest/getting_started/quick_start.html

### Requirements
A conventional requirements file is included which means that all dependencies can be installed by navigating to the project directory and typing the following in your cmd:
```
$ pip install -r requirements.txt
```

## Contributing
This project is currently private and there are no plans to make outside contributions available in the near future.
