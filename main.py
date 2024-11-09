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
imageCap = 5
numThreads = 0

# Very safe code
ID = "randomID"
code = "51413"


images = queue.Queue()
threads = []
threadSem = threading.Semaphore(0)
prodSem = threading.Semaphore(imageCap)
mutex = threading.Semaphore(1)


def makeThreads():
    for i in range(threadCap):
        newThread = threading.Thread(target=upload)
        newThread.start()
        threads.append(newThread)


def getImage():
    # might change to subprocess, depends on how long upload takes compared to image capture
    #os.system("./webcam.sh")
    os.system("./testCam.sh")
    res = subprocess.run(["./testCam.sh"], capture_output=True, text=True)
    imageFile = res.stdout.strip()
    return imageFile


def upload():
    while True:
        threadSem.acquire()
        with mutex:
            imageFile = images.get()
        files = {
            'id': ID,
            'file': (imageFile, open(imageFile, 'rb'))
        }
        print(f"Uploaded file {imageFile}")
        #response = requests.post(url, files=files)
        time.sleep(3)
        subprocess.Popen(["rm",imageFile])
        prodSem.release()


def run():
    global numThreads
    makeThreads()
    while True:
        prodSem.acquire()
        imageName = getImage()
        with mutex:
            images.put(imageName)
        threadSem.release()
        time.sleep(1)


if __name__ == '__main__':
    run()

