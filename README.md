# A Fully Automated Deep Learning-based Network For Detecting COVID-19 from a New And Large Lung CT Scan Dataset

COVID-19 is a severe global problem, and AI can play a significant role in preventing losses by monitoring and detecting infected persons in early-stage. This paper aims to propose a high-speed and accurate fully-automated method to detect COVID-19 from the patient's CT scan images. We introduce a new dataset that contains 48260 CT scan images from 282 normal persons and 15589 images from 95 patients with COVID-19 infections. At the first stage, this system runs our proposed image processing algorithm to discard those CT images that inside the lung is not properly visible in them. This action helps to reduce the processing time and false detections. At the next stage, we introduce a novel method for increasing the classification accuracy of convolutional networks. We implemented our method using the ResNet50V2 network and a modified feature pyramid network alongside our designed architecture for classifying the selected CT images into COVID-19 or normal with higher accuracy than other models. After running these two phases, the system determines the condition of the patient using a selected threshold. We are the first to evaluate our system in two different ways. In the single image classification stage, our model achieved 98.49% accuracy on more than 7996 test images. At the patient identification phase, the system correctly identified almost 234 of 245 patients with high speed. We also investigate the classified images with the Grad-CAM algorithm to indicate the area of infections in images and evaluate our model classification correctness.


