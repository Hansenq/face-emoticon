import webbrowser, time
for i in range(40, 80):
    webbrowser.open('http://0.0.0.0:8000/clmtrackr/feature_detection.html?num=' + str(i), new=2, autoraise=False)
    time.sleep(5)