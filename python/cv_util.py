# import the necessary packages
from imutils import face_utils
import dlib
import cv2

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
p = "./models/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)


def draw_points(image):

    # detect faces in the grayscale image
    rects = detector(image, 0)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(image, rect)
        shape = face_utils.shape_to_np(shape)

        # loop over the (x, y)-coordinates for the facial landmarks
        # and draw them on the image
        for (x, y) in shape:
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    while(True):
        cv2.imshow('test', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Destroy all the windows
    cv2.destroyAllWindows()

def read_image_from_url(url, mode=cv2.IMREAD_GRAYSCALE):
    return cv2.imread(url, mode)

if __name__ == '__main__':
    img = read_image_from_url('../samples/charry.jpg')
    draw_points(img)