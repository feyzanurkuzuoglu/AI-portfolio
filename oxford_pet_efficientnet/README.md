# Oxford-IIIT Pet Classification with PyTorch

A small computer vision project built with **PyTorch** and `torchvision` using the Oxford-IIIT Pet dataset.

The goal of this project was to practice an end-to-end image classification workflow, starting with a simple custom CNN and later using transfer learning with EfficientNet.

## Dataset

The project uses the **Oxford-IIIT Pet Dataset**, which contains images from 37 cat and dog breeds.

For the initial custom CNN experiment, the images were resized to a smaller resolution to keep the model lightweight.

For EfficientNet, the images were resized to **224 × 224 pixels**.

## Models

### Custom CNN

I first built a small convolutional neural network from scratch to practice:

* defining a CNN architecture in PyTorch
* creating training and evaluation loops
* calculating loss and accuracy
* visualizing training results

The model achieved poor classification performance and was mainly used as a learning exercise rather than as a serious classifier.

### EfficientNet

I then used a pretrained **EfficientNet** model from `torchvision` with transfer learning.

The final classification layer was modified for the 37 classes in the Oxford-IIIT Pet dataset.

The pretrained model performed substantially better and was used for the final inference experiment.

## Workflow

* Load the Oxford-IIIT Pet dataset
* Apply image transformations
* Create PyTorch `DataLoader`s
* Build and train a simple custom CNN
* Evaluate and visualize its results
* Load a pretrained EfficientNet model
* Adapt the classifier for 37 pet breeds
* Train and evaluate the model
* Perform inference on a custom image

## Custom Image Test

As a final experiment, I used an image of my own domestic tabby cat.

The EfficientNet model predicted the cat as a **Bengal**.

The Oxford-IIIT Pet dataset contains only 37 predefined breeds and does not include a general domestic tabby or mixed-breed class. The classifier therefore has no "none of the above" option and must assign the image to one of the available classes.

## Technologies

* Python
* PyTorch
* torchvision
* EfficientNet
* Matplotlib
* Google Colab

## Notes

This project was created as a learning exercise while studying convolutional neural networks and transfer learning with PyTorch. It is not intended to be a production-level pet breed classification system.
