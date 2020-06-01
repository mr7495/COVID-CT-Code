# A Fully Automated Deep Learning-based Network For Detecting COVID-19 from a New And Large Lung CT Scan Dataset

COVID-19 is a severe global problem that has crippled many industries and killed many people around the world. One of the primary ways to decrease the casualties is the infected person's identification at the proper time. AI can play a significant role in these cases by monitoring and detecting infected persons in early-stage so that it can help many organizations.
 In this paper, we aim to propose a fully-automated method to detect COVID-19 from the patient's CT scan without needing a clinical technician.
We introduce a new dataset that contains 48260 CT scan images from 282 normal persons and 15589 images from 95 patients with COVID-19 infection. Our proposed network takes all the CT scan image sequences of a patient as the input and determines if the patient is infected with COVID-19. At the first stage, this network runs an image processing algorithm to discard those CT images that inside the lung is not properly visible in them. This helps to reduce the number of images that shall be identified as normal or COVID-19, so it reduces the processing time. Also, running this algorithm makes the deep network at the next stage to analyze only the proper images and thus reduces false detections. At the next stage, we propose a modified version of ResNet50V2 that is enhanced by a feature pyramid network for classifying the selected CT images into COVID-19 or normal. If enough number of chosen CT scan images of a patient be identified as COVID-19, the network considers that patient, infected to this disease. The ResNet50V2 with feature pyramid network achieved 98.49% accuracy on more than 7996 validation images and correctly identified almost 237 patients from 245 patients.



In this paper, we introduce a fully-automated method for detecting COVID-19 cases from the output files(images) of the lung HRCT scan device. This system does not need any medical expert for system configuration and takes all the CT scans of a patient and clarifies if he is infected to COVID-19 or not.

We also introduce and share a new dataset that we called COVID-CTset that contains 15589 COVID-19 images from 95 patients and 48260 normal images from 282 persons.

**The details about our dataset is availabel at [COVID-CTset](https://github.com/mr7495/COVID-CTset)**

At the first stage of our work, we use an image processing algorithm for selecting those images of the patients, that inside the lung and the possible infections be observable in them. In this way, we speed up the process because the network does not have to analyze all the images. Also, we improve the accuracy by giving the network the proper images.

 After that, we will train and test three deep convolutional neural networks for classifying the selected images. One of them is our proposed enhanced version of ResNet50V2 with a feature pyramid network. At the final stage, after the deep network is ready, we evaluate our fully automated system on more than 230 patients and 7996 images. 
 
The general view of our work in this paper is represented in nextfigure.

<p align="center">
	<img src="images/general-1.jpg" alt="photo not available" width="100%" height="70%">
	<br>
	<em> General view of our proposed fully automated network</em>
</p>



 
  \subsection{CT scans Selection}
\label{22}
%?HR
The lung HRCT scan device takes a sequence of consecutive images(we can call it a video or consecutive frames) from the chest of the patient that wants to check his infection to COVID-19. In an image sequence, the infection points may appear in some images and not be shown in other images. 

The clinical expert analyzes theses consecutive images and, if he finds the infections on some of them, indicates the patient as infected. 

Many previous methods selected an image of each patient's lung HRCT images and then used them for training and validation. Here we decide to make the patient lung analysis fully automated. Consider we have a neural network that is trained for classifying CVOID-19 cases based on a selected data that inside the lung was obviously visible in them. If we test that network on each image of an image sequence the belongs to a patient, the network may fail. Because at the beginning and the end of each CT scan image sequence, the lung is closed as it is depicted in fig. \ref{first_middle}. Hence, the network has not seen these cases while training; it may result in wrong detections, and so does not work well. 

To solve this, we can separate the dataset into three classes: infection-visible,no-infection, and lung-closed. Although this removes the problem but dividing the dataset into three classes has other costs like spending some time for making new labels, changing the network validation way. Also, it increases the processing time because the network shall see all the images of patient CT scans. But we propose some other techniques to discard the images that inside the lungs are not visible in them. Doing this also reduces performing time for good because, in the last method, the networks should have seen all the images, and now it only sees some selected images.

Fig. \ref{flowchart} shows the steps of the image-selection algorithm. As it is evident from fig. \ref{open-closed}, the main difference between an open lung and closed lung is that the open lung image has lower pixel values(near to black) in the middle of the lung. First, we set a region in the middle of the images for analyzing the pixel values in them. This region should be at the center of the lung in all the images, so open-lung and closed-lung show the differences in this area. Unfortunately, the images of the dataset were not on one scale, and the lung's position differed for different patients; so after experiments and analysis, as the images have 512*512 pixels resolution, we set the region in the area of 120 to 370 pixels in the x-axis and 240 to 340 pixels in the y-axis ([120,240] to [370,340]). This area shall justify in containing the information of the middle of the lung in all the images. Fig. \ref{region} shows the selected region in some different images.


The images of our dataset are 16-bit grayscale images. The maximum pixel value between all the images is almost equal to 5000. This maximum value differs very much between different images. At the next step for discarding some images and selecting the rest of them from an image sequence that belongs to a patient, we aim to measure the pixels of each image in the indicated region that have less value than 300, which we call dark pixels. This number was chosen out of our experiments.

 For all the images in the sequence, we count the number of pixels in the region with less value than 300. After that, we would divide the difference between the maximum counted number, and the minimum counted number by 1.5. This calculated number is our threshold. For example, if a CT scan image sequence of a patient has 3030 pixels with a value of less than 300 in the region, and another has 30 pixels less than 300, the threshold becomes 2000. The image with less dark pixels in the region than the threshold is the image that the lung is almost closed in that, and the image with more dark pixels is the one that inside the lung is visible in it. 


We calculated this threshold in this manner that the images in a sequence (CT scans of a patient) be analyzed together because, in one sequence, the imaging scale does not differ. After that, we discard those images that have less counted dark pixels than the calculated threshold. So the images with more dark pixels than the computed threshold will be selected to be given to the network for classification.

In fig. \ref{sequence}, the image sequence of one patient is depicted, where you can observe which of the images the algorithm discards and which will be selected.

\begin{figure}[!hb]
\centering
\includegraphics[width=\linewidth]{sequence.pdf}
\caption{The CT scan images of a patient are shown in this figure. The highlighted images are the ones that the algorithm discards. It is observable that those images that clearly show inside the lung are selected to be classified at the next stage.}
\label{sequence}
\end{figure}
