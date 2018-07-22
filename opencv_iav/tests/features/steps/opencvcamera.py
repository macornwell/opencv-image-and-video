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
"""

# FILE: tests/features/steps/take_picture_steps.py
import os
import cv2
from behave import given, when, then, step, use_step_matcher
from hamcrest import assert_that, equal_to, greater_than_or_equal_to, less_than_or_equal_to, greater_than, less_than
from pymediainfo import MediaInfo
from opencv_iav.camera import OpenCVCamera

use_step_matcher("re")


def _setup_output_file_path(context, output_file_path):
    directory = os.path.dirname(output_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    context.output_file_path = output_file_path


@given('the webcam exists at /dev/video(?P<video_device>\d+), with a frame_rate of (?P<frame_rate>\d+), '
       'with speed_modulation at (?P<speed_modulation>\d+\.\d+)')
def step_impl(context, video_device, frame_rate, speed_modulation):
    context.camera = OpenCVCamera()
    context.camera.device = int(video_device)
    context.camera.speed_modulation = float(speed_modulation)
    context.camera.frame_rate = int(frame_rate)


@when('take_picture is called with an output path at (?P<output_file_path>.+)')
def step_impl(context, output_file_path):
    _setup_output_file_path(context, output_file_path)
    try:
        context.camera.take_picture(output_file_path)
    except Exception as e:
        raise e


@when('record_video is called with a duration of (?P<duration>\d+) '
      'and an output path at (?P<output_file_path>.+)')
def step_impl(context, duration, output_file_path):
    _setup_output_file_path(context, output_file_path)
    duration = int(duration)
    try:
        context.camera.record_video(context.output_file_path, duration)
    except Exception as e:
        raise e


@then('a file is created.')
def step_impl(context):
    assert_that(os.path.exists(context.output_file_path))


@then('the file is larger than (?P<minimum_file_size>\d+) bytes.')
def step_impl(context, minimum_file_size):
    minimum_file_size = int(minimum_file_size)
    file_size = os.path.getsize(context.output_file_path)
    assert_that(file_size, greater_than(minimum_file_size))


@then('the video is between (?P<low>\d+) and (?P<high>\d+) seconds long.')
def step_impl(context, low, high):
    media_info = MediaInfo.parse(context.output_file_path)
    duration_in_seconds = int(media_info.tracks[0].duration * 1000)
    assert_that(duration_in_seconds, greater_than_or_equal_to(int(low)), less_than_or_equal_to(high))


@then('the video contains between (?P<low>\d+) and (?P<high>\d+) frames.')
def step_impl(context, low, high):
    cap = cv2.VideoCapture(context.output_file_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    assert_that(length, greater_than_or_equal_to(int(low)), less_than_or_equal_to(int(high)))

