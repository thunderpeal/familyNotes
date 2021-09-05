# GroupNotes
Notes service with chat elements using PostgreSQL

Welcome to GroupNotes - a mini scrapbook-based social network!    

The principle of work is based on the ability to create many boards with notes and share them with colleagues, family, friends, whoever else! 

![Alt text](/screenshots/login.png?raw=true "Optional Title")

![Alt text](/screenshots/signup.png?raw=true "Optional Title")

By default, you have one whiteboard - for personal notes. However, you can join a group or create one yourself and invite people - a separate board will be created for each group.    

When adding notes, you can specify to which group or to which user from your groups you want to send it, or you can make it personal without selecting anything. All notes sent to the group will be displayed on a separate tab, which can be selected from the drop-down menu at the top. All notes sent to a specific user will be displayed on that user's personal board. Thus, an analogue of private messages is obtained.  

![Alt text](/screenshots/my_notes.png?raw=true "Optional Title")

![Alt text](/screenshots/group_notes.png?raw=true "Optional Title")


A wide range of actions with the group: 
- you can change the name and password if you are an admin. The color of the group notes can be chosen by each user of the group 
- this is the color of the headings of the notes on the group tab. 
- you can exclude users from the group, and then there will be an opportunity to return them - for this there is a special section "Manage ban", in which all blocked users will be stored. 
- you can leave the group, and all joint data will be deleted. If the admin left the group, the admin is randomly selected from the remaining users. If there are none, the group is deleted. 
- -you can delete the group yourself (if you are an admin). In this case, all notes will be deleted, all users will be excluded and the group will be deleted permanently. 

![Alt text](/screenshots/group_management.png?raw=true "Optional Title")
