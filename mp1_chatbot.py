import redis
import json
import random
import threading
import time

class Chatbot:
    def __init__(self, host='redis', port=6379):
        # Initialize Redis connection and chatbot state
        self.client = redis.StrictRedis(host=host, port=port)
        self.pubsub = self.client.pubsub()
        self.username = None
        self.bot_channel = "chatbot"
        
        # Multi-channel support
        self.active_channels = set()
        self.listening_thread = None
        self.stop_listening = False

        # Initialize weather data in Redis
        self.client.hset("weather:Shanghai", mapping={
            "temperature": "35 Celsius Degree",
            "condition": "Sunny",
            "humidity": "30%"
        })
    
        self.client.hset("weather:Seattle", mapping={
            "temperature": "15 Celsius Degree", 
            "condition": "Rainy",
            "humidity": "80%"
        })

        self.client.hset("weather:Nashville", mapping={
            "temperature": "30 Celsius Degree", 
            "condition": "Sunny",
            "humidity": "20%"
        })

        # Initialize fun facts in Redis list
        self.client.lpush("facts", "No number before 1,000 contains the letter A.")
        self.client.lpush("facts", "There were active volcanoes on the moon when dinosaurs were alive.")
        self.client.lpush("facts", "Sudan has more pyramids than any country in the world.")

        # Initialize quiz system
        self.init_quiz_questions()

    def init_quiz_questions(self):
        """Store quiz questions in Redis hashes"""
        questions = [
            {"question": "What state is Nashville in?", "answer": "Tennessee", "category": "geography"},
            {"question": "What is the capital of France?", "answer": "Paris", "category": "geography"},
            {"question": "How many continents are there?", "answer": "7", "category": "geography"},
            {"question": "What planet is known as the Red Planet?", "answer": "Mars", "category": "science"},
            {"question": "What gas do plants absorb from the atmosphere?", "answer": "Carbon dioxide", "category": "science"},
            {"question": "What is 8 x 7?", "answer": "56", "category": "math"},
            {"question": "What year did World War II end?", "answer": "1945", "category": "history"},
            {"question": "Who wrote Romeo and Juliet?", "answer": "Shakespeare", "category": "literature"},
            {"question": "What is the largest ocean on Earth?", "answer": "Pacific", "category": "geography"},
            {"question": "How many sides does a triangle have?", "answer": "3", "category": "math"}
        ]
        
        # Store each question as a Redis hash
        for i, q in enumerate(questions, 1):
            question_key = f"quiz:question:{i}"
            self.client.hset(question_key, mapping=q)
            
        # Store total question count
        self.client.set("quiz:total_questions", len(questions))

    def introduce(self):
        """Display chatbot introduction and available commands"""
        intro = """
        Hello! I'm your friendly Redis chatbot.
        Here are the commands you can use:
        !help: List of commands
        !weather <city>: Weather update
        !fact: Random fun fact
        !whoami: Your user information
        """
        print(intro)

    def identify(self, username, age, gender, location):
        """Store user information in Redis and initialize quiz score"""
        user_key = f"user:{username}"
        self.client.hset(user_key, mapping={
            "name": username,
            "age": age,
            "gender": gender,
            "location": location
        })
        
        # Initialize quiz score for new users
        score_key = f"user:{username}:quiz_score"
        if not self.client.exists(score_key):
            self.client.set(score_key, 0)
            
        self.username = username

    def get_user_info(self, user):
        """Retrieve user information from Redis"""
        user_key = f"user:{user}"
        return self.client.hgetall(user_key)

    def _listen_to_channels(self):
        """Background thread to listen for messages from all subscribed channels"""
        while not self.stop_listening:
            try:
                message = self.pubsub.get_message(timeout=1.0)
                if message and message['type'] == 'message':
                    try:
                        # Parse JSON message
                        msg_data = json.loads(message['data'])
                        channel = message['channel'].decode('utf-8')
                        print(f"\nReceived message from channel [{channel}] - {msg_data['from']}: {msg_data['message']}")
                        print("Enter your choice: ", end="", flush=True)
                    except json.JSONDecodeError:
                        # Handle raw text messages
                        channel = message['channel'].decode('utf-8')
                        raw_message = message['data'].decode('utf-8')
                        print(f"\nReceived raw message from channel [{channel}]: {raw_message}")
                        print("Enter your choice: ", end="", flush=True)
            except Exception as e:
                if not self.stop_listening:
                    print(f"Error in listener: {e}")
                break

    def join_channel(self, channel):
        """Subscribe to a channel and start background listener"""
        try:
            if channel in self.active_channels:
                print(f"Already in channel: {channel}")
                return
                
            self.pubsub.subscribe(channel) 
            self.active_channels.add(channel)
            print(f"Joined and listening to channel: {channel}")

            # Start background thread if not already running
            if self.listening_thread is None or not self.listening_thread.is_alive():
                self.stop_listening = False
                self.listening_thread = threading.Thread(target=self._listen_to_channels, daemon=True)
                self.listening_thread.start()
                
        except Exception as e:
            print(f"Error joining channel: {e}")

    def leave_channel(self, channel):
        """Unsubscribe from a specific channel"""
        try:
            if channel not in self.active_channels:
                print(f"You're not in channel: {channel}")
                return
                
            self.pubsub.unsubscribe(channel)
            self.active_channels.remove(channel)
            print(f"Left channel: {channel}")
            
            # Stop listening if no channels remain
            if not self.active_channels:
                self.stop_listening = True
                if self.listening_thread and self.listening_thread.is_alive():
                    self.listening_thread.join(timeout=2)
                print("Stopped listening (no active channels)")
                
        except Exception as e:
            print(f"Error leaving channel: {e}")

    def list_channels(self):
        """Display currently active channels"""
        if self.active_channels:
            print(f"Active channels: {', '.join(self.active_channels)}")
        else:
            print("No active channels")

    def send_message(self, channel, message):
        """Publish a JSON message to a channel"""
        message_obj = {
            "from": self.username,
            "message": message
        }
        self.client.publish(channel, json.dumps(message_obj))

    def process_commands(self, message):
        """Process chatbot commands starting with !"""
        if message.startswith("!help"):
            print("Here is a list of available commands: ")
            print("!weather: This function provides the weather for a city you chose, use '!weather + city_name' to run the command (Only Shanghai, " \
            "Seattle and Nashville is available for now)")
            print("!fact: This function provides a fun fact!")
            print("!whoami: This function provide information about a user based on his/her username!")  
              
        elif message.startswith("!weather"):
            # Get weather data from Redis hash
            parts = message.split()
            if len(parts) > 1:
                city = parts[1]
            
                weather_key = f"weather:{city}"
                weather_data = self.client.hgetall(weather_key)
                
                if weather_data:
                    temp = weather_data[b'temperature'].decode('utf-8')
                    condition = weather_data[b'condition'].decode('utf-8') 
                    humidity = weather_data[b'humidity'].decode('utf-8')
                    
                    print(f"Weather in {city}:")
                    print(f"Temperature: {temp}")
                    print(f"Condition: {condition}")
                    print(f"Humidity: {humidity}")
                else:
                    print("City not found.")

        elif message.startswith("!fact"):
            # Get random fact from Redis list
            length = self.client.llen("facts")
            rand_ind = random.randint(0, length-1)
            fact = self.client.lindex("facts", rand_ind)
            print(fact.decode('utf-8')) 

        elif message.startswith("!whoami"):
            # Display current user's information
            user_key = f"user:{self.username}"
            user_data = self.client.hgetall(user_key)
            for key, value in user_data.items():
                print(f"{key.decode('utf-8')}: {value.decode('utf-8')}")

    def take_quiz(self):
        """Present a random quiz question and handle scoring"""
        if not self.username:
            print("Please identify yourself first!")
            return
            
        total_questions = int(self.client.get("quiz:total_questions") or 0)
        if total_questions == 0:
            print("No quiz questions available.")
            return
            
        # Select random question
        question_id = random.randint(1, total_questions)
        question_key = f"quiz:question:{question_id}"
        question_data = self.client.hgetall(question_key)
        
        if not question_data:
            print("Error loading question.")
            return
            
        # Extract question data
        question = question_data[b'question'].decode('utf-8')
        correct_answer = question_data[b'answer'].decode('utf-8').lower()
        category = question_data[b'category'].decode('utf-8')
        
        # Present question and get answer
        print(f"\nQuiz Question ({category}):")
        print(f"Q: {question}")
        user_answer = input("Your answer: ").lower().strip()
        
        # Check answer and update score
        if user_answer == correct_answer:
            print("Correct! +10 points")
            score_key = f"user:{self.username}:quiz_score"
            current_score = int(self.client.get(score_key) or 0)
            new_score = current_score + 10
            self.client.set(score_key, new_score)
            
            # Update leaderboard
            self.client.zadd("quiz:leaderboard", {self.username: new_score})
        else:
            print(f"Incorrect. The correct answer is: {question_data[b'answer'].decode('utf-8')}")

    def view_my_score(self):
        """Display current user's quiz score"""
        if not self.username:
            print("Please identify yourself first!")
            return
            
        score_key = f"user:{self.username}:quiz_score"
        score = int(self.client.get(score_key) or 0)
        print(f"Your quiz score: {score} points")

    def view_leaderboard(self):
        """Display top 10 quiz scores"""
        leaderboard = self.client.zrevrange("quiz:leaderboard", 0, 9, withscores=True)
        
        if not leaderboard:
            print("No quiz scores yet!")
            return
            
        print("\nQuiz Leaderboard (Top 10):")
        print("-" * 30)
        for i, (username, score) in enumerate(leaderboard, 1):
            username = username.decode('utf-8')
            print(f"{i}. {username}: {int(score)} points")

    def quiz_menu(self):
        """Quiz submenu for taking quizzes and viewing scores"""
        while True:
            print("\nKnowledge Quiz Menu:")
            print("1: Take a quiz question")
            print("2: View my score")
            print("3: View leaderboard")
            print("4: Back to main menu")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                self.take_quiz()
            elif choice == "2":
                self.view_my_score()
            elif choice == "3":
                self.view_leaderboard()
            elif choice == "4":
                break
            else:
                print("Invalid choice, please try again")

    def direct_message(self, message):
        """Send direct message to bot channel and process commands"""
        message_obj = {
            "from": self.username,
            "message": message
        }
        self.client.publish(self.bot_channel, json.dumps(message_obj))

        if message.startswith("!"):
            self.process_commands(message)

