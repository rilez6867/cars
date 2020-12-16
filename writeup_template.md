# **Finding Lane Lines on the Road** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file. But feel free to use some other method and submit a pdf if you prefer.

---

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[image1]: ./examples/grayscale.jpg "Grayscale"

---

### Reflection

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

1.I applied grayscale to the input image which is needed to get  canny edge detection.

2. I then applied the canny image detector to show me the images edges. Canny edge detection  uses the horizontal and vertical gradients of the pixel values of an image to detect edges within the image.

3. I then masked out everything in the image to only show us the road lines that I care about. I did this by making a region of interest and removing all other pixels that are not in the region I care about.

4. I then used the hough transformation method to identify lines which indicate lane lines in the image  and by using this method, I can find lines from the pixel outputs of the canny edge detection output to connect all the lines in the picture.

5. The hough transform shows me small lines based on the intersections in hough . Now, with this information I can connect both the right line and the left line lane to form a full lane line without any gaps in between

I did this by separating the  lines into two groups, one with a positive gradient and the other with a negative gradient. 

I then took the average gradient and intercept values for each group and made our whole lane lines from there. The lane lines are then extrapolated to the edge detected pixel with the minimum y-axis coordinate and the pixel with the maximum y-axis coordinate.

6. Lastly I  overlaped the extrapolated lines to the input image. I did this by adding a weight value to the original image based on the detected lane line position.




![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline




One potential shortcoming is my lines dont always stay on the lane lines in the video, they sometimes move away from where they are supposed to be.

The algorithm for the lane lines needs to be a bit faster then it is now, it seems to sometimes lag instead of being in real time.I would like to find a way to imporve my algorithm to be faster and use less computing power then it does currently.


### 3. Suggest possible improvements to your pipeline

I would like to simulate my car in bad wheather conditions so I can see how the car would react to wind rain and snow in terms of being reliable and safe for both the people in the car and the people on the road as well. 

An imporvement would also be to test the algorithm on winding roads to see if it stays with the car the whole time instead of going all over the place.  I mentioned earlier as time goes on and the road gets more difficult it seems to struggle to adapt to the turns and potential hazards that might show up while driving. 
