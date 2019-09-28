# Lane-Detection
A pure image processing algorithm to detect road lanes from videos using OpenCV.

<h2> Dependencies </h2>
<ul>
  <li> Python3 </li>
  <li> OpenCV 3 (used 3.4.1) </li>
</ul>

<h2> Usage </h2>

Clone the repository:
``` sh
$foo@bar: git clone https://github.com/neeldani/Lane-Detection.git
$foo@bar: cd Lane-Detecion
```

Run the python script using:
``` python 
python3 lane-detection.py
```

<h2> Example </h2>

A video frame 

<img src="https://github.com/neeldani/Lane-Detection/blob/master/snapshots/video_frame/400.jpg" width="500">
<br />

1) Extract yellow-white colours using bit masking.

<img src="https://github.com/neeldani/Lane-Detection/blob/master/snapshots/yellow_white/400.jpg" width="500">
<br />

2) Apply edge detection algorithm

<img src="https://github.com/neeldani/Lane-Detection/blob/master/snapshots/canny/400.jpg" width="500">
<br />

3) Extract region of interest (ROI)

<img src="https://github.com/neeldani/Lane-Detection/blob/master/snapshots/roi/400.jpg" width="500">
<br />

4) Apply hough lines and extrapolate the lanes based on the slope and y-intercept

<img src="https://github.com/neeldani/Lane-Detection/blob/master/snapshots/line_img/400.jpg" width="500">
<br />


<h2> Future works </h2>

This is a simple image processing technique that can be enhanced. Further improvements via contributions are welcomed.
