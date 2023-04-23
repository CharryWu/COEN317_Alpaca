## Python Project Setup
Ensure you've installed python >= 3.6, install the follwing dependecies (if you're using macOS, use `brew install`):
- FFmpeg: `sudo apt install ffmpeg`
- CMake: `sudo apt-get -y install cmake`
- python3-dev: `sudo apt install python3-dev`
- `sudo apt-get install libopenblas-dev liblapack-dev`
- `sudo apt install libavdevice-dev libavfilter-dev libavformat-dev libavcodec-dev libswresample-dev libswscale-dev libavutil-dev`


then run `pip install -r requirements.txt`

## Python Project Run
`python3 ./python/main.py -i <PATH_TO_INPUT_VIDEO_FILE> -o <PATH_TO_OUTPUT_VIDEO_FILE>`

## Reference
https://github.com/italojs/facial-landmarks-recognition