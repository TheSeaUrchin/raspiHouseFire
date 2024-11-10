#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

fswebcam --no-banner $DATE.jpg

export NEW_IMAGE = $DATE.jpg