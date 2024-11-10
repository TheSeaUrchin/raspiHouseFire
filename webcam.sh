#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

fswebcam --no-banner $DATE.jpg

echo "$DATE.jpg"