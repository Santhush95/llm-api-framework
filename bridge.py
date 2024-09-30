# Bridge localhost:8000 port to ngrok public URL
import subprocess
import time
import sys
import json

def ngrok_bridge(port):
    test = subprocess.Popen(f'ngrok http {port}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(10)
    curlOut = subprocess.check_output(['curl',"http://localhost:4040/api/tunnels"],universal_newlines=True)
    time.sleep(1)
    ngrokURL = json.loads(curlOut)['tunnels'][0]['public_url']
    print(ngrokURL)
    print("Command to kill ngrok bridge: taskkill /f /im ngrok.exe")

ngrok_bridge("8000")