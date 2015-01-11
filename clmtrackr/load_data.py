import webbrowser, time

for i in range(0, 62):
    webbrowser.open('http://127.0.0.1:8000/clmtrackr/feature_detection.html?num=' + str(i), new=2, autoraise=False)
    time.sleep(3)
