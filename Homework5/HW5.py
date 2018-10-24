# coding: utf-8
# python3.7
import numpy as np
from PIL import Image


# dilation
def dilation(img_array,kernel):
    img_d = np.copy(img_array)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            max_ = 0
            for k in kernel:
                new_x = i + k[0]
                new_y = j + k[1]
                if(new_x >=0 and new_x<img_array.shape[0] and new_y>=0 and new_y<img_array.shape[1]):
                    max_ = max(max_,img_array[new_x][new_y])
            img_d[i][j] = max_

    return img_d

# erosion
def erosion(img_array,kernel):
    img_e = np.copy(img_array)
    length = len(kernel)
    for i in range(img_array.shape[0]):
        for j in range(img_array.shape[1]):
            min_ = 255
            count = 0
            for k in kernel:
                new_x = i + k[0]
                new_y = j + k[1]
                if(new_x >=0 and new_x<img_array.shape[0] and new_y>=0 and new_y<img_array.shape[1]):
                    count += 1
                    min_ = min(min_,img_array[new_x][new_y])
            if (count == length):
                img_e[i][j] = min_ 
            else:
                img_e[i][j] = 0
    return img_e

def opening(img_array,kernel):
    return dilation(erosion(img_array,kernel),kernel)

def closing(img_array,kernel):
    return erosion(dilation(img_array,kernel),kernel)

def main():
    
    # origin
    img = Image.open('lena.bmp')
    img_array = np.array(img)
    Image.fromarray(img_array).save('lena.jpg')
    
    # kernel is a 3-5-5-5-3 octagon, where
    kernel = [     [-2, -1], [-2, 0], [-2, 1],
              [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
              [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
              [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
                  [2, -1], [2, 0], [2, 1]]
    
    # Dilation
    print("Dilate the picture..\n")
    img_d = dilation(img_array,kernel)
    Image.fromarray(img_d).save('lena_dil.jpg')
    
    # Erosion
    print("Erose the picture..\n")
    img_e = erosion(img_array,kernel)
    Image.fromarray(img_e).save('lena_ero.jpg')
   
    # Opening 
    print("Do opening for the picture..\n")
    img_open = opening(img_array,kernel)
    Image.fromarray(img_open).save('lena_open.jpg')
    
    # Closing
    print("Do closing for the picture..\n")
    img_close = closing(img_array,kernel)
    Image.fromarray(img_close).save('lena_close.jpg')
    
    print("Done")

if __name__ == '__main__':
    main()
