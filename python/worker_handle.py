from config import Settings
from cv_util import draw_points_all
from file_util import remove_files_by_suffix, remove_files_in_dir, save_to_disk
from video_util import get_frame_rate, get_total_frames, images2video, video2images
from file_util import get_path
from log_util import log
from pathlib import Path

processing_filename = ""
processed_filename = ""

failure = False

def worker_reset():
    global processing_filename
    global processed_filename
    global failure
    remove_files_in_dir(Settings().WORKER_DIR)
    processing_filename = ""
    processed_filename = ""
    failure = False

def process(full_url, filename):
    global processing_filename
    global processed_filename
    global failure
    settings = Settings()
    try:
        processing_filename = filename
        processed_filename = ""
        # Get metadata info of input video: total num of frames and FPS
        num_frames = get_total_frames(full_url)
        frame_rate = get_frame_rate(full_url)
        input_basename = Path(processing_filename).stem # Used for naming generated frames
        output_basename = Path(processing_filename).stem + '_out' # Used for naming generated frames
        output_url = get_path(settings.WORKER_DIR, processing_filename)
        log(f'input {full_url}: frame_rate={frame_rate}, num_frames={num_frames}')
        remove_files_by_suffix(settings.WORKER_DIR, '.png')
        video2images(full_url, settings.WORKER_DIR, f'{input_basename}-%04d.png')
        draw_points_all(num_frames, settings.WORKER_DIR, input_basename, output_basename)
        images2video(settings.WORKER_DIR, f'{output_basename}-%04d.png', output_url, fps=frame_rate)
        processed_filename = output_url
    except Exception as e:
        print(e)
        failure = True
    finally: # cleanup
        remove_files_by_suffix(settings.WORKER_DIR, '.png')