if __name__ == "__main__":
    bot = Chatbot()
    bot.introduce()

    # Main menu loop
    while True:
        print("\nOptions:")
        print("1: Identify yourself")
        print("2: Join a channel")
        print("3: Leave a channel")
        print("4: Send a message to a channel")
        print("5: Get info about a user")
        print("6: Chatbot special command!")
        print("7: List active channels")
        print("8: Knowledge Quiz")
        print("9: Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # User registration/identification
            username = input("Enter username: ")
            age = input("Enter age: ")
            gender = input("Enter gender: ")
            location = input("Enter location: ")
            bot.identify(username, age, gender, location)

        elif choice == "2":
            # Join a channel for messaging
            channel = input("Enter channel name to join: ")
            bot.join_channel(channel)

        elif choice == "3":
            # Leave a specific channel
            if bot.active_channels:
                bot.list_channels()
                channel = input("Enter channel name to leave: ")
                bot.leave_channel(channel)
            else:
                print("You're not in any channels")

        elif choice == "4":
            # Send message to a channel
            channel = input("Enter channel name to send message: ")
            message = input("Enter your message: ")
            bot.send_message(channel, message)

        elif choice == "5":
            # Lookup user information
            username = input("Enter username to get info about: ")
            user_info = bot.get_user_info(username)
            for key, value in user_info.items():
                print(f"  {key.decode('utf-8')}: {value.decode('utf-8')}")  

        elif choice == "6":
            # Execute chatbot commands
            command = input("Enter bot command (!help, !weather <city>, !fact, !whoami): ")
            bot.process_commands(command)

        elif choice == "7":
            # Display active channels
            bot.list_channels()

        elif choice == "8":
            # Enter quiz menu
            bot.quiz_menu()

        else: 
            # Clean up and exit
            if bot.active_channels:
                bot.stop_listening = True
                if bot.listening_thread and bot.listening_thread.is_alive():
                    bot.listening_thread.join(timeout=2)
            break