**The details about our dataset is available at [COVID-CTset](https://github.com/mr7495/COVID-CTset)**</br>
**Find our paper at [Here](https://github.com/mr7495/COVID-CTset/blob/master/CT_V3.pdf)**
 
The general view of our work in this paper is represented in the next figure.

<p align="center">
    <img src="images/general-1.jpg" alt="photo not available" width="100%" height="70%">
    <br>
    <em> General view of our proposed fully automated network</em>
</p>



 # CT scans Selection

The lung HRCT scan device takes a sequence of consecutive images(we can call it a video or consecutive frames) from the chest of the patient that wants to check his infection to COVID-19. In an image sequence, the infection points may appear in some images and not be shown in other images. 

The clinical expert analyzes theses consecutive images and, if he finds the infections on some of them, indicates the patient as infected. 

Consider we have a neural network that is trained for classifying CVOID-19 cases based on a selected data that inside the lung was obviously visible in them. If we test that network on each image of an image sequence the belongs to a patient, the network may fail, because the lung is closed at the beginning and the end of each CT scan image sequence as it is depicted in the next figure. Hence, the network has not seen these cases while training; it may result in wrong detections, and so does not work well. 

<p align="center">
    <img src="images/open-closed-1.jpg" alt="photo not available" width="100%" height="70%">
    <br>
    <em> This figure shows the difference between an open lung and a closed lung</em>
</p>

 We propose some other techniques to discard the images that inside the lungs are not visible in them. Doing this also reduces performing time for good because, because the networks now only see some selected images.

The main difference between an open lung and closed lung is that the open lung image has lower pixel values(near to black) in the middle of the lung. First, we set a region in the middle of the images for analyzing the pixel values in them. This region should be at the center of the lung in all the images, so open-lung and closed-lung show the differences in this area. Unfortunately, the images of the dataset were not on one scale, and the lung's position differed for different patients; so after experiments and analysis, as the images have 512*512 pixels resolution, we set the region in the area of 120 to 370 pixels in the x-axis and 240 to 340 pixels in the y-axis ([120,240] to [370,340]). This area shall justify in containing the information of the middle of the lung in all the images.


The images of our dataset are 16-bit grayscale images. The maximum pixel value between all the images is almost equal to 5000. This maximum value differs very much between different images. At the next step for discarding some images and selecting the rest of them from an image sequence that belongs to a patient, we aim to measure the pixels of each image in the indicated region that have less value than 300, which we call dark pixels. This number was chosen out of our experiments.

 For all the images in the sequence, we count the number of pixels in the region with less value than 300. After that, we would divide the difference between the maximum counted number, and the minimum counted number by 1.5. This calculated number is our threshold. For example, if a CT scan image sequence of a patient has 3030 pixels with a value of less than 300 in the region, and another has 30 pixels less than 300, the threshold becomes 2000. The image with less dark pixels in the region than the threshold is the image that the lung is almost closed in that, and the image with more dark pixels is the one that inside the lung is visible in it. 


We calculated this threshold in this manner that the images in a sequence (CT scans of a patient) be analyzed together because, in one sequence, the imaging scale does not differ. After that, we discard those images that have less counted dark pixels than the calculated threshold. So the images with more dark pixels than the computed threshold will be selected to be given to the network for classification.

In the next figure, the image sequence of one patient is depicted, where you can observe which of the images the algorithm discards and which will be selected.

<p align="center">
    <img src="images/sequence-1.jpg" alt="photo not available" width="100%" height="70%">
    <br>
    <em>The output of the selection algorithm. The highlighted images are the rejected ones by the algorithm</em>
</p>

**The CT selection algorithm is shared at [CT_selection_algorithm.py](CT_selection_algorithm.py)**

# Neural Networks
In this research, at the next stage of our work, we used deep convolution networks to classify the selected image of the first stage into normal or COVID-19. We utilized Xception, ResNet50V2, and our model for running the classification.


Feature pyramid network(FPN) helps when there are objects with different scales in the image. Although here we investigate image classification, to do this, the network must learn about the infection points and classify the image based on them. Using FPN can help us better classify the images in our cases.

In the next figure, you can see the architecture of the proposed network.  We used concatenation layers instead of adding layers in the default version of the feature pyramid network due to the authors' experience. At the end of the network, we concatenated the five classification results of the feature pyramid outputs(each output presents classification based on one scale features) and gave it to the classifier so that the network can use all of them for better classification. 

<p align="center">
    <img src="images/FPN-1.jpg" alt="photo not available" width="100%" height="70%">
    <br>
    <em>Architecture of ResNet50V2 with FPN</em>
</p>

The evaluation results based on single image classification is reported in next table:

  Average between five folds | Overall Accuracy | COVID sensitivity | Normal sensitivity 
------------ | ------------- | ------------- | -------------  
 ResNet50V2 with FPN| 98.49 | 94.96 | 98.7 
 Xception| 96.55 | 98.02 | 96.47 
 ResNet50V2 | 97.52 | 97.99 | 97.49  

<p align="center">
    <img src="images/covid_vis-converted-1.jpg" alt="photo not available" width="100%" height="70%">
    <br>
    <em>Visualized Features by Grad-Cam algorithm to show that the network is operating correctly and indicate the
infection regions in the COVID-19 CT Scans</em>
</p>

<p align="center">
    <img src="images/normal_vis-converted-1.jpg" alt="photo not available" width="100%" height="70%">
    <br>
    <em>In the normal images, as the network does not see any infections, the highlighted features would be at
the center showing that no infections have been found</em>
</p>

**The developed code for training and validation is shared available at [COVID_Train&Validation.ipynb](COVID_Train&Validation.ipynb)**

# Fully automated Network

**In [Automated_covid_detector_validation.ipynb](Automated_covid_detector_validation.ipynb) You can find the developed code for validating our fully automated networks.**

**By using [Automated_covid_detector.ipynb](Automated_covid_detector.ipynb), you can apply the automated network on a patient CT scan Images to find out if he is infected to COVID-19 or not**

The fully automated network takes the Ct scan images of a person as an input and runs the selection algorithm on them to select only the proper ones. Then the selected images would be given to network for classification, and if some percent of the selected images (An optional value) of a patient be classified as COVID-19, then that person would be considered as infected to COVID-19.


The evaluated results of the fully automated network on more than 230 patients are shown in the next table:

  Average between five folds | Correct Identified Patients | Wrong Identified Patients | Correct COVID Identified |Wrong Identified as Normal | Normal Correct Identified |Wrong Identified as COVID
------------ | ------------- | ------------- | -------------  | ------------- | ------------- | -------------  
 Our model| 233.8 | 10.8 | 17.6 | 1.4 | 216.2 | 9.4
 Xception | 218.8 | 25.8 | 18.8 | 0.2 | 200 | 25.6
 ResNet50V2 | 225.2 | 19.4 | 18.2 | 0.8 | 207 | 18.6
 
 **You may find some errors if using Tensorflow and Keras new versions. If so, apply this cell at the begging of your code:**
 ```
!pip uninstall tensorflow
!pip uninstall keras
!pip install tensorflow==2.2
!pip install keras==2.3.0
```

**The published version of our paper is available at:** </br>
 https://doi.org/10.1016/j.bspc.2021.102588
 
 **The pre-prints are available at:** </br>
 
 https://doi.org/10.1101/2020.06.08.20121541
 
 https://www.researchgate.net/publication/341804692_A_Fully_Automated_Deep_Learning-based_Network_For_Detecting_COVID-from_a_New_And_Large_Lung_CT_Scan_Dataset
 
 https://www.preprints.org/manuscript/202006.0031/v3
 


**If you use our data and codes, please cite it by:**
 ```
@article{RAHIMZADEH2021102588,
title = {A fully automated deep learning-based network for detecting COVID-19 from a new and large lung CT scan dataset},
journal = {Biomedical Signal Processing and Control},
pages = {102588},
year = {2021},
issn = {1746-8094},
doi = {https://doi.org/10.1016/j.bspc.2021.102588},
url = {https://www.sciencedirect.com/science/article/pii/S1746809421001853},
author = {Rahimzadeh, Mohammad and Attar, Abolfazl and Sakhaei, Seyed Mohammad},
}
 ```

  If you have any questions, contact me by this email : mr7495@yahoo.com

