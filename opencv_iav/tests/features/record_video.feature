Feature: Record a video

  Background: A user wants to record a video with a webcam.
  Scenario: Create a video using a webcam
    Given the webcam exists at /dev/video0 using the output path at /tmp/opencv_iav/record_video.feature.avi
    When record_video is called with a duration of 1
    Then a file is created.
    Then the file is larger than 258 bytes.
