import numpy as np
import cv2

# boundary for light color
redBoundary = ([148, 9, 192], [167, 191, 255])
sizeThreshHold = 50


def processImage(fileName):
	image = cv2.imread(fileName)
	# convert to hsv
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# set boundaries
	lower, upper = redBoundary
	lower = np.array(lower)
	upper = np.array(upper)

	# apply mask to colors in range
	mask = cv2.inRange(hsv, lower, upper)
	count = cv2.countNonZero(mask)
	print(count)

	''' Image Output '''

	output = cv2.bitwise_and(image, image, mask=mask)
#	cv2.imwrite('newImage.jpg', output)
	# cv2.imshow("OG",image)
	# cv2.imshow("images", output)
	# cv2.waitKey(0)

	return count > sizeThreshHold

# processImage('imageName.jpg')