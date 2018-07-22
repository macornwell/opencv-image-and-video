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
A module that provides easy access to OpenCV image and video functionality.
"""
from threading import Thread
import cv2
import datetime


class OpenCVCamera:
    """
    A class that wraps the functionality of OpenCV.
    """
    resolution_height = 480
    resolution_width = 640
    device = 0
    codec = 'XVID'  # Note: All available fourcc codecs available here http://www.fourcc.org/codecs.php.
    frame_rate = 32
    speed_modulation = 1.0
    __speed_error_correction = 4

    def take_picture(self, file_output_path):
        """
        Takes a picture.
        :param file_output_path: String path to the final file.
        :return:
        """
        self.__wrap_opencv_video_capture(file_output_path)

    def record_video(self, file_output_path, duration_in_seconds):
        """
        Records a video.
        :param file_output_path: The path to create the video.
        :param duration_in_seconds: The desired length in seconds for the video.
        :return:
        """
        self.__wrap_opencv_video_capture(file_output_path, duration_in_seconds=duration_in_seconds)

    def __wrap_opencv_video_capture(self, output_path, duration_in_seconds=0):
        with ThreadedVideoStream(self.device, self.resolution_height,
                                 self.resolution_width) as stream:
            if not stream:
                raise Exception('WTF?')
            if duration_in_seconds <= 0:
                frame = stream.read()
                cv2.imwrite(output_path, frame)
            else:
                video_out = cv2.VideoWriter(
                    output_path,
                    cv2.VideoWriter_fourcc(*self.codec.upper()),
                    self.frame_rate * self.speed_modulation,
                    (self.resolution_width, self.resolution_height)
                )
                milliseconds_per_frame = ((1 / self.frame_rate) * 1000.0) - self.__speed_error_correction
                count = 0
                start = datetime.datetime.now()
                current = datetime.datetime.now()
                since_last = current
                while (current - start).total_seconds() < duration_in_seconds:
                    if (current - since_last).total_seconds() * 1000.0 >= milliseconds_per_frame:
                        frame = stream.read()
                        video_out.write(frame)
                        since_last = datetime.datetime.now()
                        count += 1
                    current = datetime.datetime.now()
                video_out.release()


class ThreadedVideoStream:
    """
    Creates an OpenCV stream that is threaded.
    Follows the "with" pattern allowing the class to be used in a with statement.
    Example:
        with ThreadedVideoStream(0, 640, 800) as video_stream:
            video_stream.....

    The with pattern also takes care of starting the streaming and cleaning up the resources in __exit__
    """

    def __init__(self, source_device, height, width):
        """
        Constructor
        :param source_device: An integer for which video usb device. 0 = /dev/video0
        :param height: The resolution's height
        :param width:  The resolution's width
        """
        self._stopped = False
        self.__stream = cv2.VideoCapture(source_device)
        self.__stream.set(3, width)
        self.__stream.set(4, height)
        (self.__read_success, self.__frame) = self.__stream.read()
        self.__completely_stopped = True

    def start(self):
        """
        Starts the streaming.
        :return: The ThreadedVideoStream object. (useful for setting another object)
        """
        if not self._stopped:
            Thread(target=self.__update, args=()).start()
        return self

    def read(self):
        """
        Reads the latest frame from the stream.
        :return: A OpenCV frame.
        """
        return self.__frame

    def stop(self):
        """
        Stops streaming.
        """
        self._stopped = True

    def __update(self):
        while True:
            self.__completely_stopped = False
            if self._stopped:
                break
            (self.__read_success, self.__frame) = self.__stream.read()
        self.__completely_stopped = True

    def __enter__(self):
        """
        Enter begins the streaming.
        :return:
        """
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cleans up the stream.
        """
        self.stop()
        while not self.__completely_stopped:
            pass
        self.__stream.release()
