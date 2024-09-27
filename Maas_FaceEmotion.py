import cv2
from fer import FER

# Initialize the FER detector
detector = FER()

# Start video capture
cap = cv2.VideoCapture(0)

# Emotion labels
emotion_labels = ['Happy', 'Sad', 'Angry', 'Surprised', 'Neutral']

while True:
    return_status, frame = cap.read() 
    if not return_status:
        break
    
    # Detect emotions in the frame
    emotions = detector.detect_emotions(frame)

    # Check if there are any detected faces
    if emotions:
        face = emotions[0]
        dominant_emotion = face["emotions"]
        emotion_text = max(dominant_emotion, key=dominant_emotion.get)

        print(f"Detected emotions: {dominant_emotion}")

        x, y, w, h = face['box']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.putText(frame, f'Emotion: {emotion_text.capitalize()}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Display each emotion with its score below the bounding box
        y_offset = y + h + 10 
        for label in emotion_labels:
            if label in dominant_emotion: 
                score = dominant_emotion[label]
                cv2.putText(frame, f'{label.capitalize()}: {score:.2f}', (x, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                y_offset += 15

    # Show the frame
    cv2.imshow('Emotion Detection', frame)

    # Check for 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()