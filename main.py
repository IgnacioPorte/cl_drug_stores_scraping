
import os
import threading

def main():
    for file in os.listdir():
        if file.endswith(".py") and file != "main.py":
            t = threading.Thread(target=os.system, args=(f"python {file}",))
            t.start()

if __name__ == "__main__":
    main()