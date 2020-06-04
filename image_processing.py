import cv2
import numpy as np

def rotate_image(mat, angle):
 # angle in degrees

 height, width = mat.shape[:2]
 image_center = (width / 2, height / 2)

 rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

 abs_cos = abs(rotation_mat[0, 0])
 abs_sin = abs(rotation_mat[0, 1])

 bound_w = int(height * abs_sin + width * abs_cos)
 bound_h = int(height * abs_cos + width * abs_sin)

 rotation_mat[0, 2] += bound_w / 2 - image_center[0]
 rotation_mat[1, 2] += bound_h / 2 - image_center[1]

 rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h),borderValue=(255, 255, 255))
 return rotated_mat

def skew_image(mat):
    height, width = mat.shape[:2]
    pts1 = np.float32([[130, 0], [185, 0], [117, 82]])
    pts2 = np.float32([[117, 0], [172, 0], [117, 82]])

    M = cv2.getAffineTransform(pts1, pts2)

    dst = cv2.warpAffine(mat, M,(width,height),borderValue=(255, 255, 255))
    return dst