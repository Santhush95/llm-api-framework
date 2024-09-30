# The server will start the model download and will take a while to start up

import subprocess
import time

from ipywidgets import HTML
from IPython.display import display
from IPython import get_ipython


t = HTML(
    value="0 Seconds",
    description = 'Server is Starting Up... Elapsed Time:' ,
    style={'description_width': 'initial'},
)
display(t)

flag = True
timer = 0

try:
    subprocess.check_output(['curl',"localhost:8000"])
    print("test")
    flag = False
except:
    get_ipython().system_raw('uvicorn app:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &')

res = ""

while(flag and timer < 600):
  try:
    subprocess.check_output(['curl',"localhost:8000"])
  except:
    time.sleep(1)
    timer+= 1
    t.value = str(timer) + " Seconds"
    pass
  else:
    flag = False

if(timer >= 600):
  print("Error: timed out! took more then 10 minutes :(")
subprocess.check_output(['curl',"localhost:8000"])