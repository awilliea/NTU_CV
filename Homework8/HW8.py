
import numpy as np
import pandas as pd
from PIL import Image
import math
from IPython.display import display

def show(img_array):
    display(Image.fromarray(img_array))

def generate_noise(img_array):
    length = img_array.shape[0]
    img_gau10 = np.zeros_like(img_array)
    img_gau30 = np.zeros_like(img_array)
    img_salt01 = np.zeros_like(img_array)
    img_salt005 = np.zeros_like(img_array)
    
    for i in range(length):
        for j in range(length):
            img_gau10[i][j] = img_array[i][j] + 10*np.random.normal(0,1,None)
            img_gau30[i][j] = img_array[i][j] + 30*np.random.normal(0,1,None)
            
            temp = np.random.uniform(0,1,None)
            if (temp < 0.05):
                pass
            elif(temp > 0.95):
                img_salt005[i][j] = 255
            else:
                img_salt005[i][j] = img_array[i][j]
            
            if(temp < 0.1):
                pass
            elif(temp > 0.9):
                img_salt01[i][j] = 255
            else:
                img_salt01[i][j] = img_array[i][j]
    
    return np.uint8(img_gau10),np.uint8(img_gau30),np.uint8(img_salt01),np.uint8(img_salt005)



def box_filter_3(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+2,length+2))
    img_temp[1:length+1,1:length+1] += img_array

    img_box_f3 = np.zeros_like(img_array)
    i = 1
    
    while(i<length+1):
        j = 1
        IBUF = [0,0,0]
        it = 0
        count = 0
        for r,c in kernel_3:
            IBUF[it] += img_temp[i+r][j+c]
            count += 1
            if(count%3 == 0):
                it += 1
                count %= 3
        ISUM = sum(IBUF)
        
        while(j<length+1):
            if(j == 1):
                if(i == 1 or i == length):
                    img_box_f3[i-1][j-1] = ISUM/4
                else:
                    img_box_f3[i-1][j-1] = ISUM/6
            elif(j == length):
                if(i == 1 or i == length):
                    img_box_f3[i-1][j-1] = (ISUM-IBUF[0])/4
                else:
                    img_box_f3[i-1][j-1] = (ISUM-IBUF[0])/6
            else:
                temp = img_temp[i-1][j+1]+img_temp[i][j+1]+img_temp[i+1][j+1]
                ISUM = ISUM - IBUF[0] + temp
                IBUF = [IBUF[1],IBUF[2],temp]
                if(i == 1 or i == length):
                    img_box_f3[i-1][j-1] = ISUM/6
                else:
                    img_box_f3[i-1][j-1] = ISUM/9
            j += 1
        i += 1
    return img_box_f3

def box_filter_5(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+4,length+4))
    img_temp[2:length+2,2:length+2] += img_array

    img_box_f5 = np.zeros_like(img_array)
    i = 2
    
    while(i<length+2):
        j = 2
        IBUF = [0,0,0,0,0]
        it = 0
        count = 0
        for r,c in kernel_5:
            IBUF[it] += img_temp[i+r][j+c]
            count += 1
            if(count%5 == 0):
                it += 1
                count %= 5
        ISUM = sum(IBUF)
        
        while(j<length+2):
            if(j == 2):
                if(i == 2 or i == length+1):
                    img_box_f5[i-2][j-2] = ISUM/9
                elif(i == 3 or i == length):
                    img_box_f5[i-2][j-2] = ISUM/12
                else:
                    img_box_f5[i-2][j-2] = ISUM/15
            elif(j == length+1):
                if(i == 2 or i == length+1):
                    img_box_f5[i-2][j-2] = (ISUM-IBUF[0])/9
                elif(i == 3 or i == length):
                    img_box_f5[i-2][j-2] = (ISUM-IBUF[0])/12
                else:
                    img_box_f5[i-2][j-2] = (ISUM-IBUF[0])/15
            else:
                temp = img_temp[i-2][j+2]+img_temp[i-1][j+2]+img_temp[i][j+2]+img_temp[i+1][j+2]+img_temp[i+2][j+2]
                ISUM = ISUM - IBUF[0] + temp
                IBUF = [IBUF[1],IBUF[2],IBUF[3],IBUF[4],temp]
                
                if(j == 3 or j == length):
                    if(i == 2 or i == length+1):
                        img_box_f5[i-2][j-2] = ISUM/12
                    elif(i == 3 or i == length):
                        img_box_f5[i-2][j-2] = ISUM/16
                    else:
                        img_box_f5[i-2][j-2] = ISUM/20
                else:
                    if(i == 2 or i == length+1):
                        img_box_f5[i-2][j-2] = ISUM/15
                    elif(i == 3 or i == length):
                        img_box_f5[i-2][j-2] = ISUM/20
                    else:
                        img_box_f5[i-2][j-2] = ISUM/25
            j += 1
        i += 1
    return img_box_f5


def median_filter_3(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+2,length+2))-1
    img_temp[1:length+1,1:length+1] = img_array

    img_m_f3 = np.zeros_like(img_array)
    i = 1
    
    while(i<length+1):
        j = 1
        IBUF = []
        for r,c in kernel_3:
            if(img_temp[i+r][j+c] != -1):
                IBUF.append(img_temp[i+r][j+c])
        
        while(j<length+1):
            if(j == 1):
                img_m_f3[i-1][j-1] = np.median(IBUF)
            else:
                temp = []
                for t in range(-1,2,1):
                    if(img_temp[i+t][j+1] != -1):
                        temp.append(img_temp[i+t][j+1])
                if(i == 1 or i == length):
                    if(j == 2):
                        IBUF += temp
                    else:
                        IBUF = IBUF[2:]+temp
                else:      
                    if(j == 2):
                        IBUF += temp
                    else:
                        IBUF = IBUF[3:]+temp

                img_m_f3[i-1][j-1] = np.median(IBUF)
            j += 1
        i += 1
    return img_m_f3


