In addition to the two folders "icons" and "images", this folder should contain 
two json files. The first file "app_settings.json" is used for saving the user
specific settings for the application. The second file "subreddits.json" is used 
for saving the subreddit configurations that the user are getting images based on, 
specifically the subreddit name, the time limit and the number of images for 
each added subreddit.

The file "app_settings.json" should have the following format:
```
{
  "interval": MinutesBetweenBackgroundChange
}
```

Initially the file "subreddits.json" should have the following format:
```
[]
```
When subreddits are added through the UI, the configurations are saved to this file as shown:
```
[
["Subreddit1", "TimeLimit1", NumberOfImages1],
["Subreddit2", "TimeLimit2", NumberOfImages2]
]
```