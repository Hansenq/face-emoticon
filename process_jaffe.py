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

DATA_LOCATION = './data/jaffe_raw'

DEST_FOLDER = './data/jaffe'
TEST_FOLDER = './data/jaffe_test'

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

label_list = []
label_test = []

count = 0
count_test = 0

for filename in files:

    if filename[-5:] != '.tiff':
        # if the extension is not tiff, pass
        continue

    # Open Image
    image = Image.open(DATA_LOCATION + '/' + filename).convert("L")
    # Convert Image to array.
    # image_array = numpy.array(image)
    # Comvert Image to 1D array
    # image_array_1d = numpy.ravel(image_array)

    # if first:
    #     print 'Size: ' + str(image_array.shape)
    #     first = False

    # Find the parts of the filename corresponding to the emotion
    parts = filename.split('.')
    emotion = parts[1][:-1]
    label = EMOTION_MAP[emotion]

    if parts[1][-1] == '3':
        # Add to testing set
        count_str = "%03d" % (count_test,)
        image.save('/'.join([TEST_FOLDER, 'jaffe_' + count_str + '.png']))
        label_test.append(label)
        count_test += 1
    else:
        # Add to training set
        count_str = "%03d" % (count,)
        image.save('/'.join([DEST_FOLDER, 'jaffe_' + count_str + '.png']))
        label_list.append(label)
        count += 1

    image.close()

    # if parts[1][-1] == '3':
    #     # Add to testing set
    #     test_set[0].append(image_array_1d)
    #     test_set[1].append(label)
    # else:
    #     # Add to training set
    #     training_set[0].append(image_array_1d)
    #     training_set[1].append(label)


# Process image to fit the convnetjs ConvNet demos data input format.
# imsave('./data/processed/jaffe_0.png', training_set[0])
# imsave('./data/processed/jaffe_1.png', test_set[0])

# labels = 'var labels = ' + repr(list(numpy.concatenate((training_set[1], test_set[1]))))  + ';\n'
# open('./data/processed/jaffe_labels.js', 'w').write(labels)
labels = 'var labels = ' + repr(label_list)  + ';\n'
open('./data/processed/jaffe_labels.js', 'w').write(labels)
labels = 'var labels = ' + repr(label_test)  + ';\n'
open('./data/processed/jaffe_test_labels.js', 'w').write(labels)


# print 'Training Set Size: ' + str(len(training_set[0]))
# print 'Test Set Size: ' + str(len(test_set[0]))
print 'Processed ' + str(count) + ' photos.'
print 'Stored ' + str(len(label_list)) + ' labels.'
print 'Processed ' + str(count_test) + ' test photos.'
print 'Stored ' + str(len(label_test)) + ' test labels.'
