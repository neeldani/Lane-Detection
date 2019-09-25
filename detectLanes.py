'''

Author: Neel Dani

Algorithm:

1) Extract yellow and white colours from the frames using bit masking.

2) Apply an edge detection algorithm, used Canny edge in this case

3) Extract region of interest, which is a parallelo gram having its longer side coincident on the 
   bottom of the frame and the tapering sides long the height of the frames.

4) Apply dilation and erosion to make the edges finer and as a pre-requisite for hough line.

5) Apply hough lines algorithm to join the small edges detected in step 2.

6) Average out the slope of the lines achieved in step 5.

7) Extrapolate the lines along the lanes using the staright line equation.

''' 

import os
import numpy as np
import cv2

def region_of_interest (img) :
	mask = np.zeros_like(img)
	pts = np.array([[150, 720], [530, 460], [750, 460], [1280, 720]])
	pts = pts.reshape((-1, 1, 2))

	if len(img.shape) > 2 :
		count = img.shape[2]
		colour = (255, )*count

	else :
		colour = 255

	cv2.fillPoly(mask, pts = [pts], color=(colour))
	mask_trap = cv2.bitwise_and(img, img, mask = mask)
	return mask_trap

def slope(x1, y1, x2, y2):

	if x1 == x2 :
		if y1 > y2:
			return -99
		else:
			return 99

	else :
		s = (float(y2)-y1)/(x2-x1)
		if s == 0:
			return 0.01
		return s

def avg_lines(lines):

	l_lane = []
	r_lane = []
	l_weight = []
	r_weight = []

	for line in lines :
		for x1, y1, x2, y2 in line :
			s = slope(x1, y1, x2, y2)
			c = y1 - s*x1
			length = np.sqrt((y2-y1)**2 + (x2-x1)**2)

			if s < 0:
				l_lane.append((s, c))
				l_weight.append((length))

			if s > 0:
				r_lane.append((s, c))
				r_weight.append((length))

	if len(l_weight) > 0:
		l_lane = np.dot(l_weight, l_lane)/np.sum(l_weight)
	else:
		None

	if len(r_weight) > 0:
		r_lane = np.dot(r_weight, r_lane)/np.sum(r_weight)
	else:
		None

	return l_lane, r_lane

def get_line(m, c, y1, y2):

	x1 = (int)((y1-c)/m)
	x2 = (int)((y2-c)/m)
	y1 = (int)(y1)
	y2 = (int)(y2)

	return x1, y1, x2, y2

def hough_lines (img, min_length, max_gap, frame):
	lines = cv2.HoughLinesP(img, 1, np.pi/180, 30, np.array([]), min_length, max_gap)

	l_lane, r_lane = avg_lines(lines)
	mask = np.zeros_like(frame)	

	if len(l_lane) > 0:
		 x1_l, y1_l, x2_l, y2_l = get_line(l_lane[0], l_lane[1], img.shape[0], img.shape[0]*0.7)					
		 cv2.line(mask, (x1_l, y1_l), (x2_l, y2_l), (0, 0, 255), 10, cv2.LINE_AA)
		 frame = cv2.addWeighted(frame, 1, mask, 1.0, 0.0)
	else :
		pass


	if len(r_lane) > 0:	
		x1_r, y1_r, x2_r, y2_r = get_line(r_lane[0], r_lane[1], img.shape[0], img.shape[0]*0.7)	
		cv2.line(mask, (x1_r, y1_r), (x2_r, y2_r), (0, 0, 255), 10, cv2.LINE_AA)
		frame = cv2.addWeighted(frame, 1, mask, 1.0, 0.0)
	else:	
		pass

	return frame


def dilation_ersion(img):
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	return img

def extract_colour(img):

	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	white_lower = (0, 0, 240)
	white_upper = (180, 110, 255)
	white = cv2.inRange(hsv, white_lower, white_upper)

	yellow_lower = (20, 100, 100)
	yellow_upper = (30, 255, 255)
	yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
	mask = cv2.bitwise_or(yellow, white)

	hsv_frame = cv2.bitwise_and(hsv, hsv, mask = mask)
	return hsv_frame

s = 'project_video.mp4'
cap = cv2.VideoCapture(s)

while (cap.isOpened()):
	ret, frame = cap.read()

	if ret:
		yellow_white = extract_colour(frame)
		canny = cv2.Canny(yellow_white, 150, 255)
		roi = region_of_interest (canny)
		morph = dilation_ersion(roi)
		line_img = hough_lines(morph, 0, 500, frame)
		cv2.imshow('frame', line_img)
	
	if cv2.waitKey(1) & 0x0FF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()