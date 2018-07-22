Feature: Create a picture

  Background: A user wants to create a picture using a webcam.
  Scenario: Create a picture with a webcam
    Given the webcam exists at /dev/video0, with a frame_rate of 30, with speed_modulation at 1.0
    When take_picture is called with an output path at /tmp/opencv_iav/take_picture.feature.jpg
    Then a file is created.
    Then the file is larger than 0 bytes.
