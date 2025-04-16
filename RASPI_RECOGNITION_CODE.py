import cv2
import pytesseract
import subprocess
import numpy as np
import re

# Camera parameters
width = 640
height = 480
framerate = 30
frame_size = width * height * 3 // 2  # YUV420p

# Launch libcamera-vid to output raw YUV420 frames to stdout
libcamera_cmd = [
    "libcamera-vid",
    "-t", "0",
    "--inline",
    "--width", str(width),
    "--height", str(height),
    "--framerate", str(framerate),
    "--codec", "yuv420",
    "-o", "-"
]

print("Starting Pi Camera via libcamera...")
proc = subprocess.Popen(libcamera_cmd, stdout=subprocess.PIPE, bufsize=10**8)

# Regex for matching example address pattern (customize this)
address_pattern = re.compile(r'\b1400 Washington Ave\b', re.IGNORECASE)
address_code_pattern = re.compile(r'\b500 2A\b', re.IGNORECASE)
user_code_pattern = re.compile(r'\b36947\b', re.IGNORECASE)

frame_count = 0
ocr_interval = 10


print("Reading frames and running OCR...")
try:
    while True:
        # Read a single raw YUV420 frame from stdout
        raw_frame = proc.stdout.read(frame_size)
        if len(raw_frame) < frame_size:
            print("Incomplete frame")
            break

        # Decode raw YUV420 to BGR
        yuv = np.frombuffer(raw_frame, dtype=np.uint8).reshape((height * 3 // 2, width))
        bgr = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)

        # Convert to grayscale for better OCR accuracy
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        
        
        frame_count += 1
        if frame_count % ocr_interval == 0:
            # OCR using pytesseract
            text = pytesseract.image_to_string(gray)
            # Try matching addresses in the text
            matches = user_code_pattern.findall(text)
            if matches:
                print("🔍 Code match found:", matches)
            if address_pattern.search(text) and address_code_pattern.search(text):
                print("🔍 Address match found")



        # Show frame (optional)
        cv2.imshow("Camera Feed", bgr)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    print("Cleaning up...")
    proc.terminate()
    cv2.destroyAllWindows()
