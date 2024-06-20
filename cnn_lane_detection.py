# -*- coding: utf-8 -*-
"""CNN Lane Detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16pMEXjdOtVDI2Z6oAkqeZzu1jikoPfg0
"""

from google.colab import files

uploaded = files.upload()

!pip install --upgrade pip setuptools wheel

!pip install scipy==1.13.1

import numpy as np
import cv2
from scipy.ndimage import zoom
from moviepy.editor import VideoFileClip
from tensorflow import keras

def imresize(arr, size):
    if arr.ndim == 3:
        resized = np.zeros((size[0], size[1], arr.shape[2]), dtype=arr.dtype)
        for i in range(arr.shape[2]):
            zoom_factors = [size[0] / float(arr.shape[0]), size[1] / float(arr.shape[1])]
            resized[..., i] = zoom(arr[..., i], zoom_factors, order=3)
        return resized
    else:
        zoom_factors = [n / float(o) for n, o in zip(size, arr.shape)]
        return zoom(arr, zoom_factors, order=3)

model = keras.models.load_model('model.h5')

class Lanes():
  def __init__(self):
    self.recent_fit = []
    self.avg_fit = []
def road_lines(image):
  small_img = imresize(image, (80, 160, 3))
  small_img = np.array(small_img)
  small_img = small_img[None,:,:,:]
  prediction = model.predict(small_img) [0] * 255
  lanes.recent_fit.append(prediction)

  if len(lanes.recent_fit) > 5:
    lanes.recent_fit = lanes.recent_fit[1:]

  lanes.avg_fit = np.mean (np.array([i for i in lanes.recent_fit]), axis = 0)

  blanks = np.zeros_like(lanes.avg_fit).astype (np.uint8)
  lane_drawn = np.dstack((blanks, lanes.avg_fit, blanks))

  # lane_image = imresize (lane_drawn, (720, 1280, 3))
  lane_image = imresize(lane_drawn, (720, 1280, 3)).astype(np.uint8)

  if lane_image.dtype != image.dtype:
    lane_image = lane_image.astype(image.dtype)

  result = cv2.addWeighted(image, 1, lane_image, 1, 0)

  return result

uploaded = files.upload()

vid_input = VideoFileClip("lanes_clip.mp4")
vid_output = "lanes_output_clip.mp4"

lanes = Lanes()

vid_clip = vid_input.fl_image(road_lines)
vid_clip.write_videofile(vid_output)
