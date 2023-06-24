import cv2
import numpy as np
import torchvision.transforms as T
import rendering


def add_mask(img_path, alpha, color, color2, segment):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (1024, 1024))
    mask = rendering.process_image(img_path)
    mask = np.array(T.ToPILImage()(mask))

    _, binary_mask_1 = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
    _, binary_mask_2 = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    _, binary_mask_3 = cv2.threshold(mask, 2, 255, cv2.THRESH_BINARY)

    roof_mask = binary_mask_1 - binary_mask_2
    window_mask = binary_mask_2 - binary_mask_3
    b, g, r = cv2.split(img)
    img = cv2.merge((r, g, b))
    img_with_mask = np.copy(img)

    match segment:
        case 0:
            row_indices, col_indices = np.where(window_mask == 255)
            pixel_coordinates = list(zip(row_indices, col_indices))
            for row, col in pixel_coordinates:
                img_with_mask[col, row, :] = color

        case 1:
            row_indices, col_indices = np.where(roof_mask == 255)
            pixel_coordinates = list(zip(row_indices, col_indices))
            for row, col in pixel_coordinates:
                img_with_mask[col, row, :] = color2

        case 2:
            row_indices, col_indices = np.where(window_mask == 255)
            row_indices2, col_indices2 = np.where(roof_mask == 255)
            pixel_coordinates = list(zip(row_indices, col_indices))
            pixel_coordinates2 = list(zip(row_indices2, col_indices2))
            for row, col in pixel_coordinates:
                img_with_mask[col, row, :] = color
            for row, col in pixel_coordinates2:
                img_with_mask[col, row, :] = color2

        case _:
            return 0

    img_with_mask = cv2.addWeighted(img_with_mask, alpha, img, 1.0 - alpha, 0)
    return img_with_mask
