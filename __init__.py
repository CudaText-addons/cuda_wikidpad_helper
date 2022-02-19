import os
import string
from cudatext import *

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
        if not ch.isalpha(): return msg_status('Click not on a word-char')
        x1 = x
        x2 = x
        while x1>0 and line[x1-1].isalpha(): x1-=1
        while x2<len(line)-1 and line[x2+1].isalpha(): x2+=1
        
        word = line[x1:x2+1]
        #print('word "'+word+'"')
        if not (word[0].isupper() and word[1].islower()):
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