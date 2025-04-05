import cv2
import datetime

# Load the pre-trained Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Ask the user to select the camera interface
camera_index = int(input("Enter the camera index (e.g., 0 for default camera, 1 for external camera): "))

# Open a connection to the selected webcam
cap = cv2.VideoCapture(camera_index)

zoom_level = 1.0

# Create a named window and set it to full screen
cv2.namedWindow('Face Detection', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Face Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame. Check the camera index.")
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame with improved parameters
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=8, minSize=(30, 30))

    # Draw rectangles around the faces, count them, and display their positions and sizes
    face_count = 0
    if len(faces) > 0:
        # Use the first detected face to center the zoom
        (x, y, w, h) = faces[0]
        face_center_x, face_center_y = x + w // 2, y + h // 2
        face_count = len(faces)

        # Calculate the cropping area
        new_height, new_width = int(frame.shape[0] / zoom_level), int(frame.shape[1] / zoom_level)
        y1 = max(0, face_center_y - new_height // 2)
        y2 = min(frame.shape[0], face_center_y + new_height // 2)
        x1 = max(0, face_center_x - new_width // 2)
        x2 = min(frame.shape[1], face_center_x + new_width // 2)

        # Crop the frame
        cropped_frame = frame[y1:y2, x1:x2]

        # Resize the cropped frame to the original frame size
        frame = cv2.resize(cropped_frame, (frame.shape[1], frame.shape[0]))

        # Draw rectangles around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Display the position and size of the face
            cv2.putText(frame, f'({x}, {y})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Size: {w}x{h}', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

    # Display the face count on the frame
    cv2.putText(frame, f'Faces: {face_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Add a timestamp to the frame
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Handle key presses for zooming and exiting
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('+') and zoom_level < 4.0:
        zoom_level += 0.1
    elif key == ord('-') and zoom_level > 1.0:
        zoom_level -= 0.1

# Release the capture and close the windows
cap.release()
cv2.destroyAllWindows()