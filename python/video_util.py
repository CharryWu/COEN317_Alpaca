import os
import ffmpeg
import file_util
from time import perf_counter
from log_util import log, bcolors

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