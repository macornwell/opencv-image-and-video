"""
A module that provides easy access to OpenCV image and video functionality.
"""
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

    def _wrap_opencv_video_capture(self, output_path, duration_in_seconds=0):
        cap = cv2.VideoCapture(self.device)
        cap.set(3, self.resolution_width)
        cap.set(4, self.resolution_height)
        video_out = None
        try:
            if duration_in_seconds <= 0:
                ret, frame = cap.read()
                cv2.imwrite(output_path, frame)
            else:
                codec = self.codec.upper()
                video_out = cv2.VideoWriter(
                    output_path,
                    cv2.VideoWriter_fourcc(*codec),
                    self.frame_rate,
                    (self.resolution_width, self.resolution_height)
                )
                start_time = datetime.datetime.now()
                current_time = datetime.datetime.now()
                while (current_time - start_time).total_seconds() < duration_in_seconds:
                    current_time = datetime.datetime.now()
                    ret, frame = cap.read()
                    video_out.write(frame)
        finally:
            cap.release()
            if video_out:
                video_out.release()

    def take_picture(self, file_output_path):
        self._wrap_opencv_video_capture(file_output_path)

    def record_video(self, file_output_path, duration_in_seconds):
        self._wrap_opencv_video_capture(file_output_path, duration_in_seconds=duration_in_seconds)
