# import the necessary packages
import dlib
import cv2
import pathlib
from imutils import face_utils
from file_util import get_path
from time import perf_counter
from log_util import log, bcolors

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
file_parent = pathlib.Path(__file__).parent.resolve() # path relative to this file, not to cwd
p = get_path(file_parent, './models/shape_predictor_68_face_landmarks.dat')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)


def draw_points(image):
    """
    Draw delaunay points on a single OpenCV image.
    Args:
        - image: OpenCV image in NumPy format
    Output: None. This method does in-place mutation on the original image.
    """
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

def read_image_from_url(url, mode=cv2.IMREAD_UNCHANGED):
    return cv2.imread(url, mode)

def save_image_to_url(url, image):
    cv2.imwrite(url, image)

def draw_points_all(num_frames, work_dir, input_basename, output_basename):
    """
    Draw delaunay points on all image frames of input video in samples directory
    And save as output image frames
    """
    log(f'Face detection processing {num_frames} frames in {work_dir}. {input_basename} => {output_basename}', bcolors.OKCYAN)
    t_start = perf_counter()
    for frame_num in range(1, num_frames+1):
        img_url = get_path(work_dir, f'{input_basename}-{frame_num:04d}.png')
        img = read_image_from_url(img_url)
        draw_points(img)
        out_url = get_path(work_dir, f'{output_basename}-{frame_num:04d}.png')
        save_image_to_url(out_url, img)
    t_stop = perf_counter()
    log(f'Face detection complete! {num_frames} frames processed. Duration: {(t_stop-t_start):.2f} seconds.', bcolors.OKCYAN)