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

DEST_FOLDER = './data/ck+'

training_set = (
    [],
    []
)
test_set = (
    [],
    []
)
first = True

count = 0

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
    if width > 640:
        image = image.crop(((width - 640) / 2, 0, width - (width - 640) / 2, height))
    if height > 480:
        image = image.crop((0, (height - 480) / 2, 640, height - (height - 480) / 2))

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
    global count

    image_loc = '/'.join([BASE_DIR, PHOTO_FOLDER_NAME, sub_folder, scene_folder, image_name]) + '.png'

    label = get_emotion_label(sub_folder, scene_folder, image_name)

    dest_loc = '/'.join([DEST_FOLDER, 'ck+_' + str(count) + '_' + str(label) + '.png'])
    shutil.copy2(image_loc, dest_loc)

    count += 1

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

print 'Processed ' + str(count) + ' photos.'

# Process image to fit the convnetjs ConvNet demos data input format.
# imsave('./data/processed/ck+_train.png', training_set[0])
# imsave('./data/processed/ck+_test.png', test_set[0])

# labels = 'var labels = ' + repr(list(numpy.concatenate((training_set[1], test_set[1]))))  + ';\n'
# open('./data/processed/ck+_labels.js', 'w').write(labels)
