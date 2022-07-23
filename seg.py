from PIL import Image
import numpy as np

def convert_to_black_and_white(im):
    ''' 
    im: PIL image 
    return: numpy 2d array with 0-1 values
    '''
    NUM_ROW = im.size[1]
    NUM_COL = im.size[0]
    pix_val = np.asarray(im.getdata())
    black_and_white = np.zeros((NUM_ROW, NUM_COL))
    index = 0
    # print(pix_val[0])
    for i in range(NUM_ROW):
        for j in range(NUM_COL):
            temp = np.mean(pix_val[index][:3])
            if temp < 100:
                black_and_white[i][j] = 1
            else:
                black_and_white[i][j] = 0
            index += 1
    # Image.fromarray(black_and_white * 255).show()
    return (NUM_ROW, NUM_COL, black_and_white)

def seg_one_line_PIL_img(PIL_im):
    # print(im.format, im.size, im.mode)
    NUM_ROW, NUM_COL, black_and_white = convert_to_black_and_white(PIL_im)
    sum_array = black_and_white.sum(axis=0)
    curr_pos = 0
    all_seg = [] # record (start, end) of all segments
    def bound_up_down(b, e): # find the upper and lower position of a segment in (b, e)
        hori_sum = black_and_white[:, b:e].sum(axis=1)
        for i in range(NUM_ROW):
            if hori_sum[i] != 0:
                r1 = i
                break
        for i in range(NUM_ROW):
            if hori_sum[NUM_ROW - 1 - i] != 0:
                r2 = NUM_ROW - 1 - i
                break
        return (r1, r2+1)
    for i in range(NUM_COL):
        if sum_array[i] == 0:
            if i != curr_pos:
                # seg finished
                r1, r2 = bound_up_down(curr_pos, i)
                all_seg.append((curr_pos, i, r1, r2))
                curr_pos = i + 1
                continue
            curr_pos += 1
    if i != curr_pos - 1:
        r1, r2 = bound_up_down(curr_pos, i)
        all_seg.append((curr_pos, i, r1, r2))
    # print(all_seg)
    return all_seg, black_and_white

def seg_one_line(filename):
    im = Image.open(filename)
    return seg_one_line_PIL_img(im)
    

def seg_by_connected_parts(filename):
    '''Use union-find algorithm to determine the connected parts'''
    pass