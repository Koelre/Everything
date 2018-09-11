＃ -  *  - 编码：utf-8  -  *  -

＃文件名称：Screenshot_stitching.py
＃作者：lixue
＃创建日期：2017-08-17

import sys，os
进口重新
进口时间
导入 sjzBus
导入 glob
来自 PIL  导入图片
来自 selenium import webdriver
来自 selenium.webdriver.common.keys 导入密钥
来自 selenium.webdriver.common.action_chains 导入 ActionChains

＃设置编码格式
＃ a，b，c = sys.stdin，sys.stdout，sys.stderr
重载（sys）
sys.setdefaultencoding（' utf-8 '）
＃ sys.stdin，sys.stdout，sys.stderr = a，b，c

“””
功能：写入日志日志
@info：写入日志信息
“””
def  日志（信息）：
    用 open（' simg.log '，' ab '）作为 f：
        n = os.linesep
        f.write（info + n）


“””
功能：获取当前文件的绝对路径
“””
def  abspaths（）：
    filename = sys.argv [ 0 ]  
    dirname = os.path.dirname（filename）  
    abspath = os.path.abspath（dirname）
    返回 abspath

“””
功能：在当前目录下创建保存截图的文件夹
“””
def  creatPath（bus_name）：
    ＃获取当前文件的绝对路径
    abspath = abspaths（）
    imgpath = abspath + ' \\ img \\ ' + str（bus_name）+ ' \\ ' ＃ img路径
    如果 不是 os.path.exists（imgpath）：
        os.makedirs（imgpath）
    返回 imgpath

“””
功能：更改所有截图的像素
“””
def  convertjpg（jpgfile，outdir，width = 1184，height = 768）：
    img = Image.open（jpgfile）   
    new_img = img.resize（（宽度，高度），图像。双线性）
    new_img.save（os.path.join（OUTDIR，os.path.basename（JPG文件）））

“””
功能：把所有截图都拼接在一起然后保存
@bus_name：公交名称
“””
def  pilimages（bus_name）：
    ＃获取当前文件的绝对路径
    abspath = abspaths（）
    imgpath = abspath + ' \\ img \\ ' +  str（bus_name）+ ' \\ ' ＃ img路径
    打印 imgpath
    ＃更改所有截图的像素
    对于 glob.glob 中的 jpgfile（imgpath + ' * .png '）：
        convertjpg（JPG文件，imgpath）
    high_size =  768 ＃高
    width_size =  1184 ＃宽
    imghigh =  sum（[ len（x）for _，_，x in os.walk（os.path.dirname（imgpath））]）＃获取当前文件路径下的文件个数
    打印 你的图片个数：'，imghigh
    尝试：
        如果 str（imghigh）== ' 3 '：
            imagefile = []
            为根，显示目录，文件在 os.walk（imgpath）：
                对于 ˚F 的文件：
                    imagefile.append（Image.open（imgpath + f））
            target = Image.new（' RGB '，（width_size，high_size * 3））＃最终拼接的图像的大小
            左=  0
            right = high_size
            napath =  ' D：\\ sjzimgs \\ '
            打印 ' napath：'，napath
            如果 不是 os.path.exists（napath）：
                os.makedirs（napath）
            picname =  str（int（time.time（））* 100）
            对于图像的镜像文件：
                target.paste（image，（0，left，width_size，right））
                left + = high_size ＃从上往下拼接，左上角的纵坐标递增
                right + = high_size ＃左下角的纵坐标也递增
                target.save（napath + STR（bus_name）+ picname + ' -result.jpg '，质量= 100）＃质量来指定生成图片的质量，范围是0〜100
           
            print imghigh，u '张图片已拼接'
            time.sleep（3）
    除 例外 为 E：
        打印 è
        dt = time.strftime（“％H：％M：％S ”）
        日志（u ' ％s pilimages：％s '％（str（dt），str（e）））
    
    ＃拼完然后就删除
    为根，显示目录，文件在 os.walk（imgpath）：
        对于名称的文件：
            如果 name.endswith（ “ png格式”）：
                os.remove（os.path.join（root，name））

“””
功能：打开网页，截图，然后拼接
@url：网址
@bus_name：公交名称
“””
def  openweb（url，bus_name）：
    driver = webdriver.Chrome（）
    driver.set_window_size（1200，900）＃设置窗口高宽度
    尝试：
        driver.get（URL）
    除 例外 为 E：
        driver.close（）
        driver.quit（）
        openweb（URL）
    driver.implicitly_wait（1）

    尝试：
        ＃时间戳
        pa =  str（int（time.time（））* 1000）
        ＃创建文件路径
        imgpath = creatPath（bus_name）
        js =  ' var q = document.documentElement.scrollTop = 50 '
        driver.execute_script（JS）
        time.sleep（1）
        pngname = imgpath + str（bus_name）+ str（pa）+ ' - 01.png '
        driver.save_screenshot（pngname）
        js =  ' var q = document.documentElement.scrollTop = 850 '
        driver.execute_script（JS）
        time.sleep（1）
        pngname = imgpath + str（bus_name）+ str（pa）+ ' - 02.png '
        driver.save_screenshot（pngname）
        js =  ' var q = document.documentElement.scrollTop = 1750 '
        driver.execute_script（JS）
        time.sleep（1）
        pngname = imgpath + str（bus_name）+ str（pa）+ ' - 03.png '
        driver.save_screenshot（pngname）
        time.sleep（1）

    除 例外 为 E：
        打印 è
        dt = time.strftime（“％H：％M：％S ”）
        日志（u ' ％s   ％s下滑截图失败'％（str（dt），bus_name））
    driver.close（）
    driver.quit（）
    pilimages（bus_name）
    

def  main（）：
    buslist = sjzBus.selnames（）＃查询线路类型名称url
    对于 BS 在 buslist：
        print bs [ 0 ]，bs [ 1 ]，bs [ 2 ]
        busname = bs [ 1 ] .decode（' UTF-8 '）。encode（' GBK '）
        openweb（bs [ 2 ]，busname）
        time.sleep（2）
