import subprocess
import tkinter as tk
from tkinter import messagebox
import re

#Tkinter for warning message
root = tk.Tk()

# Installing libraries from requirements.txt

result = subprocess.run("pip install -r requirements.txt", shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print(result.stdout)
else:
    print(result.stderr)

# Checking if Ollama is installed

result_ollama = subprocess.run("ollama", shell=True, capture_output=True, text=True)

if result_ollama.returncode != 0:
    messagebox.showwarning("Missing required tool", "Please, Install Ollama on https://ollama.com/download")
    # root.mainloop()
else:
    pass

# Checking if the LLM is installed

regex_pattern = r"\bllama2\b"

result_ollamaList = subprocess.run("ollama list", shell=True, capture_output=True, text=True)

if re.search(regex_pattern, result_ollamaList.stdout):
    print("llama 2 is already installed")
else:
    print("Installing llama 2...")
    subprocess.run("ollama pull llama2", shell=True, capture_output=True, text=True)


# Execute main.py
subprocess.run("python -m chainlit run main.py", shell=True, capture_output=True, text=True)
print("App Running...")
