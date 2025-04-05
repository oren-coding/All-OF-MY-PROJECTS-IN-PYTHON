import cv2
import datetime
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ask the user to select the camera interface
try:
    camera_index = int(input("Enter the camera index: "))
except ValueError:
    print("Invalid input. Using default camera (index 0).")
    camera_index = 0

cap = cv2.VideoCapture(camera_index)
root = tk.Tk()
root.title("Emotion Percentage Prototype")

# Create a Matplotlib figure and subplot for the bar chart
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.RIGHT)

# Lists to store detected emotions and their counts
detected_emotions = []
emotion_counts = {}
emotion_labels = ["Smiling", "Neutral", "Surprised", "Frowning"]  # Example emotions

def update_emotion_chart():
    """Updates the bar chart with the current emotion percentages."""
    global detected_emotions, emotion_counts, emotion_labels

    if detected_emotions:
        emotion_counts = {label: detected_emotions.count(label) for label in emotion_labels}
        total_detections = len(detected_emotions)
        percentages = [emotion_counts[label] / total_detections * 100 if total_detections > 0 else 0 for label in emotion_labels]

        ax.clear()
        ax.bar(emotion_labels, percentages, color=['green', 'gray', 'yellow', 'blue'])
        ax.set_ylabel("Percentage (%)")
        ax.set_title("Simulated Emotion Percentages (Last 10 Faces)")
        ax.set_ylim(0, 100)
        canvas.draw()
    else:
        ax.clear()
        ax.set_ylabel("Percentage (%)")
        ax.set_title("No Faces Detected")
        ax.set_ylim(0, 100)
        canvas.draw()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame.")
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Simulate emotion detection for each face
            simulated_emotion = random.choice(emotion_labels)
            detected_emotions.append(simulated_emotion)
            if len(detected_emotions) > 10:
                detected_emotions.pop(0)
        update_emotion_chart()  # Update the chart after processing all faces
    else:
        update_emotion_chart() # Keep this to clear the chart when no face is seen

    cv2.imshow('Face Detection', frame)
    root.update()

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
root.mainloop()