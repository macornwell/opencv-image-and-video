# FILE: tests/features/steps/take_picture_steps.py
import os
from behave import given, when, then, step, use_step_matcher
from opencv_iav.camera import OpenCVCamera

use_step_matcher("re")

@given('the webcam exists at /dev/video(?P<video_device>\d) using the output path at (?P<output_file_path>.+)')
def step_impl(context, video_device, output_file_path):
    context.camera = OpenCVCamera()
    context.camera.device = int(video_device)
    directory = os.path.dirname(output_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    context.output_file_path = output_file_path

@when('take_picture is called')
def step_impl(context):
    try:
        context.camera.take_picture(context.output_file_path)
    except Exception as e:
        raise e

@when('record_video is called with a duration of (?P<duration>\d+)')
def step_impl(context, duration):
    duration = int(duration)
    try:
        context.camera.record_video(context.output_file_path, duration)
    except Exception as e:
        raise e

@then('a file is created.')
def step_impl(context):
    assert os.path.exists(context.output_file_path)

@then('the file is larger than (?P<minimum_file_size>\d+) bytes.')
def step_impl(context, minimum_file_size):
    minimum_file_size = int(minimum_file_size)
    file_size = os.path.getsize(context.output_file_path)
    assert file_size > minimum_file_size
