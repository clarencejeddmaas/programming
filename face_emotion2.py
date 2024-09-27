import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Load pre-trained emotion model
emotion_model = load_model('fer2013_mini_XCEPTION.102-0.66.hdf5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Sad', 'Surprise', 'Neutral']

# Load the face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capture video from the default camera
cap = cv2.VideoCapture(0)

# Check if the video capture is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop through detected faces
    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]

        # Resize the region of interest to the required size for the emotion model
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype('float') / 255.0
        roi = np.expand_dims(roi, axis=0)

        # Predict emotion
        emotion = emotion_model.predict(roi)[0]
        emotion_index = np.argmax(emotion)
        emotion_text = emotion_labels[emotion_index]

        # Draw rectangle around face and label the emotion
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion_text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Emotion Recognition', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 

# Release the webcam and destroy all OpenCV windows
cap.release()
cv2.destroyAllWindows()  # Fixed typo from earlier, this is the correct method to close windows
