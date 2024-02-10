import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

last_alert_time = 0
alert_cooldown = 5  # Seconds

# Function to issue alerts with a cooldown
def issue_alert(message, current_time):
    global last_alert_time
    if current_time - last_alert_time > alert_cooldown:
        print(message)
        last_alert_time = current_time

# Capture video from webcam.
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    current_time = time.time()

    # Process the image
    image = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    if results.pose_landmarks:
        # Analyze posture and head orientation here
        # Placeholder for your analysis logic
        
        # Example alert for demonstration
        issue_alert("Please adjust your posture.", current_time)

    # Display the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
