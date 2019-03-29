try:
    from todo import app
except:
    import os
    os.system("pip3 install -r reqiurments.txt")

from todo import app

app.run()