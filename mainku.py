#!/usr/bin/env python
from bottle import *
try:
    from google.appengine.ext import webapp
    from google.appengine.ext.webapp import util
    isGAE = True
except:
    isGAE = False
    pass
import os


from hmmtagger import MainTagger
from tokenization import *
from myner import *
from mypostag import *

mt = None

@route('favicon.ico')
def favicon():
    return static_file('favicon.ico', root='static/')

@route('/')
@view('antarmukates')
def index():
    return { 'apptitle':'skripsi', 'root':request.environ.get('SCRIPT_NAME') }
    
@post('/handler')
def default_handler():
    task = request.forms.get('task', '')
    if task=='postag':
        return do_tag()
    elif task=='ner':
        return do_ner()    
    response.content_type = 'text/plain'
    return "NotImplemented"


@route('/tag')
@route('sentence_tagging')
def postag():
    return { 'apptitle':'skripsi', 'root':request.environ.get('SCRIPT_NAME') }

def init_tag():
    global mt
    if mt is None:
        mt = MainTagger("resource/Lexicon.trn", "resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)
    
@post('/tag')
def do_tag():
    response.content_type = 'text/plain'
    lines = request.forms.get('teks', '').strip().split("\n")
    result = []
    try:
        init_tag()
        for l in lines:
            if len(l) == 0: continue
            out = sentence_extraction(cleaning(l))
            for o in out:
                strtag = " ".join(tokenisasi_kalimat(o)).strip()
                result += [" ".join(mt.taggingStr(strtag))]
    except:
        return "Error Exception"
    return "\n".join(result)

@post('/ner')
def do_ner():
    response.content_type = 'text/plain'
    lines = request.forms.get('teks', '').strip().split("\n")
    mt = MainTagger("resource/Lexicon.trn", "resource/Ngram.trn", 0, 3, 3, 0, 0, False, 0.2, 0, 500.0, 1)
    b =  entitas()
    tagging = []
    ner = []
    hasil =[]
    try:
        for l in lines:
            if len(l) == 0: continue
            out = sentence_extraction(cleaning(l))
            for o in out:
                strtag = " ".join(tokenisasi_kalimat(o)).strip()
                tagging = mt.taggingStr1(strtag) 
                milih = b.pilih(tagging)
                tanggal = b.tanggal()
                date = b.tanggall()
                rule = b.aturan()
                ner = b.akhir()
                hasil += ["".join(ner)]
      
    except:
        return "exception"
    return " ".join(hasil)
        
    
@route('/static/:fname#.+#')
def servestatic(fname):
    return static_file(fname, root='static/')

def main():
    if isGAE:
        util.run_wsgi_app(default_app())
    else:
        init_tag()
        run(port=8080, reloader=True)

if __name__ == '__main__':
    main()
