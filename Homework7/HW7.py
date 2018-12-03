
# origin image
import numpy as np
from PIL import Image
from IPython.display import display

def show(img_array):
    display(Image.fromarray(img_array))

def down_sample(img_array,row,col):
    length = img_array.shape[0] 
    img_d_array = np.zeros((int(length/row),int(length/col)))
    for i in range(0,length,row):
        for j in range(0,length,col):
            img_d_array[int(i/row)][int(j/col)] = img_array[i][j]
    return img_d_array

def h(b,c,d,e):
    if(b != c):
        return 's'
    elif(b == c and (d!=b or e!= c)):
        return 'q'
    else:
        return 'r'
    
def h_s(b,c,d,e):
    if(b == c and (b!=d or b!=e)):
        return 1
    else:
        return 0

def Yokoi(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+2,length+2))
    img_temp[1:length+1,1:length+1] += img_array
    
    img_yok = np.zeros((length,length))
    dic = {'q':0,'r':0,'s':0}
    
    for i in range(1,length+1,1):
        for j in range(1,length+1,1):
            if(img_temp[i][j] != 0):
                dic[h(img_temp[i][j],img_temp[i+1][j],img_temp[i+1][j-1],img_temp[i][j-1])] += 1
                dic[h(img_temp[i][j],img_temp[i][j-1],img_temp[i-1][j-1],img_temp[i-1][j])] += 1
                dic[h(img_temp[i][j],img_temp[i-1][j],img_temp[i-1][j+1],img_temp[i][j+1])] += 1
                dic[h(img_temp[i][j],img_temp[i][j+1],img_temp[i+1][j+1],img_temp[i+1][j])] += 1

                if(dic['r'] == 4):
                    img_yok[i-1][j-1] = 5
                else:
                    img_yok[i-1][j-1] = dic['q']

                for key in dic.keys():
                    dic[key] = 0
    return img_yok

# 1:marked 0: others
def is_marked(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+2,length+2))
    img_temp[1:length+1,1:length+1] += img_array
    
    img_marked = np.zeros((length,length))
    for i in range(1,length+1,1):
        for j in range(1,length+1,1):
            if(img_temp[i][j] == 1):
                if(img_temp[i][j+1] == 1 or img_temp[i][j-1] == 1 or img_temp[i+1][j] == 1 or img_temp[i-1][j] == 1):
                    img_marked[i-1][j-1] = 1            
    return img_marked


# 1:shrinkable 0:stay origin
def is_shrinked(img_array,i,j):
    x0 = img_array[i][j]
    x1 = img_array[i][j+1]
    x2 = img_array[i-1][j]
    x3 = img_array[i][j-1]
    x4 = img_array[i+1][j]
    x5 = img_array[i+1][j+1]
    x6 = img_array[i-1][j+1]
    x7 = img_array[i-1][j-1]
    x8 = img_array[i+1][j-1]
    
    count = 0
    count += (h_s(x0,x1,x6,x2)+h_s(x0,x2,x7,x3)+h_s(x0,x3,x8,x4)+h_s(x0,x4,x5,x1))
    if(count == 1):
        return 1
    else:
        return 0

def thin(img_array):
    img_yok = Yokoi(img_array)
    img_marked = is_marked(img_yok)
    
    length = img_array.shape[0]
    img_temp = np.zeros((length+2,length+2))
    img_temp[1:length+1,1:length+1] += img_array
    img_thin = np.copy(img_array)
    
    count = 0
    for i in range(1,length+1,1):
        for j in range(1,length+1,1):
            if(img_temp[i][j] != 0):
                s = is_shrinked(img_temp,i,j)
                if(s == 1 and img_marked[i-1][j-1] == 1):
                    img_temp[i][j] = 0
                    img_thin[i-1][j-1] = 0
    return img_thin

def thin_iter(img_array):
    img_thin = thin(img_array)
    img_temp = np.copy(img_array)
    
    while(np.sum(img_temp!=img_thin)>0):
        img_temp = np.copy(img_thin)
        img_thin = thin(img_thin)
    return img_thin


def main():
    img = Image.open('lena.bmp')
    img_array = np.array(img)
    Image.fromarray(img_array)
    Image.fromarray(img_array).save('lena.jpg')
    
    img_b_array = np.uint8(np.copy(img_array)>=128)*255
    Image.fromarray(img_b_array).s ave('lena_b.jpg')
    
    img_d_array = np.uint8(down_sample(img_b_array,8,8))

    img_thin = np.uint8(thin_iter(img_d_array))
    Image.fromarray(img_thin).save('lena_thin.jpg')
    print('Done, the thin image is outputed as lena_thin.jpg')


if __name__ == '__main__':
    main()
