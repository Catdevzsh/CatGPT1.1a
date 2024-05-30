# CatGPT1.1a
V1
CatGPT 1.1 [C] Flames AI
Welcome to CatGPT 1.1 [C] Flames AI! This project is a sophisticated chatbot application designed to provide an engaging and interactive experience. CatGPT is built using Python's Tkinter library for the graphical user interface and incorporates threading and subprocess management to handle various tasks.

Features
Interactive Chat Interface: Communicate with CatGPT through a user-friendly graphical interface.
Command-Based Task Management: Use commands to generate agents, create code, and manage tasks.
Automated Code Generation: Continuously generate and execute code based on provided descriptions.
Agent Mode: Create and manage multiple agents to handle different tasks.
Autorun Mode: Automatically generate and save code until stopped.
Execution Output Display: View the output of executed code directly within the chat interface.
Installation
Prerequisites
Python 3.6 or higher
Required Python libraries:
tkinter
requests
threading
queue
json
Clone the Repository
bash
Copy code
git clone https://github.com/Catdevzsh/CatGPT1.1a.git
cd CatGPT1.1a
Install Dependencies
Ensure you have all the required dependencies installed:

bash
Copy code
pip install requests
Usage
Running the Application
Run the following command to start the CatGPT application:

bash
Copy code
python3 chat_app.py
Interface Overview
Chat Window: Displays the conversation between the user and CatGPT.
Input Box: Type your messages and commands here.
Send Button: Click to send your message or command.
Available Commands
/dream <task>: Generate a new agent for the specified task.
/code <description>: Generate code based on the given description.
/autorun <description>: Continuously generate code and save it to a folder until /stop is issued.
/stop: Stop the autorun mode.
test: Test command to check functionality.
Example Usage
Generate an Agent:

plaintext
Copy code
/dream Create a new agent to handle data processing.
Generate Code:

plaintext
Copy code
/code Generate a Python script to sort a list of numbers.
Activate Autorun Mode:

plaintext
Copy code
/autorun Generate Python scripts to solve various problems.
Stop Autorun Mode:

plaintext
Copy code
/stop
Customization
Changing Button Colors
To change the appearance of the "Send" button to a dark matrix green color with a blackish gray hue, the following properties are adjusted:

python
Copy code
self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message, font=("Helvetica", 14), background="#006400", foreground="#2F4F4F")
Additional Customizations
Feel free to modify the source code to customize the appearance and functionality to your liking. The main file to edit is chat_app.py.

Contributing
We welcome contributions! If you have suggestions for improvements or new features, feel free to create an issue or submit a pull request.

License
This project is licensed under the MIT License.

Contact
For any questions or inquiries, please contact CatDevZSH at [contathaltmannworks@gmail.com].

Enjoy using CatGPT 1.1 [C] Flames AI!
