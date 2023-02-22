import pylab as plt
from PIL import Image
import numpy as np


def calculate_H(a):
    if(a == 0):
        return 0
    else:
        return(a*np.log2(a))


def divide(a, b):
    if b == 0:
        return 0
    else:
        return a/b


#處理image
img = Image.open('image.png')

img = img.convert("1")  # 轉換成黑白影象


#img = img.resize((5, 5))  # 方便檢查，可刪
img = np.array(img)
img = img.astype(int)


img = np.ravel(img)


#iid
pb = img.mean()
pw = 1-pb
#print("pb : ", pb, "pw : ", pw)
H_iid = -((pb*np.log2(pb))+(pw*np.log2(pw)))
print("first Entropy(iid) : ", H_iid)

#first order markov model
n2 = [0, 0, 0, 0]  # 00 0->1 1->0 11
for i in range(len(img)-1):
    if(img[i] == 0 and img[i+1] == 0):
        n2[0] = n2[0]+1
    elif(img[i] == 0 and img[i+1] == 1):
        n2[1] = n2[1]+1
    elif(img[i] == 1 and img[i+1] == 0):
        n2[2] = n2[2]+1
    elif(img[i] == 1 and img[i+1] == 1):
        n2[3] = n2[3]+1

p2 = [0, 0, 0, 0]  # 00 0->1 1->0 11
p2[0] = divide(n2[0], (n2[0]+n2[2]))
p2[1] = divide(n2[1], (n2[0]+n2[2]))
p2[2] = divide(n2[2], (n2[1]+n2[3]))
p2[3] = divide(n2[3], (n2[1]+n2[3]))


H_first = (-(calculate_H(p2[2])+calculate_H(p2[3]))
           * pb-(calculate_H(p2[0])+calculate_H(p2[1]))*pw)
print("first order markov Entropy: ", H_first)

#second order markov model
n3 = [0, 0, 0, 0, 0, 0, 0, 0]  # 000 001 010 011 100 101 110 111
for i in range(len(img)-2):
    if(img[i] == 0 and img[i+1] == 0 and img[i+2] == 0):
        n3[0] = n3[0]+1
    if(img[i] == 0 and img[i+1] == 0 and img[i+2] == 1):
        n3[1] = n3[1]+1
    if(img[i] == 0 and img[i+1] == 1 and img[i+2] == 0):
        n3[2] = n3[2]+1
    if(img[i] == 0 and img[i+1] == 1 and img[i+2] == 1):
        n3[3] = n3[3]+1
    if(img[i] == 1 and img[i+1] == 0 and img[i+2] == 0):
        n3[4] = n3[4]+1
    if(img[i] == 1 and img[i+1] == 0 and img[i+2] == 1):
        n3[5] = n3[5]+1
    if(img[i] == 1 and img[i+1] == 1 and img[i+2] == 0):
        n3[6] = n3[6]+1
    if(img[i] == 1 and img[i+1] == 1 and img[i+2] == 1):
        n3[7] = n3[7]+1


p3 = [0, 0, 0, 0, 0, 0, 0, 0]  # 000 001 010 011 100 101 110 111
p3[0] = divide(n3[0], (n3[0]+n3[4]))
p3[1] = divide(n3[1], (n3[0]+n3[4]))
p3[2] = divide(n3[2], (n3[1]+n3[5]))
p3[3] = divide(n3[3], (n3[1]+n3[5]))
p3[4] = divide(n3[4], (n3[2]+n3[6]))
p3[5] = divide(n3[5], (n3[2]+n3[6]))
p3[6] = divide(n3[6], (n3[3]+n3[7]))
p3[7] = divide(n3[7], (n3[3]+n3[7]))


H_second = -(pw*p2[0]*(calculate_H(p3[0])+calculate_H(p3[1]))+pw*p2[1]*(calculate_H(p3[2])+calculate_H(p3[3]))
             + pb*p2[2]*(calculate_H(p3[4])+calculate_H(p3[5]))+pb*p2[3]*(calculate_H(p3[6])+calculate_H(p3[7])))
print("second order markov Entropy : ", H_second)

#diff
diff_0 = 0
diff_1 = 0
#dn1=0
for i in range(len(img)-1):
    k = int(img[i])-int(img[i+1])
    if(k == 0):
        diff_0 += 1
    else:
        diff_1 += 1
piff_0 = divide(diff_0, (diff_0+diff_1))
piff_1 = divide(diff_1, (diff_0+diff_1))
Hd = -(calculate_H(piff_0)+calculate_H(piff_1))
print("difference", Hd)
