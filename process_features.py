import os

FEATURE_LOC = './data/jaffe_test_features'

files = os.listdir(FEATURE_LOC)

features = {}

for filename in files:
    path = '/'.join([FEATURE_LOC, filename])

    # Remove all files with a space in them
    if ' ' in filename:
        os.remove(path)
        continue

    f = open(path)

    point_arr = []

    for line in f:
        # Remove comma
        split_arr = line.split(',')
        point = [ float(split_arr[0]), float(split_arr[1]) ]
        point_arr.append(point)

    filename_arr = filename.split('_')
    filename_arr_back = filename_arr[1].split('.')

    features[int(filename_arr_back[0])] = point_arr


labels = 'var jaffe_test_features = ' + repr(features)  + ';\n'
open('./data/processed/jaffe_test_features.js', 'w').write(labels)

