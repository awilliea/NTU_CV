# origin image
import numpy as np
from PIL import Image
img = Image.open('lena.bmp')
img_array = np.array(img)
Image.fromarray(img_array)
Image.fromarray(img_array).save('lena.jpg')

# 用來顯示圖片的函數
from IPython.display import display
def show(img_array):
    display(Image.fromarray(img_array))

def convolution(A,B):
    value = 0
    length = A.shape[0]
    assert A.shape == B.shape
    for i in range(length):
        for j in range(length):
            value += (A[i][j]*B[length-i-1][length-j-1])
    return value

def conv(A,kernel,threshold):
    length = A.shape[0]
    kernel_len = kernel.shape[0]
    img_conv = np.zeros((length-kernel_len+1,length-kernel_len+1))
    
    for i in range(img_conv.shape[0]):
        for j in range(img_conv.shape[1]):
            img_conv[i][j] = convolution(A[i:i+kernel_len,j:j+kernel_len],kernel)
    return np.uint8((img_conv<threshold)*255)

def conv_(A,kernel,threshold):
    length = A.shape[0]
    kernel_len = kernel.shape[0]
    img_conv = np.zeros((length-kernel_len+1,length-kernel_len+1))
    
    for i in range(img_conv.shape[0]):
        for j in range(img_conv.shape[1]):
            img_conv[i][j] = convolution(A[i:i+kernel_len,j:j+kernel_len],kernel)
    return np.uint8((img_conv>threshold)*255)
    threshold_lists = [15,15,20,3000,1]

def get_edge_picture(img_array,kernel_lists,threshold_lists):
    names = ['l1','l2','minvar','gau','diff']
    for i,k in enumerate(kernel_lists):
        if(names[i]!='diff'):
            img_temp = conv(img_array,k,threshold_lists[i])
            Image.fromarray(img_temp).save('lena_'+names[i]+'.bmp')
        else:
            img_temp = conv_(img_array,k,threshold_lists[i])
            Image.fromarray(img_temp).save('lena_'+names[i]+'.bmp')
        print('Get lena_'+names[i]+'.bmp')

def main():
    kernel_l1 = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    kernel_l2 = np.array([[1,1,1],[1,-8,1],[1,1,1]])/3
    kernel_minvar = np.array([[2,-1,2],[-1,-4,-1],[2,-1,2]])/3
    kernel_gau = np.array([
                [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
                [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
                [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
                [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
                [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
                [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
                [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
                [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
                [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
                [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
                [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]])
    kernel_diff = np.array([
                [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
                [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
                [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
                [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
                [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
                [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
                [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
                [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
                [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
                [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
                [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]])
    kernel_lists = [kernel_l1,kernel_l2,kernel_minvar,kernel_gau,kernel_diff]


    get_edge_picture(img_array,kernel_lists,threshold_lists)
    print('All Done')

if __name__ == '__main__':
    main()