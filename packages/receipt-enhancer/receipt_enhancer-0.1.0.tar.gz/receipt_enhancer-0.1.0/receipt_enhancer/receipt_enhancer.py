from typing import List, Tuple
from numpy import ndarray
import numpy as np
import cv2


class ReceiptEnhancer:

    def convert_to_greyscale(self, image: ndarray) -> ndarray:
        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def get_hough_lines(self, image: np.ndarray,
                        length: Tuple[float, float],
                        min_distance: Tuple[float, float] = (0, 0)) -> List:

        if len(image.shape) > 2:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        grey = image
        binary = self.adaptive_binary_threshold(grey)

        mean_intensity = np.mean(image)
        resolution = min(image.shape[0], image.shape[1])

        canny_lower_threshold = int(max(0, mean_intensity * 0.5))
        canny_upper_threshold = int(min(255, mean_intensity * 1.5))

        aperture_size = max(3, int(resolution / 500))
        hough_threshold = max(1, int(mean_intensity / 10))

        max_gap = max(1, int(resolution / 100))

        borders = cv2.Canny(binary,
                            canny_lower_threshold,
                            canny_upper_threshold,
                            apertureSize=aperture_size)

        lines = cv2.HoughLinesP(borders, 1, np.pi / 180, threshold=hough_threshold,
                                minLineLength=int(length[0]), maxLineGap=max_gap)

        if lines is None:
            return []

        if min_distance == (0, 0):
            return lines

        min_dist, max_dist = min_distance
        filtered_lines = []
        line_set = set()

        for i in range(len(lines)):
            if i in line_set:
                continue
            for j in range(i + 1, len(lines)):
                if j in line_set:
                    continue
                dist = np.linalg.norm(np.array(lines[i][0][:2]) - np.array(lines[j][0][:2]))
                if min_dist <= dist <= max_dist:
                    filtered_lines.append(lines[i])
                    filtered_lines.append(lines[j])
                    line_set.add(i)
                    line_set.add(j)

        return filtered_lines

    def find_densest_region(self, image: ndarray, lines, proximity_threshold=50):
        max_density = 0
        best_x, best_y = 0, 0

        for line1 in lines:
            x1_1, y1_1, x2_1, y2_1 = line1[0]
            density = 0

            for line2 in lines:
                x1_2, y1_2, x2_2, y2_2 = line2[0]

                distance = np.sqrt((x1_1 - x1_2)**2 + (y1_1 - y1_2)**2) + \
                    np.sqrt((x2_1 - x2_2)**2 + (y2_1 - y2_2)**2)

                if distance < proximity_threshold:
                    density += 1

            if density > max_density:
                max_density = density
                best_x = (x1_1 + x2_1) // 2
                best_y = (y1_1 + y2_1) // 2

        return best_x, best_y

    def get_image_with_line_density_focused(self, image: ndarray, x: int, y: int):
        image = self.convert_to_greyscale(image)
        square_image = np.zeros_like(image)

        square_size = 100
        square_x1 = max(x - square_size // 2, 0)
        square_y1 = max(y - square_size // 2, 0)
        square_x2 = min(x + square_size // 2, image.shape[1])
        square_y2 = min(y + square_size // 2, image.shape[0])

        cv2.rectangle(square_image, (square_x1, square_y1),
                      (square_x2, square_y2), (255, 255, 255), cv2.FILLED)

        return square_image

    def get_document_slice_from_image_line_density_based(self, image: ndarray, densest_x: int, densest_y: int) -> ndarray:

        image = self.convert_to_greyscale(image)
        mean_intensity = np.mean(image)
        lower_paper_intensity = int(mean_intensity * 0.9)
        upper_paper_intensity = 255

        paper_mask = cv2.inRange(image, lower_paper_intensity, upper_paper_intensity)

        contours, _ = cv2.findContours(paper_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        x, y, w, h = densest_x, densest_y, 1, 1

        for contour in contours:
            x_c, y_c, w_c, h_c = cv2.boundingRect(contour)
            if x_c <= densest_x <= x_c + w_c and y_c <= densest_y <= y_c + h_c:
                x, y, w, h = x_c, y_c, w_c, h_c
                break

        return image[y:y + h, x:x + w]

    def rotation_fix_hough_based(self, image: ndarray,
                                 hough_lines: List[ndarray],
                                 image_return="default",
                                 debug=False) -> ndarray:

        grey = self.convert_to_greyscale(image)
        binary = self.adaptive_binary_threshold(grey)

        inclinations = []
        for line in hough_lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 != 0:
                inclinations.append(np.arctan((y2 - y1) / (x2 - x1)))

        angle = np.degrees(np.median(inclinations))

        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)

        corners = np.array([[0, 0], [width, 0], [width, height], [0, height]])
        rotated_corners = cv2.transform(np.array([corners]), rotation_matrix)[0]
        new_width = int(max(rotated_corners[:, 0]) - min(rotated_corners[:, 0]))
        new_height = int(max(rotated_corners[:, 1]) - min(rotated_corners[:, 1]))

        rotation_matrix[0, 2] += (new_width - width) / 2
        rotation_matrix[1, 2] += (new_height - height) / 2

        if debug:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            for line in hough_lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        return cv2.warpAffine({"default": image, "grey": grey, "binary": binary}.get(image_return),
                              rotation_matrix, (new_width, new_height), flags=cv2.INTER_CUBIC)

    def __get_adaptive_alpha_beta_gamma(self, image: ndarray) -> Tuple[float, float, float]:
        image = self.convert_to_greyscale(image)

        hist, _ = np.histogram(image.flatten(), 256, [0, 256])

        total_pixels = image.shape[0] * image.shape[1]
        cumulative_hist = np.cumsum(hist) / total_pixels
        min_val_idx = np.argmax(cumulative_hist > 0.01)
        max_val_idx = np.argmax(cumulative_hist > 0.99)

        min_val = min_val_idx if min_val_idx != max_val_idx else 0
        max_val = max_val_idx if max_val_idx != min_val_idx else 255

        alpha_denominator = max_val - min_val if max_val != min_val else 1.0
        alpha = 255.0 / alpha_denominator
        beta = -min_val * alpha

        mean = np.mean(image)
        gamma_denominator = mean / 255 if mean != 0 else 1.0
        gamma = np.log(0.5) / np.log(gamma_denominator) if np.log(gamma_denominator) != 0 else np.log(gamma_denominator)

        return alpha, beta, gamma

    def __segment_image_into_blocks(self, image: ndarray) -> List[ndarray]:
        mean_intensity = np.mean(image)
        block_size = max(int(mean_intensity / 10), 3)
        block_size = block_size + 1 if block_size % 2 == 0 else block_size
        block_size = max(block_size, 3)

        rows, cols = image.shape
        block_height = rows // block_size
        block_width = cols // block_size

        blocks = []
        for r in range(block_size):
            for c in range(block_size):
                block = image[r * block_height:(r + 1) * block_height, c * block_width:(c + 1) * block_width]
                blocks.append(block)

        return blocks

    def __build_image_from_blocks(self, blocks: List[ndarray]) -> ndarray:

        max_block_height = max(block.shape[0] for block in blocks)
        max_block_width = max(block.shape[1] for block in blocks)
        blocks_resized = [cv2.resize(block, (max_block_width, max_block_height)) for block in blocks]

        cols_per_row = int(np.sqrt(len(blocks_resized)))
        blocks_per_row = [blocks_resized[i:i + cols_per_row] for i in range(0, len(blocks_resized), cols_per_row)]

        return np.vstack([np.hstack(row_blocks) for row_blocks in blocks_per_row])

    def adaptive_local_contrast(self, image: np.ndarray) -> np.ndarray:
        image = self.convert_to_greyscale(image)
        blocks = self.__segment_image_into_blocks(image)

        adaptive_blocks_final = []

        for block in blocks:
            mean_block_intensity = np.mean(block)
            max_block_intensity = np.max(block)
            min_block_intensity = np.min(block)

            min_threshold = min_block_intensity + (mean_block_intensity * 0.05)
            max_threshold = max_block_intensity - (mean_block_intensity * 0.05)

            _, dark_regions = cv2.threshold(block, min_threshold, 255, cv2.THRESH_BINARY)
            _, bright_regions = cv2.threshold(block, max_threshold, 255, cv2.THRESH_BINARY_INV)

            dark_mask = cv2.bitwise_not(dark_regions)
            bright_mask = cv2.bitwise_not(bright_regions)
            tile_grid_size = max(8, int(mean_block_intensity * 0.03))

            clahe = cv2.createCLAHE(clipLimit=min(2.0, mean_block_intensity * 0.05),
                                    tileGridSize=(tile_grid_size, tile_grid_size))

            block_clahe = clahe.apply(block.astype(np.uint8))

            texture_smoothed_block = cv2.bilateralFilter(block_clahe,
                                                         d=max(10, int(0.1 * tile_grid_size)),
                                                         sigmaColor=int(0.1 * mean_block_intensity),
                                                         sigmaSpace=int(0.1 * tile_grid_size))

            black_adjustment = min(1.0, max(0.6, (min_block_intensity - 10) / 255))
            black_adaptive = cv2.convertScaleAbs(texture_smoothed_block, alpha=black_adjustment, beta=0)

            white_adjustment = min(1.0, (255 - max_block_intensity) / 255)
            white_adaptive = cv2.convertScaleAbs(texture_smoothed_block, alpha=white_adjustment, beta=0)

            black_adaptive = cv2.bitwise_and(black_adaptive, black_adaptive, mask=bright_mask)
            white_adaptive = cv2.bitwise_and(white_adaptive, white_adaptive, mask=dark_mask)

            adaptive_block = cv2.addWeighted(block_clahe, 1, black_adaptive, 0.3, 0)
            adaptive_block = cv2.addWeighted(adaptive_block, 1, white_adaptive, 0.3, 0)
            adaptive_block_color = cv2.cvtColor(adaptive_block, cv2.COLOR_GRAY2BGR)

            adaptive_block = cv2.bilateralFilter(adaptive_block_color,
                                                 d=max(10, int(0.1 * tile_grid_size)),
                                                 sigmaColor=int(0.1 * mean_block_intensity),
                                                 sigmaSpace=int(0.1 * tile_grid_size))

            local_std_dev = np.std(adaptive_block)

            sharpness_strength = max(0.2, min(1.0, local_std_dev / 100))
            sharpness_block = cv2.detailEnhance(adaptive_block, sigma_s=sharpness_strength, sigma_r=0.5)
            sharpness_block = cv2.cvtColor(sharpness_block, cv2.COLOR_BGR2GRAY)

            adaptive_blocks_final.append(sharpness_block)

        adaptive_image = self.__build_image_from_blocks(adaptive_blocks_final)

        std_dev = np.std(adaptive_image)

        adaptive_image = cv2.bilateralFilter(adaptive_image,
                                             d=max(10, int(0.1 * std_dev)),
                                             sigmaColor=int(0.1 * std_dev),
                                             sigmaSpace=int(0.1 * std_dev))

        return adaptive_image

    def adaptative_weight(self, image: ndarray) -> ndarray:
        image = self.convert_to_greyscale(image)

        blocks = self.__segment_image_into_blocks(image)

        adaptive_blocks = []
        for block in blocks:
            alpha, beta, gamma = self.__get_adaptive_alpha_beta_gamma(block)
            adaptive_block = cv2.convertScaleAbs(cv2.addWeighted(block, alpha, np.zeros_like(block), 0, beta))
            adaptive_blocks.append(adaptive_block)

        adapative_image = self.__build_image_from_blocks(adaptive_blocks)

        return adapative_image

    def adaptive_binary_threshold(self, image: ndarray) -> ndarray:

        image = self.convert_to_greyscale(image)
        blocks = self.__segment_image_into_blocks(image)
        binary_blocks = []

        for block in blocks:
            _, block_binary = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            binary_blocks.append(block_binary)

        binary_image = self.__build_image_from_blocks(binary_blocks)
        return binary_image
