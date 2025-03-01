from ultralytics import YOLO
import cv2
import numpy as np
import os
import sys

model = YOLO("src/model/yolov8x-seg.pt")

def road_segmnent(image):
  # Convert imae to hsv
  hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

  # Segment green object
  lower_blue = np.array([40, 50, 50])
  upper_blue = np.array([90, 255, 255])
  mask = cv2.inRange(hsv, lower_blue, upper_blue)

  # Cut the ROI
  active_pixels = np.stack(np.where(mask))
  top_left = np.min(active_pixels, axis=1).astype(np.int32)
  bottom_right = np.max(active_pixels, axis=1).astype(np.int32)
  y1, x1 = top_left
  y2, x2 = bottom_right
  mask = mask[y1:, x1:x2]

  # Extract the largest component
  mask = mask.astype('uint8')
  mask = cv2.bitwise_not(mask)
  mask = mask.astype('uint8')
  nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
  sizes = stats[:, -1]
  max_label = 1
  max_size = sizes[1]
  for i in range(2, nb_components):
    if sizes[i] > max_size:
      max_label = i
      max_size = sizes[i]
  mask = np.zeros(output.shape)
  mask[output == max_label] = 255

  # Connect
  mask = mask.astype('uint8')
  mask = cv2.bitwise_not(mask)
  mask = mask.astype('uint8')
  cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    area = cv2.contourArea(c)
    if area < 10:
      cv2.drawContours(mask, [c], -1, (0, 0, 0), -1)
  # Morph close and invert image
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
  mask = 255 - cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

  # Extract the largest component
  mask = mask.astype('uint8')
  nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
  sizes = stats[:, -1]
  max_label = 1
  max_size = sizes[1]
  for i in range(2, nb_components):
    if sizes[i] > max_size:
      max_label = i
      max_size = sizes[i]
  mask = np.zeros(output.shape)
  mask[output == max_label] = 255

  # Cut the ROI
  mask = mask.astype('uint8')
  mask = cv2.bitwise_not(mask)
  active_pixels = np.stack(np.where(mask))
  top_left = np.min(active_pixels, axis=1).astype(np.int32)
  bottom_right = np.max(active_pixels, axis=1).astype(np.int32)
  y3, x3 = top_left
  y4, x4 = bottom_right
  mask = mask[y3:, x3:x4]

  return mask


def indentify_density(image):
  cap = cv2.imread(image)

  # Get road segment
  road_mask = road_segmnent(cap)

  results = model.predict(cap, device="mps", classes=[0, 1, 2, 3, 5, 7], verbose=False)
  result = results[0]

  boxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
  classes = np.array(result.boxes.cls.cpu(), dtype="int")
  masks = result.masks.xy

  for cls, box, mask in zip(classes, boxes, masks):
    (x, y, x2, y2) = box
    points = np.int32([mask])
    cv2.fillPoly(cap, points, (0, 0, 0))

  # Get vehicle segment
  gray_image = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
  ret, thresh_binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY)

  # Calculate P
  road_pixel = np.sum(road_mask == 0)*0.5
  vehicle_pixel = np.sum(thresh_binary == 0)
  P = vehicle_pixel/road_pixel*100

  if P > 50:
    return 'High'
  elif (P >= 20) & (P < 50):
    return 'Medium'
  else:
    return 'Low'


if __name__ == "__main__":
  image = sys.argv[1]
  density = indentify_density(image)
  print(density)
  sys.stdout.flush()
