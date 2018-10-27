#By Azhy Slemany in 12/10/2018
#An example for using EasyFileChooser
#Which runs any chosen media file

from EasyFileChooser import csMain
import os

def func(result, args):
    os.system('start "" "'+result+'"')

if(__name__=='__main__'):
    csMain(func, filter_='mp4|mpeg|mov|avi|wmv|webm|'+'tiff|bmp|jpeg|jpg|png|gif')
