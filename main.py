import requests
import subprocess
import threading
import time
import queue
import os

serverName = "ismyhouseonfire.tech"
endpoint = "upload"
imagePath = "./fire.jpg"
url = "http://" + serverName + "/" + endpoint
threadCap = 2
numThreads = 0

# Very safe code
ID = "randomID"
code = "51413"


threads = queue.Queue()
def run():
    global numThreads
    while True:
        imageName = getImage()
        if numThreads >= threadCap:
            firstThread = threads.get()
            # wait for first thread in queue to finish
            firstThread.join()
        else:
            numThreads += 1

        # add upload thread to queue
        newThread = threading.Thread(target=upload, args=[imageName])
        threads.put(newThread)
        newThread.start()

        time.sleep(1)


def getImage():
    # might change to subprocess, depends on how long upload takes compared to image capture
    os.system("./webcam.sh")
    imageFile = os.environ['NEW_IMAGE']
    return imageFile


def upload(imageFile):
    files = {
        'id': ID,
        'file': (imageFile, open(imagePath, 'rb'))
    }
    response = requests.post(url, files=files)


if __name__ == '__main__':
    run()

