from PIL import Image
import numpy as np
import generate
import os
from locale import atoi

# read all existing imgs
_, _, filenames = next(os.walk(os.path.join(os.getcwd(), "imgs")), (None, None, []))
filenames = [i.split(".")[0] for i in filenames]
# print(filenames)
all_imgs = [Image.open(os.path.join(os.getcwd(), "imgs", i+".bmp")) for i in filenames]
all_imgs_ratio_col_over_row = [im.size[0] / im.size[1] for im in all_imgs]
all_names = generate.get_latex_of_all_symbols()
# print(all_names)
# print(all_imgs_ratio_col_over_row)
# print(filenames[10])
# all_imgs[10].show()

# print(np.asarray(all_imgs[0].getdata()))

def get_dist_between_two_img(im1, im2):
    '''im1 and im2 should have the same size'''
    t1 = np.asarray(im1.getdata())
    t2 = np.asarray(im2.getdata())
    return np.sum(np.abs(t1 - t2))

def identify(img):
    # segment detection of the target img
    import seg
    all_seg, black_and_white = seg.seg_one_line_PIL_img(img)
    results = []
    for seg in all_seg:
        a, b, c, d = seg
        ratio_col_over_row = (b - a) / (d - c)
        sorted_names_indices = np.argsort(np.abs(ratio_col_over_row-np.asarray(all_imgs_ratio_col_over_row)))
        # print(filenames[sorted_names_indices[0]])
        target_im = Image.fromarray(black_and_white[c:d, a:b] * 255).convert("L").resize([32, 32])
        smallest_dist = 16 * 16 * 256 * 256
        best_fit_name = filenames[sorted_names_indices[0]]
        for i in range(len(filenames)):
            curr_index = sorted_names_indices[i]
            if np.abs(ratio_col_over_row - all_imgs_ratio_col_over_row[curr_index]) > 0.2:
                break
            im  = all_imgs[curr_index].copy().resize([32, 32])
            dist = get_dist_between_two_img(target_im, im)
            if dist < smallest_dist:
                smallest_dist = dist
                best_fit_name = filenames[curr_index]
        results.append(all_names[atoi(best_fit_name)])
    return results
