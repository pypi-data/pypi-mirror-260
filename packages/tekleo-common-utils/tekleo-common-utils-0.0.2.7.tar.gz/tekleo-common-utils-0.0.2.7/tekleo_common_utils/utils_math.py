import math
from typing import List
from injectable import injectable
from tekleo_common_message_protocol import PointRelative, RectanglePixel


@injectable
class UtilsMath:
    # Remove values in a list that are too close to each other
    # List must be unique and sorted
    def reduce_list_int(self, values: List[int], reduction_delta: int = 1) -> List[int]:
        # If there are less than 2 elements - exit directly
        if len(values) < 2:
            return values

        # Resort the list
        values = sorted(set(values))

        # Go over each pair of values
        for i in range(0, len(values) - 1):
            current_value = values[i]
            next_value = values[i + 1]
            delta = abs(next_value - current_value)

            # If this is a candidate for reduction
            if delta <= reduction_delta:
                # Compute new value (as a midpoint) and replace it in the list
                new_value = int((current_value + next_value) / 2)
                values[i] = new_value
                values[i + 1] = new_value
                values = sorted(set(values))

                # Recursive call
                return self.reduce_list_int(values, reduction_delta)

        return values

    def points_add(self, point_a: PointRelative, point_b: PointRelative) -> PointRelative:
        return PointRelative(
            point_a.x + point_b.x,
            point_a.y + point_b.y
        )

    def points_subtract(self, point_a: PointRelative, point_b: PointRelative) -> PointRelative:
        return PointRelative(
            point_a.x - point_b.x,
            point_a.y - point_b.y
        )

    def points_multiply(self, point_a: PointRelative, point_b: PointRelative) -> PointRelative:
        return PointRelative(
            point_a.x * point_b.x - point_a.y * point_b.y,
            point_a.x * point_b.y + point_a.y * point_b.x
        )

    def point_multiply(self, point_a: PointRelative, c: float) -> PointRelative:
        return PointRelative(
            point_a.x * c,
            point_a.y * c
        )

    def point_rotate(self, point_a: PointRelative, point_center: PointRelative, angle: float) -> PointRelative:
        angle_radians = math.radians(angle)
        angle_cos = math.cos(angle_radians)
        angle_sin = math.sin(angle_radians)
        point_a_shifted = self.points_subtract(point_a, point_center)
        point_a_rotated = self.points_multiply(point_a_shifted, PointRelative(angle_cos, angle_sin))
        point_a_rotated_back = self.points_add(point_a_rotated, point_center)
        return point_a_rotated_back

    def does_rectangle_contain(self, rectangle_big: RectanglePixel, rectangle_small: RectanglePixel) -> bool:
        if rectangle_small.x > rectangle_big.x:
            if rectangle_small.x + rectangle_small.w < rectangle_big.x + rectangle_big.w:
                if rectangle_small.y > rectangle_big.y:
                    if rectangle_small.y + rectangle_small.h < rectangle_big.y + rectangle_big.h:
                        return True
        return False

    def do_rectangles_overlap(self, rectangle_a: RectanglePixel, rectangle_b: RectanglePixel) -> bool:
        # If they contain each other this is an overlap
        if self.does_rectangle_contain(rectangle_a, rectangle_b) or self.does_rectangle_contain(rectangle_b, rectangle_a):
            return True

        # If one rectangle is on left side of other
        if rectangle_a.x + rectangle_a.w < rectangle_b.x:
            return False
        if rectangle_b.x + rectangle_b.w < rectangle_a.x:
            return False

        # If one rectangle is above other
        if rectangle_a.y + rectangle_a.h < rectangle_b.y:
            return False
        if rectangle_b.y + rectangle_b.h < rectangle_a.y:
            return False

        return True
