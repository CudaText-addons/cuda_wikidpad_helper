import os
import string
from cudatext import *

def is_camel_case(s):

    if len(s)<3:
        return False
    if not s[0].isupper():
        return False
    for i in range(len(s)-1):
        if s[i].isupper() and s[i+1].islower():
            return True
    for ch in s[2:]:
        if ch.isupper():
            return True
    return False


class Command:

    def on_click_dbl(self, ed_self, state):
        fn = ed.get_filename()
        if not fn: return msg_status('Need named file-tab')
        dir = os.path.dirname(fn)

        carets = ed.get_carets()
        if len(carets)!=1: return msg_status('Need single caret')
        x, y, x1, y1 = carets[0]
        if y>=ed.get_line_count(): return msg_status('Bad caret pos')
        line = ed.get_text_line(y)
        if x>=len(line): return msg_status('Click after line end')

        ch = line[x]
        if not ch.isalnum(): return msg_status('Click not on a word-char')
        x1 = x
        x2 = x
        while x1>0 and line[x1-1].isalnum(): x1-=1
        while x2<len(line)-1 and line[x2+1].isalnum(): x2+=1

        if x1>0 and line[x1-1]=='\\': return msg_status('Click on escaped word')

        word = line[x1:x2+1]
        #print('word "'+word+'"')

        if not is_camel_case(word):
            return msg_status('Click on non-CamelCase word')

        fn = os.path.join(dir, word+'.wiki')
        if not os.path.isfile(fn):
            res = msg_box('File is not found:\n'+fn+'\n\nCreate it?', MB_OKCANCEL+MB_ICONWARNING)
            if res==ID_CANCEL: return
            with open(fn, 'w') as f:
                f.write('\n')

        file_open(fn)
        ed.set_prop(PROP_LEXER_FILE, 'WikidPad')
        return False
