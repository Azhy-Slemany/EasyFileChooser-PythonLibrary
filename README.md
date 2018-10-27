# EasyFileChooser-PythonLibrary

A python module or library that you can choose or open a file easily from your windows system storage by using my custom style.

### This method provides two ways to choose files for your python programs:-

1. By using a `tkinter.Tk` object, it means you have created a `tkinter` window and passed the main `tkinter.Tk` object into this module's function which is `EasyFileChooser.tkMain`.
  
2. By creating a new `tkinter.Tk` object just for the dialog and after you chose the file the tkinter window(dialog) will be distroyed which used by `EasyFileChooser.csMain`.
  
## How to use this module:

- ##### If you created a console program and you don't use `tkinter` window or any other GUI Python Frameworks so you should use the `EasyFileChooser.csMain(resultFunc, args = None, filter_ = None)` function which parameters are:-
  - **resultFunc** : a defined function to handle the dialog's result, which should have a first parameter for the chosen file path and you can pass some other parameters in a tuple in the second parameter positions for using them in the function.
  - **args** : the arguments in a tuple to use them in the `resultFunc` function.
  - **filter_** : a file filter for filtering the shown files in the dialog, for example : `mp4|mpeg|mov|avi|wmv|webm`.
- ##### But if you created a `tkinter` window and you want to add this file chooser dialog to your program so you should use `EasyFileChooser.tkMain(master, resultFunc, args = None, filter_ = None)` function which parameters are:-
  - **master** : the main `tkinter.Tk` object that the python program uses.
  - **resultFunc** : a defined function to handle the dialog's result, which should have a first parameter for the chosen file path and you can pass some other parameters in a tuple in the second parameter positions for using them in the function.
  - **args** : the arguments in a tuple to use them in the `resultFunc` function.
  - **filter_** : a file filter for filtering the shown files in the dialog, for example : `mp4|mpeg|mov|avi|wmv|webm`.
  
## Some notes about the dialog:

- The folders in the dialog can be easily opened by one click (not double click), and also the file can be chosen by one click like the folders.
- There are some Key Shortcuts which can be used during choosing the file, which are:-
  - **Home** : to return back to to drives.
  - **Backspace** : to return back to the parent folder.
  - **Escape** to exit the dialog with result of `Nothing`.
- If the user closed the dialog anyway so the `result` parameter or the first parameter of your listener function which described as chosen file path will resturn `Nothing`.

## An Example:

```
#By Azhy Slemany in 12/10/2018
#An example for using EasyFileChooser
#Which runs any chosen media file

from EasyFileChooser import csMain
import os

def func(result, args):
    os.system('start "" "'+result+'"')

if(__name__=='__main__'):
    csMain(func, filter_='mp4|mpeg|mov|avi|wmv|webm|'+'tiff|bmp|jpeg|jpg|png|gif')
```
