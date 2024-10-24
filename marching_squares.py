import numpy as np
import cv2


class MarchingSquares:
    def __init__(self, image_path, threshold=None):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Unable to load image")

        self.grid = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(float) / 255.0
        self.shape = img.shape[:2]  # Keep only height and width

        if threshold is None:
            self.threshold = np.mean(self.grid)
            print(f"Automatic threshold set to: {self.threshold:.3f}")
        else:
            self.threshold = threshold / 255.0
            print(f"Manual threshold set to: {self.threshold:.3f}")

        self.rows, self.cols = self.grid.shape

        self.CASES = {
            # No contour
            0: [],
            15: [],
            # Simple contours
            1: [[[0.5, 0], [0, 0.5]]],  # ╝
            2: [[[1, 0.5], [0.5, 0]]],  # ╚
            3: [[[1, 0.5], [0, 0.5]]],  # ═
            4: [[[1, 0.5], [0.5, 1]]],  # ╔
            6: [[[0.5, 0], [0.5, 1]]],  # ║
            7: [[[0, 0.5], [0.5, 1]]],  # ╗
            8: [[[0, 0.5], [0.5, 1]]],  # ╝
            9: [[[0.5, 0], [0.5, 1]]],  # ║
            11: [[[1, 0.5], [0.5, 1]]],  # ╔
            12: [[[0, 0.5], [1, 0.5]]],  # ═
            13: [[[0.5, 0], [1, 0.5]]],  # ╚
            14: [[[0.5, 0], [0, 0.5]]],  # ╗
            # Ambiguous cases
            5: [[[0.5, 0], [0, 0.5]], [[1, 0.5], [0.5, 1]]],
            10: [[[0.5, 0], [1, 0.5]], [[0, 0.5], [0.5, 1]]]
        }

    def get_square_value(self, row, col):
        value = 0
        corners = [
            (row + 1, col), (row + 1, col + 1),
            (row, col + 1), (row, col)
        ]

        for i, (r, c) in enumerate(corners):
            if self.grid[r, c] > self.threshold:
                value |= 1 << i

        return value

    def generate_contours(self):
        contours = []

        for row in range(self.rows - 1):
            for col in range(self.cols - 1):
                case = self.get_square_value(row, col)

                for segment in self.CASES[case]:
                    start = [col + segment[0][0], row + segment[0][1]]
                    end = [col + segment[1][0], row + segment[1][1]]
                    contours.append([start, end])

        return contours

    def draw_contours(self, thickness=1):
        result = np.full((*self.shape, 3), 255, dtype=np.uint8)
        contours = self.generate_contours()

        for segment in contours:
            pt1 = (int(segment[0][0]), int(segment[0][1]))
            pt2 = (int(segment[1][0]), int(segment[1][1]))
            cv2.line(result, pt1, pt2, (0, 0, 0), thickness)

        return result


def process_image(image_path, output_path="output.png", threshold=None, thickness=1):
    ms = MarchingSquares(image_path, threshold)
    result = ms.draw_contours(thickness)

    cv2.imwrite(output_path, result)
    print(f"Result saved to {output_path}")


if __name__ == "__main__":
    process_image("image.png", "output_auto.png")
    process_image("image.png", "output_manual.png", threshold=127)
    process_image("image.png", "output_auto_thick.png", thickness=2)
    process_image("image.png", "output_manual_thick.png", threshold=127, thickness=2)
