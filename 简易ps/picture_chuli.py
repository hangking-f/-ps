import math

import cv2
import numpy as np

####################灰度图和二值化########################################

def gray_picture(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return img_gray

def erzhihua(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rst = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    return rst[1]

##################加噪###########################################################
def jynoisy(img,num):    #椒盐彩色
    result = img.copy()
    w, h = img.shape[:2]
    for i in range(num):
        # 宽和高的范围内生成一个随机值，模拟表x,y坐标
        x = np.random.randint(1, w)
        y = np.random.randint(1, h)
        if np.random.randint(0, 2) == 0:
            # 生成白色噪声（盐噪声）
            result[x, y] = 0
        else:
            # 生成黑色噪声（椒噪声）
            result[x, y] = 255
    return result


def gsnoise(img,mean,sigma):       #添加高斯噪音
    img = np.array(img / 255, dtype=float)
    noise = np.random.normal(mean, sigma ** 0.5, img.shape)
    out_img = img + noise
    if out_img.min() < 0:
        low_clip = -1
    else:
        low_clip = 0
        out_img = np.clip(out_img, low_clip, 1.0)
        out_img = out_img * 255
    return out_img


################图像锐化#####################
def laplas(img):                                               #拉普拉斯变化
    lap_9 = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # 拉普拉斯9的锐化
    img = cv2.filter2D(img, cv2.CV_8U, lap_9)
    return img

def gama(img,power1=1.5):                              #伽马变化
    if len(img.shape) == 3:
         img= cv2.cvtColor(img,cv2.CV_8U)
    img = 255*np.power(img/255,power1)
    img = np.around(img)
    img[img>255] = 255
    out_img = img.astype(np.uint8)
    return out_img



################图像去噪####################################################
def medianBlurfun(img):      #中值滤波
    img=cv2.medianBlur(img,3)
    return img

def GaussianBlurfun(img):      #高斯滤波
    img=cv2.GaussianBlur(img,(5,5),0,0)
    return img


def blurfun(img):              #均值滤波
    img==cv2.blur(img,(5,5))
    return img


###############图像翻转####################################################
def flipfun(img):   #水平翻转
    img = cv2.flip(img,1)
    return img

def sxfun(img):     #上下翻转
    img = cv2.flip(img,0)
    return img

def RotateClockWise90(img):         #顺时针翻转
    trans_img = cv2.transpose(img)
    img = cv2.flip(trans_img, 1)
    return img

def RotateAntiClockWise90(img):         #逆时针翻转
    trans_img = cv2.transpose(img)
    img = cv2.flip(trans_img, 0)
    return img


##############轮廓检测####################################################
def morphologyExfun(img):
    img_gradient = cv2.Laplacian(img, cv2.CV_8U)
    return img_gradient


#############sift检测#######################################################
def sift_fun(img):
    sift = cv2.SIFT_create()
    kps = sift.detect(img)
    img_sift = cv2.drawKeypoints(img, kps, None, -1, cv2.DrawMatchesFlags_DEFAULT)
    return img_sift

##################################修复####
def xiufu(img):
    _, mask1 = cv2.threshold(img, 245, 255, cv2.THRESH_BINARY)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask1 = cv2.dilate(mask1, k)
    result1 = cv2.inpaint(img, mask1[:, :, -1], 5, cv2.INPAINT_NS)
    return result1

##############浮雕效果##########
def fudiao_fun(img):
    h, w, c = img.shape
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = np.zeros((h, w), dtype='uint8')
    gray2 = cv2.addWeighted(gray1, -1, img2, 0, 255, 0)
    gray2 = cv2.GaussianBlur(gray2, (25, 25), 0)
    dst = cv2.addWeighted(gray1, 0.5, gray2, 0.5, 0)
    return dst

###########水彩效果####
def shuicai_fun(img):
    res = cv2.stylization(img, sigma_s=60, sigma_r=0.6)
    return res

if __name__ == '__main__':
    img = cv2.imread("lena.jpg")
    cv2.imshow(' ',img)
    newimg=xiufu(img)
    cv2.imshow(' ',newimg)
    cv2.waitKey(0)

