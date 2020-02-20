#!/usr/bin/env python 
# encoding: utf-8 

"""
@version: v1.0
@author: XF
@site: https://www.cnblogs.com/c-x-a
@software: PyCharm
@file: GIF_Synthesis.py
@time: 2020/2/19 22:43
"""
# ---------------------------------------------------------------------------------- 
# 读取文件夹下的所有图片并制作成gif动图
# ---------------------------------------------------------------------------------- 
import os
import imageio
# ----------------------------------------------------------------------------------
path= os.getcwd()
filenames=[]
for files in os.listdir(path):
    if files.endswith('jpg') or files.endswith('jpeg') or files.endswith('png'):
    	file=os.path.join(path,files)
    	filenames.append(file)
# ----------------------------------------------------------------------------------
images=[]
for filename in filenames:
	images.append(imageio.imread(filename))
imageio.mimsave('my.gif',images,duration=0.1)
# ---------------------------------------------------------------------------------- 