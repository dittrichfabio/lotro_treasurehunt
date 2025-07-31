import cv2
import numpy as np
import os

def find_red_x_center(img):
    """Find the center of a red X (approx 20x20 px) based on RGB ranges."""
    # Threshold for red (you can tweak further if needed)
    lower = np.array([0, 0, 200])   # A bit lower than 228 to catch some variation
    upper = np.array([30, 30, 255]) # A bit above 14 for green and blue channels

    mask = cv2.inRange(img, lower, upper)
    coords = cv2.findNonZero(mask)

    if coords is None:
        raise ValueError("Red X not found in the image.")
    
    # Average coordinates to find the center
    avg = np.mean(coords, axis=0)[0]
    return int(avg[0]), int(avg[1])

def combine_images(img_top, img_left, img_br, show_markers=True):
    images = [img_top, img_left, img_br]
    merged = np.maximum.reduce(images)

    if not show_markers:
        x_size, y_size = 22, 22

        for i, img in enumerate(images):
            center = find_red_x_center(img)
            if center:
                x, y = center
                x1, x2 = x - x_size // 2, x + x_size // 2
                y1, y2 = y - y_size // 2, y + y_size // 2

                # Use the next image in the list as the clean patch source
                replacement_img = images[(i + 1) % 3]

                # Bounds check
                if (
                    0 <= x1 < x2 <= merged.shape[1]
                    and 0 <= y1 < y2 <= merged.shape[0]
                ):
                    merged[y1:y2, x1:x2] = replacement_img[y1:y2, x1:x2]
                else:
                    print(f"Skipping out-of-bounds patch at ({x}, {y})")

    return merged

def crop_image(img, top_left, bottom_right):
    """
    Crop the image using top-left and bottom-right coordinates.

    Args:
        img (np.ndarray): The image to crop.
        top_left (tuple): (x, y) coordinates for the top-left corner of the crop.
        bottom_right (tuple): (x, y) coordinates for the bottom-right corner of the crop.

    Returns:
        np.ndarray: The cropped image.
    """
    x1, y1 = top_left
    x2, y2 = bottom_right
    return img[y1:y2, x1:x2]


def process_images(img_top_path, img_left_path, img_br_path, output_prefix="combined_map", show_markers=True):
    img_top = cv2.imread(img_top_path)
    img_left = cv2.imread(img_left_path)
    img_br = cv2.imread(img_br_path)

    if img_top is None or img_left is None or img_br is None:
        raise FileNotFoundError("One or more input images could not be read.")

    merged = combine_images(img_top, img_left, img_br, show_markers=show_markers)

    # Save the merged image (with or without markers)
    combined_filename = f"{output_prefix}_full.png"
    cv2.imwrite(combined_filename, merged)
    print(f"Combined image saved to {combined_filename}")

    # Find center of red X in img_top (you can change to another image if needed)
    center_top = find_red_x_center(img_top)
    center_left = find_red_x_center(img_left)
    center_br = find_red_x_center(img_br)

    # Crop boundaries
    top_left = (center_left[0], center_top[1])
    bottom_right = center_br

    # Crop and save
    cropped = crop_image(merged, top_left, bottom_right)
    cropped_filename = f"{output_prefix}_cropped.png"
    cv2.imwrite(cropped_filename, cropped)
    print(f"Cropped image saved to {cropped_filename}")

# Example usage
if __name__ == "__main__":

    process_images(
        img_top_path="combine_map_images/img_top.jpg",
        img_left_path="combine_map_images/img_left.jpg",
        img_br_path="combine_map_images/img_br.jpg",
        output_prefix="combine_map_images/lotro_map",
        show_markers=False  # Set to False to remove the red Xs
    )
