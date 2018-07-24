Feature: Record a video

  Background: A user wants to record a video with a webcam.
  Scenario: Create a video using a webcam with regular "default" settings
    Given the webcam exists at /dev/video0, with a frame_rate of 30, with speed_modulation at 1.0
    When record_video is called with a duration of 10 and an output path at /tmp/opencv_iav/record_video.feature.0.30.1.avi
    Then a file is created.
    Then the file is larger than 258 bytes.
    Then the video is between 8 and 12 seconds long.
    Then the video contains between 280 and 320 frames.

  Scenario: Create a video using a webcam that plays back 2x faster than normal.
    Given the webcam exists at /dev/video0, with a frame_rate of 30, with speed_modulation at 2.0
    When record_video is called with a duration of 10 and an output path at /tmp/opencv_iav/record_video.feature.0.30.2.avi
    Then a file is created.
    Then the file is larger than 258 bytes.
    Then the video is between 4 and 6 seconds long.
    Then the video contains between 280 and 320 frames.

  Scenario: Create a video using a webcam that plays back at half speed.
    Given the webcam exists at /dev/video0, with a frame_rate of 30, with speed_modulation at 0.5
    When record_video is called with a duration of 10 and an output path at /tmp/opencv_iav/record_video.feature.0.30.point5.avi
    Then a file is created.
    Then the file is larger than 258 bytes.
    Then the video is between 18 and 22 seconds long.
    Then the video contains between 140 and 160 frames.

  Scenario: Create a video using a webcam that plays at regular speed but with half the frames.
    Given the webcam exists at /dev/video0, with a frame_rate of 15, with speed_modulation at 1.0
    When record_video is called with a duration of 10 and an output path at /tmp/opencv_iav/record_video.feature.0.15.1.avi
    Then a file is created.
    Then the file is larger than 258 bytes.
    Then the video is between 8 and 12 seconds long.
    Then the video contains between 140 and 160 frames.

  Scenario: Be able to create a 24h video that can be watched in 2 minutes.
    Given the webcam exists at /dev/video0, with a frame_rate of 1, with speed_modulation at 720.0
    When record_video is called with a duration of 1440 and an output path at /tmp/opencv_iav/record_video.feature.24h.avi
    Then a file is created.
    Then the file is larger than 258 bytes.
    Then the video is 2 seconds long.
    Then the video contains between 700 and 740 frames.
