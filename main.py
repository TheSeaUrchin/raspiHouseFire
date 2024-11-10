import requests
import subprocess
import threading
import time
import queue
import os
from ImageProcess import processImage

serverName = "api.ismyhouseonfire.tech"
endpoint = "upload"
imagePath = "./fire.jpg"
url = "http://" + serverName + "/" + endpoint
headers = {"Content-Type": "application/json"}
threadCap = 1
imageCap = 1
numThreads = 0
numFalses = 3
count = 5

# Very safe code
ID = "randomID"
code = "99999"


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
    # os.system("./webcam.sh")
    # os.system("./testCam.sh")
    res = subprocess.run(["./webcam.sh"], capture_output=True, text=True)
    imageFile = res.stdout.strip()
    return imageFile


def upload():
    global count
    while True:
        threadSem.acquire()
        with mutex:
            imageFile, lightOn = images.get()


        files = {
            'code': code,
            'key': "hello",
            'status': str(lightOn).lower()
        }

        response = requests.post(url, headers=headers, json=files)
        if response.status_code != 200:
            print(response)

        else:
            print("Sent Successfully")

        # time.sleep(3)
        #print(f"Uploaded file {imageFile}, lightOn is {lightOn}")
        print(f"light is:{lightOn}")

        subprocess.Popen(["rm",imageFile])
        prodSem.release()


def run():
    global numThreads
    global count
    makeThreads()
    while True:
        prodSem.acquire()
        imageName = getImage()
        lightOn = processImage(imageName)
        print("oldStatus", lightOn)
        
        if lightOn == False and count<5:
            lightOn = True
            count += 1
        elif lightOn == True:
            count = 0
        with mutex:
            images.put((imageName, lightOn))
            #print(f"ImageQueue:{list(images.queue)}")
        threadSem.release()
        time.sleep(1)

def run2():
    while True:
        imageName = getImage()
        lightOn = processImage(imageName)
        files = {
            'code': code,
            'key': "hello",
            'status': str(lightOn).lower()
        }

        response = requests.post(url, headers=headers, json=files)
        if response.status_code != 200:
            print(response)
        else:
            print("Sent Successfully")

        # time.sleep(3)
        # print(f"Uploaded file {imageFile}, lightOn is {lightOn}")
        print(f"light is:{lightOn}")
        os.system(f"rm {imageName}")

        # subprocess.Popen(["rm", imageName])


if __name__ == '__main__':
    run()
