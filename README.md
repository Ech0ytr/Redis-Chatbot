# Redis-Chatbot

Introduction
Here is a comprehensive explanation that how to setup the chatbot, what functions does it have, and how to use it with your local environment.
	The chatbot is built based on python functions and Redis, which allows the user to interact with the bot to identify themselves,  subscribe and publish messages in a channel in a Redis, and use special fun commands with the bot. 
	
Setup
The folder structure looks like:
--Miniproject1 (folder)
	-- docker-compose.yml
-- mp1_chatbot.py

 <img width="462" height="237" alt="image" src="https://github.com/user-attachments/assets/9f5608c6-cd4d-4202-9f52-952c418c5eff" />

Here is the docker-compose.yml file, which allows us to build two containers in docker, one for Redis and the other for python based on Redis. In this project, we use Redis as our database and it’s smart enough to build a database for subscribing and publishing. Please make sure we change the path with red mark before the colon to the folder where the python file was inside, or the compose up will be failed.
The mp1_chatbot.py file is basically where we realize all the functions of chatbot with python based on Redis. I will show the contents inside the python file later. 
To setup, first open our terminal and use ‘cd’ to direct to the folder with the docker-compose.yml inside, now use docker ps to check if any other containers are using myredis/slim-python services, please kill those containers if they do. 

 <img width="468" height="157" alt="image" src="https://github.com/user-attachments/assets/6f3c1eb7-4128-4fda-bcb7-eea03589b3c1" />


Now, use ‘docker-compose up’ to build the two containers in docker

<img width="468" height="180" alt="image" src="https://github.com/user-attachments/assets/6793164d-0fcb-4340-85a4-987d622f3720" />

 
And after it was set up, open a new window thru shell -> new window on the top left menu bar. Again, direct to the folder with the .yml and .py file inside.
(Optional: if we want use a monitor inside the Redis to track your action, run ‘docker-compose exec redis redis-cli’ then run ‘monitor’

<img width="468" height="193" alt="image" src="https://github.com/user-attachments/assets/2f37e2cc-6bed-4d13-a9e0-be5bc794b406" />

 
The monitor in Redis will simultaneously record the interactions when the user is using the chatbot like identifying.













Run the chatbot
Now it’s time to run the chatbot! Again, open a new window and use ‘cd’ to direct to the same folder as before. Run the command ‘docker exec -it slim-python bash’ and we will get into the python container with the user ‘root’. 

<img width="468" height="280" alt="image" src="https://github.com/user-attachments/assets/25fe7e70-cff8-4ab6-81dd-bc80325a66be" />

 
Before running the python file, use ‘pip install redis’ to ensure Redis package has been installed into the container so that the python file can work correctly. 

<img width="468" height="137" alt="image" src="https://github.com/user-attachments/assets/ce589163-df3b-497d-9ab8-8c5833e30af6" />

Now, run ‘python mp1_chatbot.py’ to run the python file.
 
<img width="468" height="266" alt="image" src="https://github.com/user-attachments/assets/0d9072b5-0564-4c08-b23a-9707401f1c35" />


We will see the introduction of the bot and options that provided to the user. As soon as we run the python file, the monitor in another window has recorded some default insert into the Redis that already initiated in the python file 
 
<img width="468" height="131" alt="image" src="https://github.com/user-attachments/assets/95175e23-3c8b-4289-bd13-d11cf8e3349b" />

 <img width="468" height="247" alt="image" src="https://github.com/user-attachments/assets/aef0df2a-ece9-4b44-b6b0-36fed883ae44" />


Now back to these options, we can first identify ourselves  with option1. In this way, we are required to enter their usernames, ages, genders and locations step by step. I don’t set a limitation here for any string or integers input since it’s just a beta version. In the future version, I may add a string mandatory restriction on the username, gender and location, integer mandatory on age, and maybe more detailed like input length limits. Again, monitor in Redis captured this and recorded. In the following commands, I will just use ‘Monitor Records’ and a screenshot to show the monitor track. 
Monitor Records:
 
 <img width="468" height="65" alt="image" src="https://github.com/user-attachments/assets/d5480d06-4c13-4df1-a6c8-70db9db49e1f" />

<img width="434" height="220" alt="image" src="https://github.com/user-attachments/assets/bd095275-c7a8-4582-b03d-8cca05bbb8b7" />

After identifying, we can join a channel if we are not in one with using option 2. We will need to input the channel name we want to join, and the chatbot will say we’ve successfully joined and listened to a certain channel.

 <img width="468" height="183" alt="image" src="https://github.com/user-attachments/assets/7b9f5fd7-08f7-4cb5-bd8c-5748c7fb4950" />


Monitor Records: 

<img width="468" height="45" alt="image" src="https://github.com/user-attachments/assets/fefdbed6-bafb-475f-8803-9413ac299367" />


After we joined a channel like ‘channel1’ here, we can listen to messages that anyone send to this channel. 

And of course, since we can join, we can also leave the channel. Here, we choose option 3, and enter a channel name that we joined before, here I use two shell windows for two users. One subscribe to channel1 and the other send a ‘hello’ message to channel1.
 
<img width="468" height="216" alt="image" src="https://github.com/user-attachments/assets/658fad3b-dde2-4c6a-88d9-43764356882e" />


Monitor Records:
 <img width="468" height="131" alt="image" src="https://github.com/user-attachments/assets/f88c0a43-b52e-4d77-9e6a-45a35194d513" />


Similar to the previous 2 options, we can choose the option 4 to send a message to a channel. We can enter the channel name, and the input the message to send a message to the channel. 
<img width="468" height="164" alt="image" src="https://github.com/user-attachments/assets/99ecccf6-3e7c-4179-8995-825fda102fa7" />


Monitor Records: 
<img width="468" height="25" alt="image" src="https://github.com/user-attachments/assets/d346760e-afbb-4e34-bca3-130ee6def345" />


Now, move onto option 5, we just enter the usernames that have been identified before to see in the information of that user.

 <img width="468" height="189" alt="image" src="https://github.com/user-attachments/assets/de99395c-65e2-47a2-ad12-d09caa78b606" />


Monitor Records:
 <img width="468" height="22" alt="image" src="https://github.com/user-attachments/assets/acbf4461-d83e-4e23-9040-216bf69b2496" />


And for option 6, it includes some special commands: 1) !help: This command can give the us a full introduction of the the 4 special commands. 2) !weather: This command returns us with the weather condition based on the city name we input (It only supports Shanghai, Seattle and Nashville for the current input). 3) !fact: This command returns a random fun fact to us. 4) !whoami: Like option 5, it returns the info of the current user after identifying.

 <img width="468" height="193" alt="image" src="https://github.com/user-attachments/assets/32bb47aa-73f5-4e58-b240-348c473b19d4" />

