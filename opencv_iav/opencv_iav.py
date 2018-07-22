"""
Copyright (C) 2018 Michael Cornwell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Module:
This application uses OpenCV to take pictures and record video. (no sound)
There are many options that are available for recording the video such as changing the frame rate and playback speed.
"""

import argparse
from opencv_iav.camera import OpenCVCamera


def _parse_args():
    parser = argparse.ArgumentParser("This application uses OpenCV to take pictures or record videos without sound.")
    parser.add_argument('OUTPUT', type=str, help='The full path for the output file desired.')
    parser.add_argument('-d', '--duration', type=int, help='The video duration in seconds. '
                                                           'NOTE: This is required for creating a video.')
    parser.add_argument('-g', '--height', type=int, help='The resolution height.', default=640)
    parser.add_argument('-w', '--width', type=int, help='The resolution width.', default=800)
    parser.add_argument('-c', '--codec', type=str, help='The 4 character codec to use. '
                                                        'See: http://www.fourcc.org/codecs.php')
    parser.add_argument('-f', '--framerate', type=int, help='The frame rate to use for video. '
                                                            'Note: Depending on computing horse power this value'
                                                            'may vary. Consider experimenting.', default=32)
    parser.add_argument('-e', '--device', type=int, help='The /dev/video device number. Example: 0 = /dev/video0',
                        default=0)
    parser.add_argument('-s', '--speed-modulation', type=float,
                        help='Speeds up or slows down a video recording. 1.0 = Normal. 2.0 = Two Times Faster',
                        default=1.0)

    args = parser.parse_args()
    return args


def _get_camera(args):
    camera = OpenCVCamera()
    camera.device = args.device
    if args.height:
        camera.resolution_height = args.height
    if args.width:
        camera.resolution_width = args.width
    if args.codec:
        camera.codec = args.codec
    if args.framerate:
        camera.frame_rate = args.framerate
    if args.speed_modulation != 1.0:
        camera.speed_modulation = args.speed_modulation
    return camera


def main():
    args = _parse_args()
    camera = _get_camera(args)
    output = args.OUTPUT
    duration = args.duration

    if not duration:
        camera.take_picture(output)
    else:
        camera.record_video(output, duration)

if __name__ == '__main__':
    main()
