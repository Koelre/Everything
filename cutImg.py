#-*- coding:utf-8 -*-
# 把图片切割成九宫格

import os,sys,re
from PIL import Image
import filetype

reload(sys)
sys.setdefaultencoding('utf-8')


path = os.path.abspath(os.path.dirname(__file__))

class  CutImages(object):
    """docstring for  CutImages"""
    def __init__(self):
        self.mines = ['image/jpeg','image/jpg','image/png'] # 定义需要的文件类型
    #     pass
        
    def get_imlist(self):
        """返回目录中所有png图像的文件名列表"""                                                             #判断文件的类型是否是 需要的文件类型
        return [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(f) if filetype.guess(f) if filetype.guess(f).mime in mines ]
        

    #将图片填充为正方形
    def fill_image(self,image):
        width, height = image.size
        #选取长和宽中较大值作为新图片的
        new_image_length = width if width > height else height
        #生成新图片[白底]
        new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')
        #将之前的图粘贴在新图上，居中
        if width > height:#原图宽大于高，则填充图片的竖直维度
            #(x,y)二元组表示粘贴上图相对下图的起始位置
            new_image.paste(image, (0, int((new_image_length - height) / 2)))
        else:
            new_image.paste(image, (int((new_image_length - width) / 2),0))
        return new_image

    #切图
    def cut_image(self,image):
        width, height = image.size
        item_width = int(width / 3)
        box_list = []
        # (left, upper, right, lower)
        for i in range(0,3):#两重循环，生成9张图片基于原图的位置
            for j in range(0,3):
                box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
                box_list.append(box)

        image_list = [image.crop(box) for box in box_list]
        return image_list

    #保存
    def save_images(self,image_list):
        splitfile = os.path.join(path,self.filename)
        if not os.path.exists(splitfile):
            os.makedirs(splitfile)
        index = 1
        for image in image_list:
            image.save(splitfile + "\\" + str(index) + '.jpg')
            index += 1
        
    # 调整图片
    def readimg(self,image,file):
        r, g, b, a = image.split()
        im = Image.merge("RGB", (r, g, b))
        os.remove(file)
        im.save(file[:-4] + ".jpeg")
        file = file[:-4] + ".jpeg"
        image = Image.open(file)
        image = self.fill_image(image)
        image_list = self.cut_image(image)
        self.save_images(image_list)
        return file


    def mains(self):
        file_path = self.get_imlist()
        if len(file_path)>0:
            for file in file_path:
                print file
                self.filename = os.path.splitext(file)[0]

                image = Image.open(file)
                # image.show()
                image = self.fill_image(image)
                image_list = self.cut_image(image)
                try:
                    self.save_images(image_list)
                except Exception as e:
                    self.readimg(image,file)
   

if __name__ == '__main__':
    cuts = CutImages()
    cuts.mains()


