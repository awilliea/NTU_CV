# coding: utf-8
# python3.7
import numpy as np
from PIL import Image


# dilation
def dilation(img_array,kernel,pixel):
    img_d = np.copy(img_array)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if(img_array[i][j]==pixel):
                for k in kernel:
                    new_x = i + k[0]
                    new_y = j + k[1]
                    if(new_x >=0 and new_x<img_array.shape[0] and new_y>=0 and new_y<img_array.shape[1]):
                        img_d[new_x][new_y] = pixel
    return img_d

# erosion
def erosion(img_array,kernel,pixel):
    img_e = np.copy(img_array)
    length = len(kernel)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            count = 0
            for k in kernel:
                new_x = i + k[0]
                new_y = j + k[1]
                if(new_x >=0 and new_x<img_array.shape[0] and new_y>=0 and new_y<img_array.shape[1] and img_array[new_x][new_y]==pixel):
                    count += 1
            if(count < length):
                img_e[i][j] = 255-pixel
            if(count == length):
                img_e[i][j] = pixel
    return img_e

# hit and miss
def hit_and_miss(img_array,kernel_J,kernel_K,pixel):
    img_e_positive = erosion(img_array,kernel_J,pixel)
    img_e_negative = erosion(img_array,kernel_K,255-pixel)
    img_h_a_m = np.copy(img_e_positive)
    
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            if(img_h_a_m[i][j] == pixel):
                if(img_e_negative[i][j] != 255-pixel):
                    img_h_a_m[i][j] = 255-pixel
    return img_h_a_m

def opening(img_array,kernel,pixel):
    return dilation(erosion(img_array,kernel,pixel),kernel,pixel)

def closing(img_array,kernel,pixel):
    return erosion(dilation(img_array,kernel,pixel),kernel,pixel)

def main():
    
    # origin
    img = Image.open('lena.bmp')
    img_array = np.array(img)
    Image.fromarray(img_array).save('lena.jpg')
    
    # binary
    print("Binarize the origin picture..\n")
    img_b_array = np.uint8(np.copy(img_array)>=128)*255
    Image.fromarray(img_b_array).save('lena_bin_128.jpg')
    
    # kernel is a 3-5-5-5-3 octagon, where
    kernel = [     [-2, -1], [-2, 0], [-2, 1],
              [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
              [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
              [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
                  [2, -1], [2, 0], [2, 1]]
    kernel_J = [[1,0], [0,0],[0,-1]]
    kernel_K = [[0,1],[-1,1],[-1,0]]
    
    # Dilation
    print("Dilate the binary picture..\n")
    img_d = dilation(img_b_array,kernel,255)
    Image.fromarray(img_d).save('lena_bin_dil.jpg')
    
    # Erosion
    print("Erose the binary picture..\n")
    img_e = erosion(img_b_array,kernel,255)
    Image.fromarray(img_e).save('lena_bin_ero.jpg')
   
    # Opening 
    print("Do opening for the binary picture..\n")
    img_open = opening(img_b_array,kernel,255)
    Image.fromarray(img_open).save('lena_bin_open.jpg')
    
    # Closing
    print("Do closing for the binary picture..\n")
    img_close = closing(img_b_array,kernel,255)
    Image.fromarray(img_close).save('lena_bin_close.jpg')
    
    # Hit-and-Miss
    print("Do hit-and-miss for the binary picture..\n")
    img_h_a_m = hit_and_miss(img_b_array,kernel_J,kernel_K,255)
    Image.fromarray(img_h_a_m).save('lena_bin_ham.jpg')
    
    print("Done")

if __name__ == '__main__':
    main()