<img width="468" height="180" alt="image" src="https://github.com/user-attachments/assets/7c93f527-ae6e-48e6-a543-5595bcf2944c" />

<img width="468" height="159" alt="image" src="https://github.com/user-attachments/assets/6b339d3f-4a29-46a8-b34a-91c617885404" />

 <img width="468" height="193" alt="image" src="https://github.com/user-attachments/assets/b5d8441f-8335-4f72-a21e-074a974d98a6" />

 


 

Monitor Records:
<img width="468" height="41" alt="image" src="https://github.com/user-attachments/assets/f8e4af27-2e56-449f-a551-985676ce7b33" />

 

And here are the screenshots of the output for at 3 different user inputs to the bot: 
Toy uses option 4 to send ‘hello’ to channel1
 <img width="468" height="23" alt="image" src="https://github.com/user-attachments/assets/ea735e01-a2b3-4d21-84dc-db9d76409be2" />


Sol uses option 6: !whoami to get the info about herself.
 <img width="468" height="26" alt="image" src="https://github.com/user-attachments/assets/255e92c5-2f26-4891-a560-ee8ef78cb349" />


Echo uses option 5 to get info about Sol
 <img width="468" height="24" alt="image" src="https://github.com/user-attachments/assets/9ab9efd8-269c-4c3b-b8ac-bd078d94d70d" />


Extra Special functions:
Here are some special functions based on the beta version.

1.	Add the function that allows the user to subscribe multiple channels: Now, users are allowed to listen to multiple channels at the same time. For example, if I’m in channel1 and I want to listen from channel2, I don’t have to leave channel1 then join channel2. Instead, just join channel2 now, and the user can listen to the message from channel2. Besides, users can now ask the chatbot to list out all the subscribed channel.
 
 <img width="468" height="336" alt="image" src="https://github.com/user-attachments/assets/917b55bf-e400-4310-a5dc-b22b93cc97be" />
<img width="468" height="229" alt="image" src="https://github.com/user-attachments/assets/f2689c93-12c9-42dd-acb0-8b3e2e438c42" />


2.	Knowledge test is available for the users. There are some simple but fun questions in the quiz, and users can get 10 points for answering correctly for each. Besides, users can check their own points, or they can also check the leaderboard, which allows them to see their names over there!
 
 <img width="275" height="376" alt="image" src="https://github.com/user-attachments/assets/d8769668-119d-4eb9-9732-cf62e78d9640" />
<img width="426" height="602" alt="image" src="https://github.com/user-attachments/assets/4c109862-ab18-45f5-b886-e65c1b496500" />


Summary
	Here is all the detailed setup and commands/functions for this chatbot. Hope you have fun with it!

Additional information:
	There are some parts that I used GenAi to support with. They are all the comments and the extra function for subscribing multiple channels, and the code for the knowledge quiz part.

<img width="498" height="653" alt="image" src="https://github.com/user-attachments/assets/bde0b8cd-c953-4b89-93c0-da68ac4e47dd" />
