# import the necessary packages
import cv2
import mediapipe as mp
from imutils import face_utils
from file_util import get_path
from time import perf_counter
from log_util import log, bcolors

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

def draw_points(image):
    """
    Draw delaunay points on a single OpenCV image.
    Args:
        - image: OpenCV image in NumPy format
    Output: None. This method does in-place mutation on the original image.
    """
    # Convert the BGR image to RGB before processing.
    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print and draw face mesh landmarks on the image.
    if not results.multi_face_landmarks:
        return None
    for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style()
        )
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style()
        )
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_iris_connections_style()
        )

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