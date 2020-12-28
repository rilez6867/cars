## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./examples/undistort_output.png "Undistorted"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

I took an image of a checkerboard and the corners on the board are identified and deviations from the expected checkerboard measurements are used to calculate the distortion coefficients. These coefficients are then used to remove  distortion from the image giving a fuller picture of the checkerboard fitting the picture into place. 
![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

I used an image of a lane of two images and compared them side by side. A good  way that we have been taught is to separate and detect objects in the image and use  transforms and gradient strategies to generate a filtered-down thresholded binary image of the picture you are looking at. 
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I applied a perspective transformation to a region of interest in the image of the car on the road.  You pick the area in the image you would like to run the transformation on. I ran the algorithm on the lane lines isolating them from the picture and blacking everything else out so that is the only thing you would focus on in the picture.

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

I used perspective transform on the lane lines to isolate them and make them appear parallel so that it would be easier for the camera on the car to follow the lane lines. I did this by taking a 2D picture and fitting a polynomal bringing out the lane line features in the picture, giving me a good mathmatical representation of the image in terms of it'ss lines.
```

This gave me the following destination points on the image 

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 0.43, .65      | 0, 0        | 
| 0.58, .65      | 1, 0      |
| 0.1, 1         | 0, 1      |
| 1 ,1           | 1, 1        |

I ran the algorithm on a test photo and the lines did in fact appear parallel to where they were before, this is how I know that it worked.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?


I used the sobel technique which is the bread and butter of the canny edge method and it basically takes the derivative of the image in the x or y direction and depending on the picture you get a different outcome depending what kind of lines are in the picture if they are on the X axis or the Y axis. It really does make a difference where the lines are located.

I also used the magnitude gradient to bring out the lines in the picture, basically you take both sobel gradients x and y and calculate the magnitude of the gradients and rescale to 8 bit and then you make a binery image of where the threshold is and this gives you your end result.





#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

You find a  starting point to search for pixels belonging to each lane line. I  used a sliding window search technique that starts from the bottom and iterates all the way to the top of the image, adding pixels it finds to a list. If an acceptable number of pixels are found, the next window will be centred around their average point, that way you are following the path of the pixels throughout the image.

After it  finds the pixels belonging to each lane line, it then puts a polynomial through the points, generating a line of where the lines are in the image.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)


My pipeline video is an advanced lane detector in motion that uses bright color to show you where the car is and also the curved lines in the image. I thought about using bright color because some people might be color blind and they are easier to see for most people . It obviously needs to be tested more for safety before it could ever be used in a test car on the road. 

---



Sometimes the wrong pictures would show up when I was trying to calibrate images, I eventually got all the pictures on the same page so the ones that I wanted to show did.



I would like to find a way for the camera to see clearly enough in rain and snow and fog to drive safely. The Camera is the cheapest option in terms of finding lines compared to expensive senors, this is important because it would make the cars more affordable to a wider range of people instead of people wealthy enough to afford the cars they have now. 
