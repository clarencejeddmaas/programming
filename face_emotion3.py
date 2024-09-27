import cv2
from fer import FER

# Initialize the FER detector
detector = FER()

# Start video capture
cap = cv2.VideoCapture(0)

# Emotion labels
emotion_labels = ['happy', 'sad', 'angry', 'surprised', 'neutral']

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect emotions in the frame
    emotions = detector.detect_emotions(frame)

    # Check if there are any detected faces
    if emotions:
        # Get the most confident face detection
        face = emotions[0]
        
        # Extract the emotion dictionary
        dominant_emotion = face["emotions"]
        emotion_text = max(dominant_emotion, key=dominant_emotion.get)  # Get the emotion with the highest score
        
        # Debugging output to console
        print(f"Detected emotions: {dominant_emotion}")  # Print the dictionary of emotions

        # Get the bounding box for the face
        x, y, w, h = face['box']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle around the face

        # Display the dominant emotion in proper noun format
        cv2.putText(frame, f'Emotion: {emotion_text.capitalize()}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Display each emotion with its score below the bounding box
        y_offset = y + h + 10  # Start displaying just below the bounding box
        for label in emotion_labels:
            if label in dominant_emotion:  # Check if the label exists in the dictionary
                score = dominant_emotion[label]  # Get the score for each emotion
                cv2.putText(frame, f'{label.capitalize()}: {score:.2f}', (x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 15  # Move down for the next label

    # Show the frame
    cv2.imshow('Emotion Detection', frame)

    # Check for 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
