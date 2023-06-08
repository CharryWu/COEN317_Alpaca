import os
import re
import ffmpeg
import file_util
from time import perf_counter
from log_util import log, bcolors
import subprocess

def get_frame_rate(video_url: str) -> str:
    output = subprocess.check_output(['ffprobe', video_url, '-v', '0', '-select_streams',
                                  'v', '-print_format', 'flat', '-show_entries', 'stream=r_frame_rate'], stderr=subprocess.STDOUT).decode()
    return output.split('"')[1]

def get_total_frames(video_url: str) -> int:
    frame_num = -1
    probe = ffmpeg.probe(video_url)
    video_info = next(s for s in probe['streams']
                      if s['codec_type'] == 'video')

    if 'nb_frames' in video_info:
        return int(video_info['nb_frames'])
    elif 'duration_ts' in video_info:
        return int(video_info['duration_ts'])

    log(f'{video_url} metadata doesn\'t contain precise duration, try using `ffmpeg` to find total frames')
    rc = subprocess.call(['which', 'ffmpeg'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if rc == 0:
        try:
            output = subprocess.check_output(
                ['ffmpeg', '-i', video_url, '-map', '0:v:0', '-c', 'copy', '-f', 'null', '-'], stderr=subprocess.STDOUT).decode()
            m = re.findall(r'frame=\s*(\d+)', output)
            if len(m) > 0:
                # If there're multiple streams in vid file, get largest frame_num
                for str_frame_num in m:
                    frame_num = max(frame_num, int(str_frame_num))
                return frame_num
        except Exception as e:
            pass

    log(f'ffmpeg not found or execute error, calculate number of approximate frames by FPS * duration (in seconds)')
    frame_rate = float(get_frame_rate(video_url))
    if frame_rate != -1:
        if 'format' in probe and 'duration' in probe['format']:
            return int(float(probe['format']['duration']) * frame_rate)
    return -1

def get_duration(video_url):
    """
    Get duration of video
    https://stackoverflow.com/a/31025482
    """
    result = subprocess.run([
            'ffprobe',
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            video_url
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    return float(result.stdout)

def video2images(video_url: str, output_dir: str = './', frame_filename_schema: str = '%04d.png'):
    output_url = file_util.get_path(output_dir, frame_filename_schema)
    log(f'{video_url} => {output_url}', bcolors.OKCYAN)
    t_start = perf_counter()
    result = ffmpeg.input(video_url).output(
        output_url).run(overwrite_output=True)
    t_stop = perf_counter()
    log(f'Duration: {(t_stop-t_start):.2f} seconds, result={result}', bcolors.OKCYAN)


def images2video(input_dir: str, frame_filename_schema: str = '%04d.png', output_url: str = 'out.mp4', fps: str = '25'):
    input_url = file_util.get_path(input_dir, frame_filename_schema)
    log(f'{input_url} => {output_url}', bcolors.OKCYAN)
    t_start = perf_counter()
    result = ffmpeg.input(input_url).filter('fps', fps=fps, round='up').output(
        os.path.abspath(output_url)).run(overwrite_output=True)
    t_stop = perf_counter()
    log(f'Duration: {(t_stop-t_start):.2f} seconds, result={result}', bcolors.OKCYAN)
