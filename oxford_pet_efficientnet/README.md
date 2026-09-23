# Oxford-IIII Pet Classification with PyTorch

A small computer vision project built with **PyTorch** and `torchvision` using the Oxford-IIIT Pet dataset.

The main goal of this project was to practice an end-to-end image classification workflow and compare a simple custom convolutional neural network with a pretrained EfficientNet model.

## Dataset

The project uses the **Oxford-IIIT Pet Dataset**, which contains images from 37 cat and dog breeds.

For the initial custom CNN experiment, the images were resized to a smaller resolution to keep the model lightweight.

For EfficientNet, the images were resized to **224 × 224 pixels** to match the expected input size of the pretrained model.

## Models

### 1. Custom CNN

I first built a small convolutional neural network from scratch and trained it on the Oxford-IIIT Pet dataset.

The model was intentionally simple and mainly used as a baseline to practice:

* building a CNN with PyTorch
* creating training and evaluation loops
* calculating loss and accuracy
* visualizing model performance

Its classification performance was relatively poor, which was expected given the simplicity of the architecture and the difficulty of distinguishing 37 visually similar pet breeds.

### 2. EfficientNet

I then used a pretrained **EfficientNet** model from `torchvision` with transfer learning.

The final classification layer was modified to output predictions for the 37 classes in the Oxford-IIIT Pet dataset.

Using a pretrained model produced substantially better results than the custom CNN.

## Model Comparison

The results of the custom CNN and EfficientNet were compared using training and test metrics.

Plots were also created to visualize the differences in model performance.

This comparison demonstrates the advantage of transfer learning when working with a relatively small image dataset and a more complex classification problem.

## Workflow

* Load the Oxford-IIIT Pet dataset using `torchvision.datasets`
* Apply image preprocessing and transformations
* Create PyTorch `DataLoader`s
* Build and train a custom CNN as a baseline
* Evaluate the custom model
* Load a pretrained EfficientNet model
* Adapt its classifier for 37 pet breeds
* Train and evaluate EfficientNet
* Compare the performance of both models
* Plot training and evaluation results
* Perform inference on a custom image

## Custom Image Test

As a final experiment, I used an image of my own domestic tabby cat.

The EfficientNet model predicted the cat as a **Bengal**.

This highlights an important limitation of closed-set classifiers. The Oxford-IIIT Pet dataset contains only 37 predefined breeds and does not include a general domestic tabby or mixed-breed category.

The model therefore has no option to predict "none of the above" and must assign the image to one of the classes it has learned.

## Technologies

* Python
* PyTorch
* torchvision
* EfficientNet
* Matplotlib
* Google Colab

## Notes

This project was created as a learning exercise while studying computer vision, convolutional neural networks, and transfer learning with PyTorch.

The custom CNN was used primarily as a baseline for comparison rather than as an attempt to build a high-performance classifier.

The project is not intended to be a production-level pet breed classification system.
