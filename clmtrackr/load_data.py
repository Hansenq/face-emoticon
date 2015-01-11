import webbrowser
for i in range(0, 2):
	webbrowser.open('http://127.0.0.1:8000/clmtrackr/feature_detection.html?id=' + str(i), new=2, autoraise=False)