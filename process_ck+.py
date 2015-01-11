import numpy # For array processing
from os import listdir    # For listing all files in directory
from os.path import expanduser # For finding home directory
import os
import shutil # To move images
from PIL import Image # For Image processing
from scipy.misc import imsave # To save images as png
from random import randint


EMOTION_MAP = {
    0: 6, # Neutral
    1: 0, # Anger
    2: 7, # Contempt
    3: 1, # Disgust
    4: 2, # Fear
    5: 3, # Happiness
    6: 4, # Sadness
    7: 5, # Surprise
}


HOME_DIR = expanduser('~')
BASE_DIR = HOME_DIR + '/Downloads/CK+'
EMOTION_FOLDER_NAME = 'Emotion'
PHOTO_FOLDER_NAME = 'cohn-kanade-images'

DEST_FOLDER = './data/ck+_scaled'
TEST_FOLDER = './data/ck+_test_scaled'

IMAGE_WIDTH = 480
IMAGE_HEIGHT = 480

training_set = (
    [],
    []
)
test_set = (
    [],
    []
)
label_list = []
label_test = []
first = True

count = 0
count_test = 0

def get_emotion_label(sub_folder, scene_folder, image_name):
    emotion_loc = '/'.join([BASE_DIR, EMOTION_FOLDER_NAME, sub_folder, scene_folder, image_name]) + '_emotion.txt'
    f = open(emotion_loc)
    emotion_number = int(float(f.read()))
    f.close()
    label = EMOTION_MAP[emotion_number]
    return label

def process_photo(sub_folder, scene_folder, image_name):

    # Open image
    image_loc = '/'.join([BASE_DIR, PHOTO_FOLDER_NAME, sub_folder, scene_folder, image_name]) + '.png'
    image = Image.open(image_loc).convert("L")
    # Fix issues with the image + crop to 640x480
    (width, height) = image.size
    if width > IMAGE_WIDTH:
        image = image.crop(((width - IMAGE_WIDTH) / 2, 0, width - (width - IMAGE_WIDTH) / 2, height))
    if height > IMAGE_HEIGHT:
        image = image.crop((0, (height - IMAGE_HEIGHT) / 2, IMAGE_WIDTH, height - (height - IMAGE_HEIGHT) / 2))

    # Emotion label
    label = get_emotion_label(sub_folder, scene_folder, image_name)

    global first
    if first:
        print 'Size: ' + str(image_array.shape)
        first = False

    # Process image to fit the convnetjs ConvNet demos data input format.
    image_array = numpy.array(image)
    image_array_1d = numpy.ravel(image_array)

    if randint(0, 4) == 0:
        # Test Set
        test_set[0].append(image_array_1d)
        test_set[1].append(label)
    else:
        # Training Set
        training_set[0].append(image_array_1d)
        training_set[1].append(label)

    del image


def move_photo(sub_folder, scene_folder, image_name):
    global count, count_test

    image_loc = '/'.join([BASE_DIR, PHOTO_FOLDER_NAME, sub_folder, scene_folder, image_name]) + '.png'
    image = Image.open(image_loc).convert("L")
    # Fix issues with the image + crop to 640x480
    (width, height) = image.size
    if width > IMAGE_WIDTH:
        image = image.crop(((width - IMAGE_WIDTH) / 2, 0, width - (width - IMAGE_WIDTH) / 2, height))
    if height > IMAGE_HEIGHT:
        image = image.crop((0, (height - IMAGE_HEIGHT) / 2, IMAGE_WIDTH, height - (height - IMAGE_HEIGHT) / 2))

    # Resize image to scale
    image = image.resize((256, 256))

    label = get_emotion_label(sub_folder, scene_folder, image_name)

    if randint(0,4) == 0:
        # Test Set
        label_test.append(label)
        count_str = "%03d" % (count_test,)
        dest_loc = '/'.join([TEST_FOLDER, 'ck+_' + count_str + '.png'])
        # shutil.copy2(image_loc, dest_loc)
        image.save(dest_loc)
        count_test += 1
    else:
        # Training Set
        label_list.append(label)
        count_str = "%03d" % (count,)
        dest_loc = '/'.join([DEST_FOLDER, 'ck+_' + count_str + '.png'])
        # shutil.copy2(image_loc, dest_loc)
        image.save(dest_loc)
        count += 1
    image.close()

# One folder for each subject
sub_folders = listdir('/'.join([BASE_DIR, EMOTION_FOLDER_NAME]))

# Traverse the nested folders and look for folders with a .txt emotion
# label file.
# This code is terrible but oh well.
for sub_folder in sub_folders:
    try:
        scene_folders = listdir('/'.join([BASE_DIR, EMOTION_FOLDER_NAME, sub_folder]))
    except OSError:
        continue

    for scene_folder in scene_folders:
        try:
            files = listdir('/'.join([BASE_DIR, EMOTION_FOLDER_NAME, sub_folder, scene_folder]))
        except OSError:
            continue

        for f in files:
            if f[-4:] != '.txt':
                continue

            # We've found a emotion label for a photo.
            # Now let's get the photo.
            image_name = f[:-12] # Remove '_emotion.txt'
            # process_photo(sub_folder, scene_folder, image_name)
            move_photo(sub_folder, scene_folder, image_name)

# Process image to fit the convnetjs ConvNet demos data input format.
# imsave('./data/processed/ck+_train.png', training_set[0])
# imsave('./data/processed/ck+_test.png', test_set[0])

# labels = 'var labels = ' + repr(list(numpy.concatenate((training_set[1], test_set[1]))))  + ';\n'
# open('./data/processed/ck+_labels.js', 'w').write(labels)
labels = 'var labels = ' + repr(label_list)  + ';\n'
open('./data/processed/ck+_labels.js', 'w').write(labels)
labels = 'var labels = ' + repr(label_test)  + ';\n'
open('./data/processed/ck+_test_labels.js', 'w').write(labels)

print 'Processed ' + str(count) + ' photos.'
print 'Stored ' + str(len(label_list)) + ' labels.'
print 'Processed ' + str(count_test) + ' test photos.'
print 'Stored ' + str(len(label_test)) + ' test labels.'
