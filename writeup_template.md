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

My pipeline consisted of several steps. First, the image was converted to grayscale. Second, the image was run through the blur function to reduce image noise and reduce detail so that we can get an almost naked picture of the parts we need to see or in this case the lines and edges in the picture which also utilized the canny function. The canny in this case was used to find the edges and bring them out into the open which included masking certain areas of the image to find the edges and lastly, I used the hough transform method to connect the lines to their mates, this method simply helped me connect the lines in the image that weren't connected.


I made a nested for loop to loop over the lines and get their coordinates. Then I added up the slope using the coordinates and filtered the lines into "left" and "right" sides based on their slopes. I also started grabbing their x and y values to be turned into a mean number later on. Then the slopes and coordinates of each of the sides were averaged to find the mean and the endpoints of the  lines were extrapolated using the mean coordinates and the slope for each.  When the function gets done running it should have added thick lines to the images of the roadway lines.





If you'd like to include images to show how the pipeline works, here is how to include an image: 

![alt text][image1]


### 2. Identify potential shortcomings with your current pipeline




One potential shortcoming is my lines dont always stay on the lane lines in the video, they sometimes move away from where they are supposed to be.

The algorithm for the lane lines needs to be a bit faster then it is now, it seems to sometimes lag instead of being in real time.I would like to find a way to imporve my algorithm to be faster and use less computing power then it does currently.


### 3. Suggest possible improvements to your pipeline

I would like to simulate my car in bad wheather conditions so I can see how the car would react to wind rain and snow in terms of being reliable and safe for both the people in the car and the people on the road as well. 

An imporvement would also be to test the algorithm on winding roads to see if it stays with the car the whole time instead of going all over the place.  I mentioned earlier as time goes on and the road gets more difficult it seems to struggle to adapt to the turns and potential hazards that might show up while driving. 
