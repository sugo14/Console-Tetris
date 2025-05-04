import subprocess

if __name__ == "__main__":
    subprocess.Popen(["start", "cmd", "/k", "python program.py"], shell=True)
