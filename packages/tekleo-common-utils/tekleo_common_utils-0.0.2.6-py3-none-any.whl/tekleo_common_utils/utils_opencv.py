import math
from typing import Tuple, List
import cv2
import numpy
from numpy import ndarray
from injectable import injectable, autowired, Autowired
from tekleo_common_message_protocol import PointPixel, PointRelative
from tekleo_common_utils.utils_math import UtilsMath


@injectable
class UtilsOpencv:
    @autowired
    def __init__(self, utils_math: Autowired(UtilsMath)):
        self.utils_math = utils_math

    # Dimensions
    #-------------------------------------------------------------------------------------------------------------------
    def get_dimensions_hw(self, image_cv: ndarray) -> (int, int):
        h, w = image_cv.shape[:2]
        return h, w

    def get_dimensions_wh(self, image_cv: ndarray) -> (int, int):
        h, w = image_cv.shape[:2]
        return w, h

    def get_area(self, image_cv: ndarray) -> int:
        h, w = self.get_dimensions_hw(image_cv)
        return h * w

    def get_number_of_channels(self, image_cv: ndarray) -> int:
        if image_cv.ndim == 2:
            return 1
        elif image_cv.ndim == 3:
            return image_cv.shape[-1]
        else:
            raise ValueError("Weird image with ndim=" + str(image_cv.ndim))
    #-------------------------------------------------------------------------------------------------------------------

    def are_images_equal(self, image_cv_a: ndarray, image_cv_b: ndarray) -> bool:
        if image_cv_a.shape == image_cv_b.shape:
            difference = cv2.subtract(image_cv_a, image_cv_b)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                return True
            else:
                return False
        else:
            return False

    def convert_to_grayscale(self, image_cv: ndarray) -> ndarray:
        if self.get_number_of_channels(image_cv) == 1:
            return image_cv
        else:
            return cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Brightness range 0 to 510, same result = 255
    # Contrast range 0 to 254, same result = 127
    def brightness_and_contrast(self, image_cv: ndarray, brightness: int = 255, contrast: int = 127) -> ndarray:
        new_image_cv = image_cv.copy()
        brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
        contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

        # Apply brightness
        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                max = 255
            else:
                shadow = 0
                max = 255 + brightness
            al_pha = (max - shadow) / 255
            ga_mma = shadow

            # The function addWeighted calculates the weighted sum of two arrays
            new_image_cv = cv2.addWeighted(new_image_cv, al_pha, new_image_cv, 0, ga_mma)

        # Apply contrast
        if contrast != 0:
            alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            gamma = 127 * (1 - alpha)

            # The function addWeighted calculates the weighted sum of two arrays
            new_image_cv = cv2.addWeighted(new_image_cv, alpha, new_image_cv, 0, gamma)

        return new_image_cv

    def saturation(self, image_cv: ndarray, saturation_coefficient: float) -> ndarray:
        image_cv_hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(image_cv_hsv)
        s = s * saturation_coefficient
        s = numpy.clip(s,0,255)
        image_cv_hsv = cv2.merge([h,s,v])
        image_cv_bgr = cv2.cvtColor(image_cv_hsv.astype("uint8"), cv2.COLOR_HSV2BGR)
        return image_cv_bgr

    def hue(self, image_cv: ndarray, hue_coefficient: float) -> ndarray:
        image_cv_hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV).astype("float32")
        (h, s, v) = cv2.split(image_cv_hsv)
        h = h * hue_coefficient
        h = numpy.clip(h,0,255)
        image_cv_hsv = cv2.merge([h,s,v])
        image_cv_bgr = cv2.cvtColor(image_cv_hsv.astype("uint8"), cv2.COLOR_HSV2BGR)
        return image_cv_bgr

    def border(self, image_cv: ndarray, border_top: int, border_bottom: int, border_left: int, border_right: int, border_color: Tuple[int, int, int]) -> ndarray:
        new_image_cv = image_cv.copy()
        new_image_cv = cv2.copyMakeBorder(
            new_image_cv,
            top=border_top,
            bottom=border_bottom,
            left=border_left,
            right=border_right,
            borderType=cv2.BORDER_CONSTANT,
            value=[border_color[0], border_color[1], border_color[2]]
        )
        return new_image_cv

    def flip(self, image_cv: ndarray, flip_axis: str) -> ndarray:
        new_image_cv = image_cv.copy()
        flip_axis = flip_axis.strip().lower()
        if flip_axis == "x":
            new_image_cv = cv2.flip(new_image_cv, 1)
        elif flip_axis == "y":
            new_image_cv = cv2.flip(new_image_cv, 0)
        else:
            raise ValueError("Unknown flip_axis=" + str(flip_axis) + ", must be from ['x', 'y']")
        return new_image_cv

    def blur_gaussian(self, image_cv: ndarray, blur_x: int, blur_y: int) -> ndarray:
        new_image_cv = image_cv.copy()
        new_image_cv = cv2.GaussianBlur(new_image_cv, (blur_x, blur_y), 0)
        return new_image_cv

    def sharpen_blur(self, image_cv: ndarray, sharpen_blur_x: int, sharpen_blur_y) -> ndarray:
        new_image_cv = image_cv.copy()
        new_image_cv_smoothed = self.blur_gaussian(new_image_cv, sharpen_blur_x, sharpen_blur_y)
        new_image_cv_sharpened = cv2.addWeighted(new_image_cv, 1.5, new_image_cv_smoothed, -0.5, 0)
        return new_image_cv_sharpened

    def sharpen_kernel(self, image_cv: ndarray) -> ndarray:
        new_image_cv = image_cv.copy()

        kernel = numpy.array([
            [0, -1, 0],
            [-1, 5,-1],
            [0, -1, 0]
        ])

        # kernel = numpy.array([
        #     [-1, -1, -1],
        #     [-1, 9, -1],
        #     [-1, -1, -1]
        # ])

        # kernel = numpy.array([
        #     [-1, -1, -1],
        #     [-1, 8, -1],
        #     [-1, -1, 0]
        # ], numpy.float32)

        new_image_cv_sharpened = cv2.filter2D(src=new_image_cv, ddepth=-1, kernel=kernel)
        return new_image_cv_sharpened

    def get_most_occurring_color(self, image_cv: ndarray, apply_blur: bool = True) -> (int, int, int):
        if apply_blur:
            image_cv = self.blur_gaussian(image_cv, 25, 25)

        width, height, channels = image_cv.shape
        color_count_map = {}
        for y in range(0, height):
            for x in range(0, width):
                BGR = (int(image_cv[x, y, 0]), int(image_cv[x, y, 1]), int(image_cv[x, y, 2]))
                if BGR in color_count_map:
                    color_count_map[BGR] += 1
                else:
                    color_count_map[BGR] = 1
    
        max_count = 0
        max_BGR = (0, 0, 0)
        for BGR in color_count_map:
            count = color_count_map[BGR]
            if count > max_count:
                max_count = count
                max_BGR = BGR
    
        return max_BGR



    # Image transformations
    #-------------------------------------------------------------------------------------------------------------------
    # Rotate (with filling in background gaps, but preserving original dimensions of the image)
    def rotate_with_background_warp_bound(self, image_cv: ndarray, angle: float) -> ndarray:
        if angle == 0:
            return image_cv
        image_result = image_cv.copy()
        h, w = image_result.shape[:2]
        c_x, c_y, = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D((c_x, c_y), angle, 1.0)
        image_result = cv2.warpAffine(image_result, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return image_result

    # Rotate (with filling in background gaps, but changing dimensions of the original image)
    def rotate_with_background_warp_free(self, image_cv: ndarray, angle: float) -> ndarray:
        if angle == 0:
            return image_cv
        image_result = image_cv.copy()
        h, w = image_result.shape[:2]
        c_x, c_y, = (w // 2, h // 2)

        # Compute the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D((c_x, c_y), angle, 1.0)
        rotation_matrix_cos = numpy.abs(rotation_matrix[0, 0])
        rotation_matrix_sin = numpy.abs(rotation_matrix[0, 1])

        # Compute the new bounding dimensions of the image
        new_w = int((h * rotation_matrix_sin) + (w * rotation_matrix_cos))
        new_h = int((h * rotation_matrix_cos) + (w * rotation_matrix_sin))

        # Adjust the rotation matrix to take into account translation
        rotation_matrix[0, 2] += (new_w / 2) - c_x
        rotation_matrix[1, 2] += (new_h / 2) - c_y

        # Rotate
        image_result = cv2.warpAffine(image_result, rotation_matrix, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return image_result

    # Rotate (with cutting away any background gaps, and changing dimensions of the original image)
    def rotate_with_background_crop(self, image_cv: ndarray, angle: float) -> ndarray:
        if angle == 0:
            return image_cv
        image_result = image_cv.copy()
        h, w = image_result.shape[:2]
        c_x, c_y, = (w // 2, h // 2)

        # Compute the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D((c_x, c_y), angle, 1.0)
        rotation_matrix_cos = numpy.abs(rotation_matrix[0, 0])
        rotation_matrix_sin = numpy.abs(rotation_matrix[0, 1])

        # Compute the new bounding dimensions of the image (with a safezone)
        new_w = int((h * rotation_matrix_sin) + (w * rotation_matrix_cos)) + 4
        new_h = int((h * rotation_matrix_cos) + (w * rotation_matrix_sin)) + 4

        # Adjust the rotation matrix to take into account translation
        rotation_matrix[0, 2] += (new_w / 2) - c_x
        rotation_matrix[1, 2] += (new_h / 2) - c_y

        # Rotate (with black background)
        image_result = cv2.warpAffine(image_result, rotation_matrix, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)

        # Find rotated contours
        gray = self.convert_to_grayscale(image_result)
        blur = self.blur_gaussian(gray, 9, 9)
        contours, hierarchy = cv2.findContours(blur, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)

        # Find largest contour, approximate it, and get its points
        contour = contours[0]
        contour_length = cv2.arcLength(contour, True)
        contour = cv2.approxPolyDP(contour, 0.001 * contour_length, True)
        x_values = sorted(set([p[0][0] for p in contour]))
        y_values = sorted(set([p[0][1] for p in contour]))
        x_values = self.utils_math.reduce_list_int(x_values, reduction_delta=3)
        y_values = self.utils_math.reduce_list_int(y_values, reduction_delta=3)

        # Apply crop to the image (with safezone)
        if len(y_values) > 2:
            y_values.remove(min(y_values))
            y_values.remove(max(y_values))
        if len(x_values) > 2:
            x_values.remove(min(x_values))
            x_values.remove(max(x_values))
        crop_y_start = min(y_values) + 4
        crop_y_end = max(y_values) - 4
        crop_x_start = min(x_values) + 4
        crop_x_end = max(x_values) - 4
        image_result = image_result[crop_y_start:crop_y_end, crop_x_start:crop_x_end]

        # Return result
        return image_result

    # Rotate 90 degrees, with added points
    def rotate_90(self, image_cv: ndarray, points: List[PointPixel], orientation: str) -> (ndarray, List[PointPixel]):
        image_result = image_cv.copy()
        h, w = image_result.shape[:2]
        c_x, c_y, = (w // 2, h // 2)

        # Determine angle
        angle = 0
        orientation = orientation.strip().lower()
        if orientation == 'r' or orientation == 'right':
            angle = -90
        elif orientation == 'l' or orientation == 'left':
            angle = 90
        else:
            raise ValueError("Unknown orientation value = " + str(orientation))

        # Compute the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D((c_x, c_y), angle, 1.0)
        rotation_matrix_cos = numpy.abs(rotation_matrix[0, 0])
        rotation_matrix_sin = numpy.abs(rotation_matrix[0, 1])

        # Compute the new bounding dimensions of the image
        new_w = int((h * rotation_matrix_sin) + (w * rotation_matrix_cos))
        new_h = int((h * rotation_matrix_cos) + (w * rotation_matrix_sin))

        # Adjust the rotation matrix to take into account translation to the center
        rotation_matrix[0, 2] += (new_w / 2) - c_x
        rotation_matrix[1, 2] += (new_h / 2) - c_y

        # Rotate (with black background)
        image_result = cv2.warpAffine(image_result, rotation_matrix, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT)

        # Rotate points
        points_result = []
        for point in points:
            np_point = numpy.array([[[point.x, point.y]]], dtype = "float32")
            np_rotated_point = cv2.transform(np_point, rotation_matrix)
            rotated_point = PointPixel(int(np_rotated_point[0][0][0]), int(np_rotated_point[0][0][1]))
            points_result.append(rotated_point)

        # Return result
        return (image_result, points_result)

    # Rotate (smartly, deciding which way of rotation will work better here)
    def rotate(self, image_cv: ndarray, angle: float, rotate_bound_threshold_angle: float = 20.0) -> ndarray:
        if -1.0 * rotate_bound_threshold_angle <= angle <= rotate_bound_threshold_angle:
            return self.rotate_with_background_warp_bound(image_cv, angle)
        else:
            return self.rotate_with_background_warp_free(image_cv, angle)

    # Blend a background image with an alpha channeled foreground image, with an additional factor to tune how strongly the alpha is applied
    # foreground_alpha_factor = 0.1 will result in more transparent blend
    # foreground_alpha_factor = 1.0 will preserve the alpha channel fully
    def blend(self, background_image_cv: ndarray, foreground_image_cv: ndarray, foreground_alpha_cv: ndarray, foreground_alpha_factor: float = 1) -> ndarray:
        # To be safe make copies here
        background_image_cv = background_image_cv.copy()
        foreground_image_cv = foreground_image_cv.copy()
        foreground_alpha_cv = foreground_alpha_cv.copy()

        # Convert uint8 to float
        foreground = foreground_image_cv.astype(float)
        background = background_image_cv.astype(float)

        # Normalize the alpha mask to keep intensity between 0 and 1 and apply factor
        alpha = foreground_alpha_cv.astype(float) / 255
        alpha = alpha * foreground_alpha_factor

        # Multiply the foreground with the alpha matte
        foreground = cv2.multiply(alpha, foreground)

        # Multiply the background with (1 - alpha)
        background = cv2.multiply(1.0 - alpha, background)

        # Add the masked foreground and background.
        return numpy.uint8(cv2.add(foreground, background))
    #-------------------------------------------------------------------------------------------------------------------



    # Image deskewing
    #-------------------------------------------------------------------------------------------------------------------
    # Calculate skew angle of an image
    def calculate_skew_angle(self, image_cv: ndarray) -> float:
        # Prep image, copy, convert to gray scale, blur, and threshold
        image_result = image_cv.copy()
        gray = self.convert_to_grayscale(image_result)
        blur = self.blur_gaussian(gray, 9, 9)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Apply dilate to merge text into meaningful lines/paragraphs.
        # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
        # But use smaller kernel on Y axis to separate between different blocks of text
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilate = cv2.dilate(thresh, kernel, iterations=5)

        # Find all contours
        contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)
        if len(contours) == 0:
            return 0

        # Find largest contour and surround in min area box
        largestContour = contours[0]
        minAreaRect = cv2.minAreaRect(largestContour)

        # Determine the angle. Convert it to the value that was originally used to obtain skewed image
        angle = minAreaRect[-1]
        if angle < -45:
            angle = 90 + angle
            return -1.0 * angle
        elif angle > 45:
            angle = 90 - angle
            return angle
        return -1.0 * angle

    # Deskew image
    def deskew(self, image_cv: ndarray) -> (ndarray, float):
        angle = self.calculate_skew_angle(image_cv)
        rotated_image_cv = self.rotate(image_cv, -1.0 * angle)
        return rotated_image_cv, angle
    #-------------------------------------------------------------------------------------------------------------------



    def edge_detection(self, image_cv: ndarray) -> List[List[PointPixel]]:
        image_gray_cv = self.convert_to_grayscale(image_cv)
        image_blurred_cv = self.blur_gaussian(image_gray_cv, 3, 3)
        # image_threshold_cv = cv2.adaptiveThreshold(image_blurred_cv, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 11)
        ret, image_threshold_cv = cv2.threshold(image_blurred_cv, 100, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(image_threshold_cv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        new_contours = []
        min_countour_area = self.get_area(image_cv) * (0.3 / 100)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > min_countour_area:
                contour_length = cv2.arcLength(contour, True)
                reduced_contour = cv2.approxPolyDP(contour, 0.001 * contour_length, True)
                new_contours.append(reduced_contour)

        new_contours = sorted(new_contours, key = cv2.contourArea, reverse = True)

        contours_as_points = []
        for contour in new_contours:
            points = []
            for raw_point in contour:
                x = raw_point[0][0]
                y = raw_point[0][1]
                points.append(PointPixel(x, y))
            contours_as_points.append(points)

        return contours_as_points



    # Drawing
    #-------------------------------------------------------------------------------------------------------------------
    def draw_rectangle_rounded(self, image_cv: ndarray, top_left: Tuple[int, int], bottom_right: Tuple[int, int], radius_scale: float = 1.0, color: List[int] = [255, 255, 255], thickness: float = 1.0, line_type: int = cv2.LINE_AA) -> ndarray:
        # Make sure we make a copy
        image_cv = image_cv.copy()

        #  corners:
        #  p1 - p2
        #  |     |
        #  p4 - p3
        p1 = top_left
        p2 = (bottom_right[0], top_left[1])
        p3 = (bottom_right[0], bottom_right[1])
        p4 = (top_left[0], bottom_right[1])

        # Calculate corners
        height = abs(bottom_right[1] - top_left[1])
        corner_radius = int(radius_scale * (height / 2))

        if thickness < 0:
            #big rect
            top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
            bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

            top_left_rect_left = (p1[0], p1[1] + corner_radius)
            bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

            top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
            bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

            all_rects = [
                [top_left_main_rect, bottom_right_main_rect],
                [top_left_rect_left, bottom_right_rect_left],
                [top_left_rect_right, bottom_right_rect_right]]

            [cv2.rectangle(image_cv, rect[0], rect[1], color, thickness) for rect in all_rects]

        # draw straight lines
        cv2.line(image_cv, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
        cv2.line(image_cv, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
        cv2.line(image_cv, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
        cv2.line(image_cv, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

        # draw arcs
        cv2.ellipse(image_cv, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90, color, thickness, line_type)
        cv2.ellipse(image_cv, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90, color, thickness, line_type)
        cv2.ellipse(image_cv, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90, color, thickness, line_type)
        cv2.ellipse(image_cv, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90, color, thickness, line_type)

        return image_cv
    #-------------------------------------------------------------------------------------------------------------------
