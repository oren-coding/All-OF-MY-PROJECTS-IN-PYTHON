import numpy as np
import cv2

# Hold the background frame for background subtraction.
background = None
hand = None
frames_elapsed = 0
FRAME_HEIGHT = 480
FRAME_WIDTH = 640
CALIBRATION_TIME = 30
BG_WEIGHT = 0.5
OBJ_THRESHOLD = 18

class HandData:
    def __init__(self, top, bottom, left, right, centerX):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.centerX = centerX
        self.prevCenterX = 0
        self.isInFrame = False
        self.isWaving = False
        self.fingers = None
        self.gestureList = []
    
    def update(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
    
    def check_for_waving(self, centerX):
        self.prevCenterX = self.centerX
        self.centerX = centerX
        self.isWaving = abs(self.centerX - self.prevCenterX) > 3


def write_on_image(frame):
    text = "Searching..."

    if frames_elapsed < CALIBRATION_TIME:
        text = "Calibrating..."
    elif hand is None or not hand.isInFrame:
        text = "No hand detected"
    else:
        if hand.isWaving:
            text = "Waving"
        elif hand.fingers == 0:
            text = "Rock"
        elif hand.fingers == 1:
            text = "Pointing"
        elif hand.fingers == 2:
            text = "Scissors"
    
    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

def get_region(frame):
    region = frame[region_top:region_bottom, region_left:region_right]
    region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    region = cv2.GaussianBlur(region, (5,5), 0)
    return region

def get_average(region):
    global background
    if background is None:
        background = region.copy().astype("float")
        return
    cv2.accumulateWeighted(region, background, BG_WEIGHT)

def segment(region):
    global hand
    diff = cv2.absdiff(background.astype(np.uint8), region)
    thresholded_region = cv2.threshold(diff, OBJ_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(thresholded_region.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        if hand is not None:
            hand.isInFrame = False
        return None
    else:
        if hand is not None:
            hand.isInFrame = True
        segmented_region = max(contours, key=cv2.contourArea)
        return (thresholded_region, segmented_region)

def get_hand_data(thresholded_image, segmented_image):
    global hand
    convexHull = cv2.convexHull(segmented_image)
    top    = tuple(convexHull[convexHull[:, :, 1].argmin()][0])
    bottom = tuple(convexHull[convexHull[:, :, 1].argmax()][0])
    left   = tuple(convexHull[convexHull[:, :, 0].argmin()][0])
    right  = tuple(convexHull[convexHull[:, :, 0].argmax()][0])
    centerX = int((left[0] + right[0]) / 2)
    if hand is None:
        hand = HandData(top, bottom, left, right, centerX)
    else:
        hand.update(top, bottom, left, right)
    if frames_elapsed % 6 == 0:
        hand.check_for_waving(centerX)
    hand.gestureList.append(count_fingers(thresholded_image))
    if frames_elapsed % 12 == 0:
        hand.fingers = most_frequent(hand.gestureList)
        hand.gestureList.clear()

def count_fingers(thresholded_image):
    line_height = int(hand.top[1] + (0.2 * (hand.bottom[1] - hand.top[1])))
    line = np.zeros(thresholded_image.shape[:2], dtype=np.uint8)
    cv2.line(line, (thresholded_image.shape[1], line_height), (0, line_height), 255, 1)
    line = cv2.bitwise_and(thresholded_image, thresholded_image, mask=line)
    contours, _ = cv2.findContours(line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    fingers = sum(1 for curr in contours if 5 < len(curr) < 3 * abs(hand.right[0] - hand.left[0]) / 4)
    return fingers

def most_frequent(input_list):
    counts = {}
    for item in reversed(input_list):
        counts[item] = counts.get(item, 0) + 1
    return max(counts, key=counts.get, default=0)

region_top = 0
region_bottom = int(2 * FRAME_HEIGHT / 3)
region_left = int(FRAME_WIDTH / 2)
region_right = FRAME_WIDTH

# Ask the user to select the camera interface
camera_index = int(input("Enter the camera index (e.g., 0 for default camera, 1 for external camera): "))

capture = cv2.VideoCapture(camera_index)

cv2.namedWindow("Camera Input", cv2.WINDOW_NORMAL)
cv2.namedWindow("Segmented Image", cv2.WINDOW_NORMAL)

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to capture frame. Check the camera index.")
        break
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
    frame = cv2.flip(frame, 1)
    region = get_region(frame)
    if frames_elapsed < CALIBRATION_TIME:
        get_average(region)
    else:
        region_pair = segment(region)
        if region_pair is not None:
            thresholded_region, segmented_region = region_pair
            cv2.drawContours(region, [segmented_region], -1, (255, 255, 255))
            cv2.imshow("Segmented Image", region)
            get_hand_data(thresholded_region, segmented_region)
    write_on_image(frame)
    cv2.imshow("Camera Input", frame)
    frames_elapsed += 1
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

capture.release()
cv2.destroyAllWindows()
