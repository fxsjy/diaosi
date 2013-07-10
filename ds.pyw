from Tkinter import *
import sdict
import os
import string
import tkFont
#import time

alphabets='abcdefghijklmnopqrstuvwxyz'

def current_file_directory():
            import os, sys, inspect
            path = os.path.realpath(sys.path[0])        # interpreter starter's path
            if os.path.isfile(path):                    # starter is excutable file
                path = os.path.dirname(path)
                return os.path.abspath(path)            # return excutable file's directory
            else:                                       # starter is python script
                caller_file = inspect.stack()[1][1]     # function caller's filename
                return os.path.abspath(os.path.dirname(caller_file))# return function caller's file's directory

def edits1(W): #set of words with edit-distance = 1 
    N = len(W)
    splits = [(W[:i],W[i:]) for i in xrange(N)]
    deletes = [ x+y[1:] for x,y in splits if y]
    trans = [a + b[1] + b[0] +b[2:] for a,b in splits if len(b)>1]
    replaces = [a + c + b[1:] for a,b in splits for c in alphabets if b]
    inserts =  [a + c + b for a,b in splits for c in alphabets]
    return set(deletes+trans+replaces+inserts)
    
_localDir=current_file_directory()

_curpath=os.path.normpath(os.path.join(os.getcwd(),_localDir))
        
dic_name = os.path.join(_curpath,"endict.txt")

#t1 =  time.time()

dic_list = []
for line in open(dic_name,"rb"):
    tup = line.rstrip().split('\t')
    en_word = tup[0]
    chn_word = tup[1:]
    low_word= en_word.lower()
    chn_word = ' '.join(chn_word)
    dic_list.append((en_word,chn_word))
    if en_word != low_word:
        dic_list.append((low_word+";"+en_word+";",chn_word))


index = sdict.Dict(dic_list)

#print "loading cost: ", time.time() -t1

def lookup_result(word):
    result = ""
    rel_words = index.prefix(word,limit=30)
    rel_words = [x if not x.endswith(';') else x.split(';')[1] for x in rel_words]
    result = ""
    if len(rel_words)==0:
        if " " in word: # due to more than one word
            return lookup_result(word.split(' ')[-1]) # use the last word
        else: # due to spelling error
            cor_words = edits1(word)
            result = "\n".join("? " +w for w in cor_words if w in index)
    else:
        result = "\n".join(w + ": "+index[w] for w in rel_words)
    return result

def on_press(event):
    global index,E1,T1
    word = E1.get().encode('utf-8')
    result = lookup_result(word)
    T1.delete(1.0,END)
    T1.insert(END,result)

def on_alt_d(event):
	global E1
	E1.focus_set()
	E1.select_range(0, END)

def on_esc(event):
	global E1
	E1.delete(0, END)

root = Tk()
root.title("Diaosi: A dictionary made by a diaosi, for the diaosi")
root.resizable(0,0)
try:
    root.wm_iconbitmap(os.path.normpath(os.path.join(os.getcwd(),_localDir,'icon')))
except:
    pass


frame1 = Frame(root,width=480,height=25)
frame1.pack_propagate(0)
frame1.pack()
frame2 = Frame(root,width=480,height=480)
frame2.pack_propagate(0)
frame2.pack()

L1 = Label(frame1,text=">>")
L1.pack(side=LEFT)
E1 = Entry(frame1,width=60,font=tkFont.Font(size=16,weight='bold'))
E1.pack(side=RIGHT,expand=True)
E1.focus_set()
T1 = Text(frame2,height=480)
T1.pack(expand=True)

E1.bind("<KeyRelease>",on_press)
root.bind("<Alt-d>",on_alt_d)
root.bind("<Escape>",on_esc)

if __name__ == "__main__":
    root.mainloop()
