import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import simpledialog, messagebox


import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox
import tkinter as tk
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
import os


def get_sensitivity():
    while True:
        sensitivity = simpledialog.askfloat("Sensitivity", "Please enter the sensitivity you desire (1-1.7):")
        if sensitivity is not None and 1 <= sensitivity <= 1.7:
            return sensitivity
        else:
            messagebox.showerror("Invalid sensitivity!", "Please enter a value between 1 and 1.7.")

def show_info_dialog():
    info_message = "Please enter the sensitivity you desire.\n"\
                   "Depending on your medical condition, you may need higher sensitivity.\n"\
                   "The more limited your movement, the higher sensitivity is suggested.\n"\
                   "If you have no problem with movement, 1.2 is suggested."

    info_window = tk.Toplevel(root)
    info_window.title("Sensitivity Information")
    info_label = tk.Label(info_window, text=info_message, padx=10, pady=10)
    info_label.pack()

# Create the main Tkinter window
root = tk.Tk()
root.withdraw()

# Show the information dialog first
show_info_dialog()

# Get the sensitivity from the user
sensitivity_value = get_sensitivity()

# Destroy the main Tkinter window after getting the sensitivity input
root.destroy()

# Now the rest of the code can use the sensitivity_value
print("Selected sensitivity:", sensitivity_value)
# Your additional code using the sensitivity_value can go here


cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[473:479]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w * landmark.x * sensitivity_value
                screen_y = screen_h * landmark.y * sensitivity_value
                pyautogui.moveTo(screen_x, screen_y)

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.01:
            pyautogui.click(button='left')
            pyautogui.sleep(0.25)

        right_top = landmarks[386]  # Top landmark of the right eye
        right_bottom = landmarks[374]  # Bottom landmark of the right eye
        cv2.circle(frame, (int(right_top.x * frame_w), int(right_top.y * frame_h)), 3, (0, 0, 255))
        cv2.circle(frame, (int(right_bottom.x * frame_w), int(right_bottom.y * frame_h)), 3, (0, 0, 255))
        if (right_bottom.y - right_top.y) < 0.003:
            pyautogui.click(button='right')
            pyautogui.sleep(0.25)

    cv2.imshow('Eye Controlled Mouse', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

if __name__ == "__main__":
    root.mainloop()
