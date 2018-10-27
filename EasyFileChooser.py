#Easy File Chooser
#Created by Azhy Slemany in 10/10/2018
#COPYRIGHT Protected

import tkinter as tk
import os

title = "Easy File Chooser"
size = '421x464'
colors = {'grey':'#444', 'blue':'#6871f7'}
fonts = {'button':('Cambria', 14), 'listbox':('Consolas', 11)}
lb_width = 50
lb_height = 20

maxLen = 45
backChar = '\u2ba2'

def getDrives():
    import string
    from ctypes import windll

    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return list(map(lambda x: x+':', drives))

class Window(tk.Frame):

    def __init__(self, master, resultFunc, args, filter_):
        self.root = master
        self.resultFunc = resultFunc
        self.args = args
        self.filter_ = filter_
        self.initializeWidgets()
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root.bind('<KeyPress>', self.KeyPressed)

    def initializeWidgets(self):
        self.pathLabel = tk.Label(self.root, font=fonts['listbox'])
        self.pathLabel['fg'] = colors['grey']
        self.pathLabel.grid()
        
        self.fileList = tk.Listbox(self.root, width=lb_width, height=lb_height)
        self.fileList['font'] = fonts['listbox']
        self.fileList['fg'] = colors['grey']
        self.fileList.bind('<<ListboxSelect>>', self.ListboxClicked)
        self.fileList.grid(row=1)
        self.parentFolder = None
        self.drives = getDrives()
        for i in self.drives:
            self.fileList.insert('end', i)

        scrollbar = tk.Scrollbar(self.root, orient='vertical')
        scrollbar['command'] = self.fileList.yview
        self.fileList['yscrollcommand'] = scrollbar.set
        scrollbar.grid(row=1, column=1, sticky='ns')

        scrollbar = tk.Scrollbar(self.root, orient='horizontal')
        scrollbar['command'] = self.fileList.xview
        self.fileList['xscrollcommand'] = scrollbar.set
        scrollbar.grid(row=2, sticky='we')
        
        self.cancelButton = tk.Button(self.root, text="Cancel")
        self.cancelButton['font'] = fonts['button']
        self.cancelButton['command'] = self.onClose
        self.cancelButton.grid(row=3,columnspan=2, sticky='we')

    def KeyPressed(self, event):
        key = event.keysym
        if key == 'BackSpace':
            self.ReturnBack()
        elif key == 'Escape':
            self.onClose()
        elif key == 'Home':
            self.pathLabel['text'] = ''
            self.fileList.delete(0, 'end')
            self.parentFolder = None
            for i in self.drives:
                self.fileList.insert('end', i)

    def ListboxClicked(self, event):
        selectedIndex = int(self.fileList.curselection()[0])
        selectedItem = self.fileList.get(selectedIndex)

        if selectedItem == backChar:
            self.ReturnBack()
            return
        
        if self.parentFolder == None:
            self.parentFolder = selectedItem + os.sep
        else:
            pf = self.parentFolder + os.sep
            self.parentFolder = os.path.join(pf, selectedItem)
            if(os.path.isfile(self.parentFolder)):
                self.resultFunc(self.parentFolder, self.args)
                self.root.destroy()
                return

        self.pathLabel['text'] = self.fixedParentPath()
        self.fileList.delete(0, 'end')
        self.fileList.insert('end', backChar)
        childList = os.listdir(self.parentFolder+'/')
        for item in childList:
            i = self.fileList.size() - 1
            if(self.filter_ == None):
                self.fileList.insert('end', item)
                if(os.path.isfile(os.path.join(self.parentFolder, item))):
                    self.fileList.itemconfig(i+1, {'fg':colors['blue']})
            else:
                ext = os.path.splitext(item)[1][1:].lower()
                allExt = list(map(str.lower, self.filter_.split('|')))
                if(os.path.isfile(os.path.join(self.parentFolder, item))):
                    if(ext in allExt):
                        self.fileList.insert('end', item)
                        self.fileList.itemconfig(i+1, {'fg':colors['blue']})
                else:
                    self.fileList.insert('end', item)

    def ReturnBack(self):
        if self.parentFolder == None:
            return
        
        if self.parentFolder.endswith('\\') or self.parentFolder.endswith('/'):
            self.parentFolder = os.path.splitdrive(self.parentFolder)[0]
        
        if self.parentFolder in self.drives:
            self.parentFolder = None
            self.fileList.delete(0, 'end')
            for i in self.drives:
                self.fileList.insert('end', i)
        elif self.parentFolder != None:
            pardir = os.path.join(self.parentFolder, os.pardir)
            self.parentFolder = os.path.abspath(pardir)
            self.fileList.delete(0, 'end')
            self.fileList.insert('end', backChar)
            childList = os.listdir(self.parentFolder+'/')
            for item in childList:
                i = self.fileList.size() - 1
                if(self.filter_ == None):
                    self.fileList.insert('end', item)
                    if(os.path.isfile(os.path.join(self.parentFolder, item))):
                        self.fileList.itemconfig(i+1, {'fg':colors['blue']})
                else:
                    ext = os.path.splitext(item)[1][1:].lower()
                    allExt = list(map(str.lower, self.filter_.split('|')))
                    if(os.path.isfile(os.path.join(self.parentFolder, item))):
                        if(ext in allExt):
                            self.fileList.insert('end', item)
                            self.fileList.itemconfig(i+1, {'fg':colors['blue']})
                    else:
                        self.fileList.insert('end', item)

        if self.parentFolder == None:
            self.pathLabel['text'] = ''
        else:
            self.pathLabel['text'] = self.fixedParentPath()

    def fixedParentPath(self):
        pf = self.parentFolder
        if(len(pf) < maxLen):
            return pf
        else:
            result = []
            pf = os.path.normpath(pf)
            folders = pf.split(os.sep)
            folders.reverse()
            for i in folders:
                if(len(i) > maxLen):
                    result.append(os.sep+i[0:40]+'...'+os.sep)
                    return result.reverse();

    def onClose(self):
        try:
            self.resultFunc(None, self.args)
            self.root.destroy()
        except:
            self.root.destroy()

def tkMain(master, resultFunc, args = None, filter_ = None):
    """Shows a dialog to choose a file from the computer using (Tk), arguments:-
    master : tkinter.Tk object
    resultFunc : choosing listener
    args : other args of your listener function
    filter_ : shown files filter, for e.g.:- exe|jar|py"""
    root = tk.Toplevel(master)
    root.title(title)
    root.geometry(size)
    root.resizable(0,0)
    window = Window(root, resultFunc, args, filter_)

def csMain(resultFunc, args = None, filter_ = None):
    """Shows a dialog to choose a file from the computer in console, arguments:-
    resultFunc : choosing listener
    args : other args of your listener function
    filter_ : shown files filter, for e.g.:- exe|jar|py"""
    root = tk.Tk()
    root.title(title)
    root.geometry(size)
    root.resizable(0,0)
    window = Window(root, resultFunc, args, filter_)
    window.root.mainloop()
