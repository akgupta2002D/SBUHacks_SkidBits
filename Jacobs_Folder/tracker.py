import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Moving average buffer and parameters
buffer_size = 10
x_coords_buffer = np.zeros(buffer_size)
buffer_index = 0

last_alert_time = 0
alert_cooldown = 2  # Seconds
movement_threshold = 0.05  # Adjust based on testing

def update_buffer(buffer, index, value):
    buffer[index % len(buffer)] = value
    return (index + 1) % len(buffer), np.mean(buffer)

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
        landmarks = results.pose_landmarks.landmark
        nose_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x

        # Update and get smoothed nose x-coordinate
        buffer_index, smoothed_nose_x = update_buffer(x_coords_buffer, buffer_index, nose_x)
        ear_midpoint_x = (landmarks[mp_pose.PoseLandmark.LEFT_EAR.value].x + landmarks[mp_pose.PoseLandmark.RIGHT_EAR.value].x) / 2

        # Check direction based on smoothed value and threshold
        if current_time - last_alert_time > alert_cooldown:
            if smoothed_nose_x < ear_midpoint_x - movement_threshold:
                print("You looked to the left.")
                last_alert_time = current_time
            elif smoothed_nose_x > ear_midpoint_x + movement_threshold:
                print("You looked to the right.")
                last_alert_time = current_time

    # Display the image
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
