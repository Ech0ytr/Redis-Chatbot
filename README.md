# Redis-Chatbot

Introduction
Here is a comprehensive explanation that how to setup the chatbot, what functions does it have, and how to use it with your local environment.
	The chatbot is built based on python functions and Redis, which allows the user to interact with the bot to identify themselves,  subscribe and publish messages in a channel in a Redis, and use special fun commands with the bot. 
	
Setup
The folder structure looks like:
--Miniproject1 (folder)
	-- docker-compose.yml
-- mp1_chatbot.py
 
Here is the docker-compose.yml file, which allows us to build two containers in docker, one for Redis and the other for python based on Redis. In this project, we use Redis as our database and it’s smart enough to build a database for subscribing and publishing. Please make sure we change the path with red mark before the colon to the folder where the python file was inside, or the compose up will be failed.
The mp1_chatbot.py file is basically where we realize all the functions of chatbot with python based on Redis. I will show the contents inside the python file later. 
To setup, first open our terminal and use ‘cd’ to direct to the folder with the docker-compose.yml inside, now use docker ps to check if any other containers are using myredis/slim-python services, please kill those containers if they do. 
 

Now, use ‘docker-compose up’ to build the two containers in docker
 
And after it was set up, open a new window thru shell -> new window on the top left menu bar. Again, direct to the folder with the .yml and .py file inside.
(Optional: if we want use a monitor inside the Redis to track your action, run ‘docker-compose exec redis redis-cli’ then run ‘monitor’
 
The monitor in Redis will simultaneously record the interactions when the user is using the chatbot like identifying.













Run the chatbot
Now it’s time to run the chatbot! Again, open a new window and use ‘cd’ to direct to the same folder as before. Run the command ‘docker exec -it slim-python bash’ and we will get into the python container with the user ‘root’. 
 
Before running the python file, use ‘pip install redis’ to ensure Redis package has been installed into the container so that the python file can work correctly. 
 

Now, run ‘python mp1_chatbot.py’ to run the python file.
 

We will see the introduction of the bot and options that provided to the user. As soon as we run the python file, the monitor in another window has recorded some default insert into the Redis that already initiated in the python file 
 

 

Now back to these options, we can first identify ourselves  with option1. In this way, we are required to enter their usernames, ages, genders and locations step by step. I don’t set a limitation here for any string or integers input since it’s just a beta version. In the future version, I may add a string mandatory restriction on the username, gender and location, integer mandatory on age, and maybe more detailed like input length limits. Again, monitor in Redis captured this and recorded. In the following commands, I will just use ‘Monitor Records’ and a screenshot to show the monitor track. 
Monitor Records:
 
 

After identifying, we can join a channel if we are not in one with using option 2. We will need to input the channel name we want to join, and the chatbot will say we’ve successfully joined and listened to a certain channel.

 

Monitor Records: 

After we joined a channel like ‘channel1’ here, we can listen to messages that anyone send to this channel. 

And of course, since we can join, we can also leave the channel. Here, we choose option 3, and enter a channel name that we joined before, here I use two shell windows for two users. One subscribe to channel1 and the other send a ‘hello’ message to channel1.
 

Monitor Records:
 

Similar to the previous 2 options, we can choose the option 4 to send a message to a channel. We can enter the channel name, and the input the message to send a message to the channel. 

Monitor Records: 

Now, move onto option 5, we just enter the usernames that have been identified before to see in the information of that user.

 

Monitor Records:
 

And for option 6, it includes some special commands: 1) !help: This command can give the us a full introduction of the the 4 special commands. 2) !weather: This command returns us with the weather condition based on the city name we input (It only supports Shanghai, Seattle and Nashville for the current input). 3) !fact: This command returns a random fun fact to us. 4) !whoami: Like option 5, it returns the info of the current user after identifying.

 


 
 


 

Monitor Records:
 

And here are the screenshots of the output for at 3 different user inputs to the bot: 
Toy uses option 4 to send ‘hello’ to channel1
 

Sol uses option 6: !whoami to get the info about herself.
 

Echo uses option 5 to get info about Sol
 

Extra Special functions:
Here are some special functions based on the beta version.

1.	Add the function that allows the user to subscribe multiple channels: Now, users are allowed to listen to multiple channels at the same time. For example, if I’m in channel1 and I want to listen from channel2, I don’t have to leave channel1 then join channel2. Instead, just join channel2 now, and the user can listen to the message from channel2. Besides, users can now ask the chatbot to list out all the subscribed channel.
 
 

2.	Knowledge test is available for the users. There are some simple but fun questions in the quiz, and users can get 10 points for answering correctly for each. Besides, users can check their own points, or they can also check the leaderboard, which allows them to see their names over there!
 
 

Summary
	Here is all the detailed setup and commands/functions for this chatbot. Hope you have fun with it!

Additional information:
	There are some parts that I used GenAi to support with. They are all the comments and the extra function for subscribing multiple channels, and the code for the knowledge quiz part.

<img width="498" height="653" alt="image" src="https://github.com/user-attachments/assets/bde0b8cd-c953-4b89-93c0-da68ac4e47dd" />
