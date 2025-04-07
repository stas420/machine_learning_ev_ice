import platform
import subprocess

dir_check = ""
plt = platform.system()

if "Windows" in plt:
    dir_check = "dir"
elif "Linux" in plt:
    dir_check = "ls -la"
else:
    print(f'Lol, the platform is unknown: {plt}')

run = subprocess.run(dir_check, shell = True, capture_output = True, text = True)
output = run.stdout

if "machine_learning_ev_ice" in output:
    
    if subprocess.run("git pull", shell = True).returncode != 0:
        print(f'Could not pull the repo, sorry :(')
    else:
        print(f'The repo is pulled, should be ok')

else:
    cmd = 'git clone https://github.com/stas420/machine_learning_ev_ice.git'

    if subprocess.run(cmd, shell = True).returncode != 0:
        print(f'Could not clone the repo, sorry :(')
    else:
        print(f'The repo is cloned, should be ok')


    
