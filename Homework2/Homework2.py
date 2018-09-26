# enviroment
# python 3.6.5

#### origin image
import numpy as np
from PIL import Image
import cv2

# 用來顯示圖片的函數
from IPython.display import display
def show(img_array):
    display(Image.fromarray(img_array))

img_array = cv2.imread('lena.bmp')
img_array_g = cv2.imread('lena.bmp',cv2.IMREAD_GRAYSCALE)

show(img_array)

# Problem 1
# binary image
img_b_array = np.zeros(img_array_g.shape,dtype = img_array.dtype)
for i in range(img_array_g.shape[0]):
    for j in range(img_array_g.shape[1]):
        if(img_array_g[i][j]<128):
            img_b_array[i][j] = 0
        else:
            img_b_array[i][j] = 255
show(img_b_array)
Image.fromarray(img_b_array).save('binary128.jpg')

# Problem 2
# histogram
import matplotlib.pyplot as plt
pixel_count = [0 for i in range(256)]
for p in img_array.flatten():
    pixel_count[int(p)] += 1
plt.title('Histogram of lena')
plt.ylabel('h(m)')
plt.plot([i for i in range(256)],pixel_count,color='black')
plt.savefig('histogram.jpg')

# Problem 3

# 4=connected label
def update_label_4connected(l,c,row_num,col_num,img_label):
    label = img_label[l][c]
    compare_list = [label]
    if (l > 0 and img_label[l-1][c] != 0):
        compare_list.append(img_label[l-1][c])
    if (l < row_num - 1 and img_label[l+1][c] != 0):
        compare_list.append(img_label[l+1][c])
    if (c > 0 and img_label[l][c-1] != 0):
        compare_list.append(img_label[l][c-1])
    if (c < col_num - 1 and img_label[l][c+1] != 0):
        compare_list.append(img_label[l][c+1])
    return min(compare_list)

# iterative algo caculate connected components
def iterative_algo(img_b_array):
    row_num,col_num = img_b_array.shape
    global_label = 0
    
    # initialize
    img_label = np.zeros(img_b_array.shape)
    for l in range(row_num):
        for c in range(col_num):
            if(img_b_array[l][c] != 0):
                global_label += 1
                img_label[l][c] = global_label
    
    # calculate components
    change = True
    run = 0
    while(change == True):
        change = False
        run += 1
        # Top down
        for l in range(row_num):
            for c in range(col_num):
                if(img_label[l][c] != 0):
                    m = update_label_4connected(l,c,row_num,col_num,img_label)
                    if (m != img_label[l][c]):
                        change = True
                    img_label[l][c] = m
        # bottom up
        for l in range(row_num-1,-1,-1):
            for c in range(col_num-1,-1,-1):
                if(img_label[l][c] != 0):
                    m = update_label_4connected(l,c,row_num,col_num,img_label)
                    if (m != img_label[l][c]):
                        change = True
                    img_label[l][c] = m
    return img_label

img_label = iterative_algo(img_b_array)

def caculate_labeldic_and_importantlabel(img_label,threshold):
    label_dic = {}
    for i in range(img_label.shape[0]):
        for j in range(img_label.shape[1]):
            if img_label[i][j] in label_dic:
                label_dic[img_label[i][j]] += 1
            else:
                label_dic[img_label[i][j]] = 1

    important_label = []
    for key in label_dic:
        if(label_dic[key] >= threshold and key != 0):
            important_label.append(key)
    
    return label_dic,important_label

label_dic,important_label = caculate_labeldic_and_importantlabel(img_label,500)

# caculate the centroids and the bounding boxes of the connected components
bounding_rows = [] 
bounding_cols = []
centers = []

for i in important_label:
    center = []
    
    up = 0
    down = 0
    boxes = []

    tmp = np.sum(img_label == i,axis = 1)
    count = 0
    for index,value in enumerate(tmp):
        if (up == 0 and value > 0):
            boxes.append(index)
            up = 1
        if (up == 1 and value == 0):
            boxes.append(index)
            break
        if (index == tmp.shape[0]-1 ):
            boxes.append(index)        
        count += (index+1)*value
        
    bounding_rows.append(boxes)
    center.append(int(count/tmp.sum()))
    
    up = 0
    down = 0
    boxes = []

    tmp = np.sum(img_label == i,axis = 0)
    count = 0
    for index,value in enumerate(tmp):
        if (up == 0 and value > 0):
            boxes.append(index)
            up = 1
        if (up == 1 and value == 0):
            boxes.append(index)
            break
        if (index == tmp.shape[0]-1 ):
            boxes.append(index)
        count += (index+1)*value
            
    bounding_cols.append(boxes)
    center.append(int(count/tmp.sum()))
    
    centers.append(center)

# plot the bounding boxes and the centroid on the lena picture
img_test = np.copy(img_array)
for i in range(len(important_label)):
    for l in range(512):
        if (l == bounding_rows[i][0] or l== bounding_rows[i][1]):
            for c in range(512):
                if(c >= bounding_cols[i][0] and c <= bounding_cols[i][1]):
                    img_test[l][c][0] = 0
                    img_test[l][c][1] = 0
                    img_test[l][c][2] = 255
                
        if (l >= bounding_rows[i][0] and l<= bounding_rows[i][1]):
            for c in range(512):
                if(c == bounding_cols[i][0] or c == bounding_cols[i][1]):
                    img_test[l][c][0] = 0
                    img_test[l][c][1] = 0
                    img_test[l][c][2] = 255
        
        if (l == centers[i][0]):
            for c in range(512):
                if(c == centers[i][1]):
                    for t in range(-8,8,1):
                        img_test[l+t][c][0] = 255
                        img_test[l+t][c][1] = 0
                        img_test[l+t][c][2] = 0
                        
                        img_test[l][c+t][0] = 255
                        img_test[l][c+t][1] = 0
                        img_test[l][c+t][2] = 0
show(img_test)
Image.fromarray(img_test).save('4connected.jpg')