import numpy # For array processing
import os    # For listing all files in directory
from PIL import Image # For Image processing
from scipy.misc import imsave # To save images as png

EMOTION_MAP = {
    'AN': 0,  # Anger
    'DI': 1,  # Disgust
    'FE': 2,  # Fear
    'HA': 3,  # Happiness
    'SA': 4,  # Sadness
    'SU': 5,  # Surprise
    'NE': 6,  # Neutral
    '--': 7,  # Contempt (does not exist in JAFFE)
}

DATA_LOCATION = './data/jaffe'

files = os.listdir(DATA_LOCATION)

training_set = (
    [],
    []
)
test_set = (
    [],
    []
)
first = True

for filename in files:

    if filename[-5:] != '.tiff':
        # if the extension is not tiff, pass
        continue

    # Open Image
    image = Image.open(DATA_LOCATION + '/' + filename).convert("L")
    # Convert Image to array
    image_array = numpy.array(image)
    # Comvert Image to 1D array
    image_array_1d = numpy.ravel(image_array)

    if first:
        print 'Size: ' + str(image_array.shape)
        first = False

    # Find the parts of the filename corresponding to the emotion
    parts = filename.split('.')
    emotion = parts[1][:-1]
    label = EMOTION_MAP[emotion]

    if parts[1][-1] == '3':
        # Add to testing set
        test_set[0].append(image_array_1d)
        test_set[1].append(label)
    else:
        # Add to training set
        training_set[0].append(image_array_1d)
        training_set[1].append(label)

imsave('./data/processed/jaffe_train.png', training_set[0])
imsave('./data/processed/jaffe_test.png', test_set[0])

labels = 'var labels = ' + repr(list(numpy.concatenate((training_set[1], test_set[1]))))  + ';\n'
open('./data/processed/jaffe_labels.js', 'w').write(labels)
