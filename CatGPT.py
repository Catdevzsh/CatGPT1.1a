import tkinter as tk
from tkinter import scrolledtext, filedialog
import requests
import threading
import os
import time
import subprocess
from queue import Queue
import json

class ChatApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CATGPT 1.1 [C] Flames AI")
        self.geometry("800x600")
        self.resizable(True, True)
        self.configure(background="#F0F0F0")
        self.create_widgets()
        self.init_chat_history()
        self.init_crewai()
        self.show_cli_commands()
        self.agent_mode = True
        self.autorun_mode = False
        self.agents = {}
        self.output_folder = ""
        self.task_queue = Queue()
        self.task_thread = None

    def create_widgets(self):
        self.output_frame = tk.Frame(self, background="#FFFFFF")
        self.output_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(self.output_frame, state="disabled", wrap=tk.WORD, font=("Helvetica", 14))
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.input_frame = tk.Frame(self, background="#F0F0F0")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.input_text = tk.Text(self.input_frame, height=3, font=("Helvetica", 14))
        self.input_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message, font=("Helvetica", 14), background="#006400", foreground="#2F4F4F")
        self.send_button.pack(side=tk.RIGHT)

    def init_chat_history(self):
        self.update_output_text("CatGPT: Hello! I'm CatGPT. I'm here to assist you and learn from our conversation!\n\n")

    def init_crewai(self):
        bios_message = """
        BIOS Version: CREWAI 1.0.0
        Initializing CREWAI...
        System Check: OK
        AI Modules: Loaded
        Ready to Assist!
        """
        self.update_output_text(f"CatGPT: {bios_message}\n\n")

    def show_cli_commands(self):
        commands = """
        Available Commands:
        /dream <task> - Generate a new agent for the specified task
        /code <description> - Generate code based on the given description
        /autorun <description> - Continuously generate code and save it to a folder until /stop is issued
        /stop - Stop the autorun mode
        test - Test command to check functionality
        """
        self.update_output_text(f"CatGPT: {commands}\n\n")

    def send_message(self):
        user_message = self.input_text.get("1.0", tk.END).strip()
        self.input_text.delete("1.0", tk.END)

        if user_message:
            self.update_output_text(f"User: {user_message}\n")

            if user_message.lower() == "test":
                self.update_output_text("CatGPT: test\n\n")
                self.after(500, lambda: self.update_output_text("CatGPT: :) ping\n\n"))
            elif user_message.lower().startswith("/dream"):
                task_description = user_message[len("/dream"):].strip()
                self.generate_agent(task_description)
            elif user_message.lower().startswith("/code"):
                code_description = user_message[len("/code"):].strip()
                self.generate_code(code_description)
            elif user_message.lower().startswith("/autorun"):
                code_description = user_message[len("/autorun"):].strip()
                self.start_autorun(code_description)
            elif user_message.lower() == "/stop":
                self.stop_autorun()
            else:
                self.send_to_api(user_message)

    def generate_agent(self, task_description):
        agent_id = len(self.agents) + 1
        agent_name = f"Agent-{agent_id}"
        agent_info = f"Agent ID: {agent_id}\nTask: {task_description}\nStatus: Ready\n"
        self.agents[agent_id] = {'name': agent_name, 'task': task_description, 'status': 'Ready'}
        self.update_output_text(f"CatGPT: Generated new agent.\n{agent_info}\n")

    def generate_code(self, code_description):
        self.send_to_api(code_description)

    def send_to_api(self, text):
        url = "http://localhost:1234/generate"
        headers = {'Content-Type': 'application/json'}
        data = {'text': text}

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            ai_response = response_data['generated_text']
            self.update_output_text(f"CatGPT: {ai_response}\n\n")
        except Exception as e:
            self.update_output_text(f"Error: {str(e)}\n\n")

    def start_autorun(self, code_description):
        self.output_folder = filedialog.askdirectory()
        if not self.output_folder:
            self.update_output_text("CatGPT: No output folder selected. Autorun mode not activated.\n\n")
            return

        self.autorun_mode = True
        self.update_output_text(f"CatGPT: Autorun mode activated. Generating code based on: {code_description}\n\n")
        self.autorun_code_description = code_description

        if not self.task_thread or not self.task_thread.is_alive():
            self.task_thread = threading.Thread(target=self.autorun_loop)
            self.task_thread.daemon = True
            self.task_thread.start()

    def stop_autorun(self):
        self.autorun_mode = False
        self.task_queue.put(None)  # Signal the thread to stop
        self.update_output_text("CatGPT: Autorun mode deactivated.\n\n")
        self.after(500, self.quit)  # Close the application after a short delay

    def autorun_loop(self):
        counter = 1
        while self.autorun_mode:
            self.task_queue.put((self.autorun_code_description, counter))
            counter += 1
            time.sleep(5)

        # Process remaining tasks in the queue
        while not self.task_queue.empty():
            task = self.task_queue.get()
            if task is None:
                break
            self.process_task(task)
        
    def process_task(self, task):
        code_description, counter = task
        self.generate_and_save_code(code_description, counter)

    def generate_and_save_code(self, code_description, counter):
        url = "http://localhost:1234/generate"
        headers = {'Content-Type': 'application/json'}
        data = {'text': code_description}

        try:
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            generated_code = response_data['generated_text']
            self.update_output_text(f"CatGPT: Generated code:\n{generated_code}\n\n")
            self.save_code_to_file(generated_code, counter)
            self.execute_code_if_possible(counter)
        except Exception as e:
            self.update_output_text(f"Error: {str(e)}\n\n")

    def save_code_to_file(self, code, counter):
        file_path = os.path.join(self.output_folder, f"generated_code_{counter}.py")  # Assuming Python code
        with open(file_path, "w") as file:
            file.write(code)
        self.update_output_text(f"CatGPT: Saved generated code to {file_path}\n\n")

    def execute_code_if_possible(self, counter):
        file_path = os.path.join(self.output_folder, f"generated_code_{counter}.py")
        try:
            result = subprocess.run(["python3", file_path], capture_output=True, text=True)
            self.update_output_text(f"CatGPT: Execution output:\n{result.stdout}\n{result.stderr}\n\n")
        except Exception as e:
            self.update_output_text(f"Error executing code: {str(e)}\n\n")

    def update_output_text(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")

if __name__ == "__main__":
    app = ChatApp()
    app.mainloop()