def median_filter_5(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+4,length+4))-1
    img_temp[2:length+2,2:length+2] = img_array

    img_m_f5 = np.zeros_like(img_array)
    i = 2
    
    while(i<length+2):
        j = 2
        IBUF = []
        for r,c in kernel_5:
            if(img_temp[i+r][j+c] != -1):
                IBUF.append(img_temp[i+r][j+c])
        
        while(j<length+2):
            if(j == 2):
                img_m_f5[i-2][j-2] = np.median(IBUF)
            else:
                temp = []
                for t in range(-2,3,1):
                    if(img_temp[i+t][j+2] != -1):
                        temp.append(img_temp[i+t][j+2])
                        
                if(i == 2 or i == length+1):
                    if(j == 3 or j == 4):
                        IBUF += temp
                    else:
                        IBUF = IBUF[3:]+temp
                elif(i == 3 or i == length):
                    if(j == 3 or j == 4):
                        IBUF += temp
                    else:
                        IBUF = IBUF[4:]+temp
                else:      
                    if(j == 3 or j == 4):
                        IBUF += temp
                    else:
                        IBUF = IBUF[5:]+temp

                img_m_f5[i-2][j-2] = np.median(IBUF)
            j += 1
        i += 1
    return img_m_f5

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

def opening_then_closing(img_array,kernel):
    return closing(opening(img_array,kernel),kernel)

def closing_then_opening(img_array,kernel):
    return opening(closing(img_array,kernel),kernel)


def clean_noise(noise_image,kernel):
    noise = ['gau10','gau30','salt005','salt01']
    methods = ['box3','box5','median3','median5','oc','co']
    for i,nm in enumerate(noise_image):
        print(noise[i])
        temp1 = np.uint8(box_filter_3(nm))
        temp2 = np.uint8(box_filter_5(nm))
        temp3 = np.uint8(median_filter_3(nm))
        temp4 = np.uint8(median_filter_5(nm))
        temp5 = np.uint8(opening_then_closing(nm,kernel))
        temp6 = np.uint8(closing_then_opening(nm,kernel))
        Image.fromarray(nm).save('lena_'+noise[i]+'.bmp')
        Image.fromarray(temp1).save('lena_'+noise[i]+'_'+methods[0]+'.bmp')
        Image.fromarray(temp2).save('lena_'+noise[i]+'_'+methods[1]+'.bmp')
        Image.fromarray(temp3).save('lena_'+noise[i]+'_'+methods[2]+'.bmp')
        Image.fromarray(temp4).save('lena_'+noise[i]+'_'+methods[3]+'.bmp')
        Image.fromarray(temp5).save('lena_'+noise[i]+'_'+methods[4]+'.bmp')
        Image.fromarray(temp6).save('lena_'+noise[i]+'_'+methods[5]+'.bmp')
        

def SN_ration(img_array,img_noise):
    length = img_array.shape[0]
    us = np.sum(img_array)/(length*length)
    vs = np.sum((img_array-us)**2)/(length*length)
    unoise = np.sum(img_noise - img_array)/(length*length)
    vn = np.sum((img_noise - img_array - unoise)**2)/(length*length)
    return 20*math.log10(vs**0.5/vn**0.5)

        
def cacualte_all_SN_ratio(img_array):
    noise = ['gau10','gau30','salt005','salt01']
    methods = ['no noise_cleaning','box3','box5','median3','median5','oc','co']
    datas = []
    for m in methods:
        data = []
        for n in noise:
            if(m=='no noise_cleaning'):
                img_n = Image.open('lena_'+n+'.bmp')
            else:
                img_n = Image.open('lena_'+n+'_'+m+'.bmp')
            img_noise = np.array(img_n)
            data.append(SN_ration(img_array,img_noise))
        datas.append(data)
    return pd.DataFrame(datas,columns = noise,index=methods)

def main():
    img = Image.open('lena.bmp')
    img_array = np.array(img)
    Image.fromarray(img_array)
    Image.fromarray(img_array).save('lena.jpg')
    img_gau10,img_gau30,img_salt01,img_salt005 = generate_noise(img_array)
    
    SN_R_list = [SN_ration(img_array,img_gau10),SN_ration(img_array,img_gau30),SN_ration(img_array,img_salt005),SN_ration(img_array,img_salt01)]
    print('SN_Ration for gau10, gau30, salt005, salt01:',SN_R_list)
    kernel_3 = [[j,i] for i in range(-1,2,1) for j in range(-1,2,1)]
    kernel_5 = [[j,i] for i in range(-2,3,1) for j in range(-2,3,1)]
    kernel = [     [-2, -1], [-2, 0], [-2, 1],
              [-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2],
              [0, -2], [0, -1], [0, 0], [0, 1], [0, 2],
              [1, -2], [1, -1], [1, 0], [1, 1], [1, 2],
              [2, -1], [2, 0], [2, 1]]
    
    clean_noise(noise_image,kernel)
    df = cacualte_all_SN_ratio(img_array)
    print(df)
    print('All Done!)


if __name__ == '__main__':
    main()

