Feature: Create a picture

  Background: A user wants to create a picture using a webcam.
  Scenario: Create a picture with a webcam
    Given the webcam exists at /dev/video1 using the output path at /tmp/opencv_iav/take_picture.feature.jpg
    When take_picture is called
    Then a file is created.
    Then the file is larger than 0 bytes.
