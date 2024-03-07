# Receipt Enhancer

Receipt Enhancer is a Python module designed to enhance and process images of receipts. It provides various functionalities for improving the quality of receipt images, including converting to grayscale, detecting lines using the Hough transform, enhancing local contrast, adaptive thresholding, and more.

## Features

- **Convert to Grayscale:** Converts the input image to grayscale for further processing.
- **Hough Line Detection:** Detects lines in the image using the Hough transform, useful for identifying borders and text regions.
- **Densest Region Detection:** Finds the densest region of lines in the image, often indicating the center of the receipt.
- **Image Rotation Correction:** Corrects the rotation of the image based on detected lines.
- **Adaptive Local Contrast Enhancement:** Enhances the local contrast of the image to improve visibility of text and details.
- **Adaptive Weighting:** Adjusts the intensity of image pixels based on local statistics to improve overall quality.
- **Adaptive Binary Thresholding:** Applies adaptive binary thresholding to segment the image into foreground and background regions.

## Installation

You can install Receipt Enhancer using pip:

```bash
pip install receipt-enhancer
```

## Usage

```python
from receipt_enhancer import ReceiptEnhancer
import cv2

# Initialize ReceiptEnhancer
enhancer = ReceiptEnhancer()

# Load an image
image = cv2.imread('receipt_image.jpg')

# Example Usage:
# Convert to grayscale
grey_image = enhancer.convert_to_greyscale(image)

# Detect lines using Hough transform
lines = enhancer.get_hough_lines(image, length=(50, 100), min_distance=(20, 50))

# Find densest region
densest_x, densest_y = enhancer.find_densest_region(image, lines)

# Correct rotation
corrected_image = enhancer.rotation_fix_hough_based(image, lines)

# Enhance local contrast
contrast_enhanced_image = enhancer.adaptive_local_contrast(image)

# Apply adaptive weighting
weighted_image = enhancer.adaptative_weight(image)

# Apply adaptive binary thresholding
binary_image = enhancer.adaptive_binary_threshold(image)
```

## Contributions

Contributions are welcome! If you have any suggestions, feature requests, or bug reports, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
