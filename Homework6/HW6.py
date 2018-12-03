# origin image
import numpy as np
from PIL import Image

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

def Yokoi(img_array):
    length = img_array.shape[0]
    img_temp = np.zeros((length+2,length+2))
    img_temp[1:length+1,1:length+1] += img_array
    
    img_yok = np.zeros((length,length))-1
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

def output_Yokoi(img_yok):
    with open('Output_ver1.txt','w') as file:
        length = img_yok.shape[0]
        for i in range(length):
            for j in range(length):
                if(img_yok[i][j] == -1):
                    file.write("  ")
                else:
                    file.write(str(img_yok[i][j])+" ")
        file.write('\n')
    with open('Output_ver2.txt','w') as file:
        length = img_yok.shape[0]
        for i in range(length):
            for j in range(length):
                if(img_yok[i][j] == -1):
                    file.write(" ")
                    else:
                        file.write(str(img_yok[i][j]))
            file.write('\n')


def main():
    img = Image.open('lena.bmp')
    img_array = np.array(img)
    Image.fromarray(img_array)
    Image.fromarray(img_array).save('lena.jpg')

    img_b_array = np.uint8(np.copy(img_array)>=128)*255
    img_d_array = np.uint8(down_sample(img_b_array,8,8))
    img_yok = np.int8(Yokoi(img_d_array))
    output_Yokoi(img_yok)
    print('Done, the yokoi file is in your Output_ver1.txt and Output_ve2.txt !')

if __name__ == '__main__':
    main()
