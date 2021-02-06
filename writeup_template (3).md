# **Behavioral Cloning** 

## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: ./examples/placeholder.png "Model Visualization"
[image2]: ./examples/placeholder.png "Grayscaling"
[image3]: ./examples/placeholder_small.png "Recovery Image"
[image4]: ./examples/placeholder_small.png "Recovery Image"
[image5]: ./examples/placeholder_small.png "Recovery Image"
[image6]: ./examples/placeholder_small.png "Normal Image"
[image7]: ./examples/placeholder_small.png "Flipped Image"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network 
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing 
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of a convolution neural network with taking the Nvida model approach with regards to building it. it utilizes 5x5 and 3x3 filter sizes and depths between 24 and 64. 

my model includes RELU layers to utilizez nonlinearity, the images are cropped and the data is rescaled using real-valued numeric attributes usaing a KLL. rescaling makes the features more consistent with each other, which allows the model to predict outputs more accurately to give a better idea of what is going on. 

#### 2. Attempts to reduce overfitting in the model



The data includes several images of different parts of the roadway and adjusted steering angles. In addition each images is flipped in order help the network do more and create more data points without creating needing to input more images into the data set.

 I also added a max pooling layer and a dropout layer. Max pooling is used to help over-fitting by providing an abstracted form of the representation of the image it's looking at and the  dropout layer turns off a few neurons in the neural network randomly in order to avoid the problem of overfitting.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually 

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, and recovering from driving off the right side of the  road, this was in additon to feeding it images of different parts of the road which the end result was the car was able to drive successfully around the track.   It only needed to be taught how to recover from right turns with manually simulating it, it learned the rest from the data set.

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to use the  NVIDIA architecture,  image augmentation and feeding it data so that it would learn what parts of the road it was looking at and also manually driving the car to simulate different scenarios like losing control of the car and regaining control and making tight right turns. The end result was the car was eventually able to fix it's flaws that it couldn't get from images alone by having it actually learn and taking in data.



#### 2. Final Model Architecture

The final model architecture consisted of a convolution neural network with a normalization layer, three 5x5 convolution layers, two 3x3 convolution layers and three fully connected Layers + Output Layer.


![alt text][image1]

#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I fed it a good amount of data images and even flipped the images to use data agumentation, this was important because prior to not using data agumentation the car performed worse early on then when the images were flipped to gather more data points in the image without having to feed it additional images, I then drove one time around the track and recovered from losing control of the car which seemed to do the trick. The car was able to successfully complete the track after that.

![alt text][image2]

I then recorded the vehicle recovering from the right side of the road back to center so that the vehicle would learn to make right turns correctly. These images show what losing control of the car looks like and how to respond to get back on the road. I also tried to record generally good driving, in addition to that I let the car lose control at higher speeds because like with a human driver, faster speeds are much more difficult to control then slower ones. This is important because I like to approch this model with safety at every design implementation because ultimately humans have to trust that the car will safely get them to their destination even at high speeds like on a highway. You doh't want humans constantly stressing if the car will make a mistake, it's our job to install confidence in people who buy self driving cars that they are safe and the risk of an accident is minimal because anything can happen but still make the possibility as low as possible.

![alt text][image3]
![alt text][image4]
![alt text][image5]



![alt text][image6]
![alt text][image7]


After the collection process, I had a good amount number of data points enough so that it learned what it needed to learn from looking at the images and implementing data agumentation made a huge difference because it was able to learn more efficiently by gathering more data points without putting in new images into the data.


I finally randomly shuffled the data set and put some of the data into a validation set. 

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 5 as evidenced by the test runs I performed with different number of epochs before ultimately decding on 5 I used an adam optimizer so that manually training the learning rate wasn't necessary.
