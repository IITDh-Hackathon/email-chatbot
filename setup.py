import os
from simplegmail import Gmail
import subprocess
import shutil

source_file = 'service_file.txt'
destination_path = '/etc/systemd/system/fetcher_bot.service'

# Copy the contents of the source file to the destination path
shutil.copyfile(source_file, destination_path)

script = [
    "#!/bin/bash",
    "python3 -m venv venv",
    "source venv/bin/activate",
    "pip install -r " + os.getcwd() + "/requirements.txt",
    "python3 "+os.getcwd()+"/services/sync_service.py",
    "sudo systemctl start fetcher_bot.service"
]

script_file_path = "/etc/systemd/system/script.sh"

# Open the script file in write mode
with open(script_file_path, "w") as script_file:
    # Write each command to the file
    for command in script:
        script_file.write(command + "\n")

result = subprocess.run("chmod +x /etc/systemd/system/script.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result1 = subprocess.run("sudo systemctl daemon-reload", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
result2 = subprocess.run("sudo systemctl enable fetcher_bot.service", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



# print(f"Contents of {source_file} copied to {destination_path}")