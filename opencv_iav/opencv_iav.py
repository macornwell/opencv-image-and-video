import argparse
from opencv_iav.camera import OpenCVCamera

def _parse_args():
    parser = argparse.ArgumentParser()
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
