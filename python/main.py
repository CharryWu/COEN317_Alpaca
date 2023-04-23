import os
import argparse
from enum import Enum
from file_util import get_path, remove_files_by_suffix
from video_util import video2images, images2video, get_frame_rate, get_total_frames
from cv_util import draw_points, read_image_from_url, save_image_to_url, draw_points_all
from log_util import log, bcolors
from pathlib import Path

class ARG_ATTR(Enum):
    INPUT_FILE = 'INPUT_FILE'
    OUTPUT_FILE = 'OUTPUT_FILE'

rootdir = '..'
SAMPLES_DIR = get_path(rootdir, 'samples')
PYTHON_DIR = get_path(rootdir, 'python')

parser = argparse.ArgumentParser()
parser.add_argument('-i', dest=ARG_ATTR.INPUT_FILE.value, type=str, required=True, default='', help='input video file')
parser.add_argument('-o', dest=ARG_ATTR.OUTPUT_FILE.value, type=str, default='', help='output video file')

def process_paths(args) -> dict:
    """
    Obtain the input and output file paths from CLI args.
    If input path is not valid file or not exist, will exist with error code 1
    If output path is not specified (empty), will replace input file
    Gets input and output file basename as well
    Input:
        - args: an arg_parse object
    Output
        - ret: dict containing parsed path info
    """
    ret = {
        'input_url': args[ARG_ATTR.INPUT_FILE.value],
        'output_url': args[ARG_ATTR.OUTPUT_FILE.value],
        'input_basename': '',
        'output_basename': '',
    }

    cwd = os.getcwd()

    if not os.path.isabs(ret['input_url']): # Resolve relative input path
        ret['input_url'] = get_path(cwd, ret['input_url'])
    if not os.path.isfile(ret['input_url']): # Exit 1 if input not valid
        log(f'{ret["input_url"]} is not a valid video file. Terminate.', bcolors.FAIL)
        exit(1)
    input_filename = os.path.basename(ret['input_url'])
    output_filename = os.path.basename(ret['output_url'])
    if ret['output_url'] == '': # Output == Input if output not specified
        ret['output_url'] = get_path(SAMPLES_DIR, input_filename)
    if not os.path.isabs(ret['output_url']): # Resolve relative output path
        ret['output_url'] = get_path(cwd, ret['output_url'])

    ret['input_basename'] = Path(ret['input_url']).stem # Used for naming generated frames
    ret['output_basename'] = Path(ret['output_url']).stem # Used for naming generated frames
    return ret


def main(**args):
    """
    Main execution entry point, calls functions from utils files
    """
    args_parsed = process_paths(args)
    try:
        # Get metadata info of input video: total num of frames and FPS
        num_frames = get_total_frames(args_parsed['input_url'])
        frame_rate = get_frame_rate(args_parsed['input_url'])
        video2images(args_parsed['input_url'], SAMPLES_DIR, f'{args_parsed["input_basename"]}-%04d.png')
        draw_points_all(num_frames, SAMPLES_DIR, args_parsed['input_basename'], args_parsed['output_basename'])
        images2video(SAMPLES_DIR, f'{args_parsed["output_basename"]}-%04d.png', args_parsed['output_url'], fps=frame_rate)
    except Exception as e:
        print(e)
    finally: # cleanup
        remove_files_by_suffix(SAMPLES_DIR, '.png')

if __name__ == '__main__':
    args = parser.parse_args()
    main(**vars(args))
