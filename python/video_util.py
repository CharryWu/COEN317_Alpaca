import os
import ffmpeg
import file_util
from time import perf_counter
from log_util import log, bcolors

def get_frame_rate_int(video_url: str) -> int:
    probe = ffmpeg.probe(video_url)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    try:
        frame_rate = int(eval(video_stream['avg_frame_rate']))
        return frame_rate
    except:
        return -1

def get_total_frames(video_url: str) -> int:
    probe = ffmpeg.probe(video_url)
    video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')

    if 'nb_frames' in video_info:
        return int(video_info['nb_frames'])
    elif 'duration_ts' in video_info:
        return int(video_info['duration_ts'])
    frame_rate = get_frame_rate_int(video_url)
    if frame_rate != -1:
        if 'format' in probe and 'duration' in probe['format']:
            return int(float(probe['format']['duration']) * frame_rate)
    return -1

def video2images(video_url: str, output_dir: str = './', input_file_schema: str = '%04d.png'):
    output_url = file_util.get_path(output_dir, input_file_schema)
    log(f'{video_url} => {output_url}', bcolors.OKCYAN)
    t_start = perf_counter()
    result = ffmpeg.input(video_url).output(output_url).run()
    t_stop = perf_counter()
    log(f'Duration: {(t_stop-t_start):.2f} seconds, result={result}', bcolors.OKCYAN)


def images2video(input_dir: str, input_file_schema: str = '%04d.png', output_url: str = 'out.mp4'):
    input_url = file_util.get_path(input_dir, input_file_schema)
    log(f'{input_url} => {output_url}', bcolors.OKCYAN)
    t_start = perf_counter()
    result = ffmpeg.input(input_url).output(os.path.abspath(output_url)).run()
    t_stop = perf_counter()
    log(f'Duration: {(t_stop-t_start):.2f} seconds, result={result}', bcolors.OKCYAN)