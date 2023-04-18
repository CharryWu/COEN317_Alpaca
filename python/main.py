from file_util import get_path, remove_files_by_suffix
from video_util import video2images, images2video

rootdir = '..'

if __name__ == '__main__':
    SAMPLES_DIR = get_path(rootdir, 'samples')
    VIDEO_URL = get_path(SAMPLES_DIR, 'Big_Buck_Bunny_Trailer_1080p.ogx')
    remove_files_by_suffix(SAMPLES_DIR, '.png')
    remove_files_by_suffix(SAMPLES_DIR, '.mp4')
    video2images(VIDEO_URL, SAMPLES_DIR, 'bunny-%04d.png')
    images2video(SAMPLES_DIR, 'bunny-%04d.png', '../samples/test2.mp4')