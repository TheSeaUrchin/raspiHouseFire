#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

fswebcam -r 650x650 --no-banner $DATE.jpg

export NEW_IMAGE = $DATE.jpg