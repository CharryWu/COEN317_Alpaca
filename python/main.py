from file_util import get_path, remove_files_by_suffix
from video_util import video2images, images2video, get_frame_rate_int, get_total_frames
from cv_util import draw_points, read_image_from_url, save_image_to_url

rootdir = '..'

if __name__ == '__main__':
    SAMPLES_DIR = get_path(rootdir, 'samples')
    VIDEO_URL = get_path(SAMPLES_DIR, 'Big_Buck_Bunny_Trailer_1080p.ogx')
    VIDEO_URL = get_path(SAMPLES_DIR, 'charry.webm')
    num_frames = get_total_frames(VIDEO_URL)
    remove_files_by_suffix(SAMPLES_DIR, '.png')
    remove_files_by_suffix(SAMPLES_DIR, '.mp4')
    # video2images(VIDEO_URL, SAMPLES_DIR, 'bunny-%04d.png')
    # images2video(SAMPLES_DIR, 'bunny-%04d.png', '../samples/test2.mp4')
    video2images(VIDEO_URL, SAMPLES_DIR, 'charry-%04d.png')
    for frame_num in range(1, num_frames+1):
        img_url = get_path(SAMPLES_DIR, 'charry-{:04d}.png'.format(frame_num))
        img = read_image_from_url(img_url)
        draw_points(img)
        out_url = get_path(SAMPLES_DIR, 'charry-processed-{:04d}.png'.format(frame_num))
        save_image_to_url(out_url, img)
    images2video(SAMPLES_DIR, 'charry-processed-%04d.png', '../samples/charry-processed.mp4')
