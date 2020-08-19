import numpy as np
import cv2
from keras.models import *
from keras.layers import *
from keras.layers import multiply
from keras.optimizers import *
from keras.initializers import *
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras.utils import plot_model
from keras import backend as keras


def U_net(pretrained_weights = None, input_size = (256,256,1), dropout_rate = 0.5, training_dropout = True):
	input_layer = Input(input_size)
	conv1 = Conv2D(64, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(input_layer)
	conv1 = Conv2D(64, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv1)
	pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
	conv2 = Conv2D(128, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool1)
	conv2 = Conv2D(128, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv2)
	pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
	conv3 = Conv2D(256, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool2)
	conv3 = Conv2D(256, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv3)
	pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
	conv4 = Conv2D(512, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool3)
	conv4 = Conv2D(512, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv4)
	drop4 = Dropout(dropout_rate)(conv4, training=training_dropout)
	pool4 = MaxPooling2D(pool_size=(2, 2))(drop4)

	conv5 = Conv2D(1024, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(pool4)
	conv5 = Conv2D(1024, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv5)
	drop5 = Dropout(dropout_rate)(conv5, training=training_dropout)

	up6 = Conv2D(512, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(drop5))
	merge6 = concatenate([drop4, up6], axis = 3)
	conv6 = Conv2D(512, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge6)
	conv6 = Conv2D(512, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv6)

	up7 = Conv2D(256, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv6))
	merge7 = concatenate([conv3, up7], axis = 3)
	conv7 = Conv2D(256, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge7)
	conv7 = Conv2D(256, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv7)

	up8 = Conv2D(128, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv7))
	merge8 = concatenate([conv2, up8], axis = 3)
	conv8 = Conv2D(128, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge8)
	conv8 = Conv2D(128, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv8)

	up9 = Conv2D(64, 2, activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(UpSampling2D(size = (2,2))(conv8))
	merge9 = concatenate([conv1, up9], axis = 3)
	conv9 = Conv2D(64, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(merge9)
	conv9 = Conv2D(64, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
	conv9 = Conv2D(2, kernel_size = (3, 3), activation = 'relu', padding = 'same', kernel_initializer = 'he_normal')(conv9)
	conv10 = Conv2D(1, 1, activation = 'sigmoid')(conv9)

	model = Model(input = input_layer, output = conv10)

	model.compile(optimizer = Adam(lr = 1e-6), loss = 'binary_crossentropy', metrics = ['accuracy'])

	if(pretrained_weights):
		model.load_weights(pretrained_weights)
	return model


def resize_tifstack(tif_stack, target_size = (512, 512)):
	'''Given a numpy stack, and a target size, resizes the image stack at each layer to the target size.
	Arguments:
		tif_stack (np.ndarray) : numpy array with or without padding dimensions.
		target_size (tuple) : dimensions (2d) to resize each layer of the tif stack to
	Returns:
		resized_stack (np.ndarray) : numpy array resized to target size along xy dimension.
	'''
	# Reduce Extra dimensions
	tif_stack = np.squeeze(tif_stack)
	resized_stack = np.zeros((tif_stack.shape[0], *target_size))

	for i, layer in enumerate(tif_stack):
		resized_stack[i,:,:] = cv2.resize(layer, dsize = target_size)

	return resized_stack


def read_tif(path):
	'''Given a path to a TIF z stack image, reads in the dataset and returns it as a numpy array.
	Arguments:
		path (str) : path to the file.
	Returns:
		image_data (np.ndarray) : image data in numpy array format
	'''
	image_data = io.imread(path)
	return image_data


def format_tifstack(tif_stack, target_size = (256, 256)):
	'''Given a numpy stack, and a target size, normalizes image for reading into neural net for predictions
	Output 3d image will be 5d, with the first dimension indicating the number of layers, the second and last dimension
	filler dimensions, and the 3rd and 4th dimension the X,Y dimensions of the image plane
	Arguments:
		tif_stack (np.ndarray) : 3d numpy array with image information
		target_size (tuple) : 2 element tuple for target image size.
	Returns:
		resized_stack (np.ndarray) : Resized image stack to target size - note this function does not resize
			the z axis. Returned image stack also is normalized to null mean, unit variance.
	'''
	resized_stack = np.zeros((tif_stack.shape[0], 1, *target_size, 1))
	tif_stack = tif_stack.astype(dtype = np.float32)
	for i, layer in enumerate(tif_stack):
		output_layer = cv2.resize(layer, dsize = target_size)
		output_layer = output_layer.astype(dtype = np.float32)
		output_layer = (output_layer - np.mean(output_layer)) / np.std(output_layer)
		output_layer = np.expand_dims(output_layer, axis = -1)
		output_layer = np.expand_dims(output_layer, axis = 0)

		resized_stack[i, 0, :, :] = output_layer

	return resized_stack


def process_single(file_path, target_size, MODEL_OBJECT, threshold = None):
	'''Given a single image filepath, opens the image, resizes the image to the target size for prediction
	and saves the corresponding prediction out to a file.
	Arguments:
		file_path (str) :  path for where the image is located
		target_size (tuple) : 2 element tuple containing the dimensions of the target image to be fed into 
			network for prediction
		model_path (str) : path where the model weights are saved
		threshold (float) : arbitrary value for simple thresholding of output predictions.

	Returns:
		result (np.ndarray) : 3D numpy nd array containing information on predicted image.
		resized_stack (np.ndarray) : 3D numpy nd array with stack resized to the target size
	'''
	img_stack = read_tif(file_path)
	resized_stack = format_tifstack(img_stack, target_size = target_size)
	generator = generate_layer(resized_stack)

	result = MODEL_OBJECT.predict_generator(generator, steps = img_stack.shape[0], verbose = 1)
	if threshold is None:
		pass
	else:
		result[result <= threshold] = 0
		result[result > threshold] = 1
	return result, resized_stack



if __name__ == "__main__":

	# This is some example code demonstrating how to load a model, and how to read it into a function as an Object.
	model_location = "PUT THE PATH TO THE MODEL HERE"
	input_size = (256,256)

	# Load the model's weights into MODEL_OBJECT. The reason why we load it before using "process_single"
	# is to save on memory; reloading the MODEL_OBJECT every time slows down the program, and presently also takes
	# up a ton of memory on the computer each time we load it since we don't unload the prior instance.
	MODEL_OBJECT = U_net(training_dropout = False, input_size = (*input_size, 1))
	MODEL_OBJECT.load_weights(model_location)

	# Use MODEL_OBJECT to process a single image
	outputImg = process_single(file_path = "testImage.tif", 
								target_size = input_size,
								MODEL_OBJECT = MODEL_OBJECT, 
								threshold = None)

	# In the process of pushing a simple image to a model, the original image is resized to "input_size", and the output image
	# is of the same dimensions.  To bring it back to the original dimensions (which I have arbitrarily set to (512,512)), we 
	# need to resize the output image.
	resizedOutputImg = resize_tifstack(outputImg, target_size = (512,512))