import subprocess, pyautogui as pa

path = r"C:\Documents\Project-TAV"

subprocess.run(f'start cmd /K "cd /d {path}"', shell=True)
