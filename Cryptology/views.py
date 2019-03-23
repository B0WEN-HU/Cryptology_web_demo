from django.http import HttpResponse
from django.template import Template, Context
from django.shortcuts import render_to_response,HttpResponseRedirect
from PW_dict.models import DICT
import hashlib
import string
import random
import qrcode
from cStringIO import StringIO

def password2code(password):
    myMd5 = hashlib.md5()
    ADD = ''.join(random.sample(string.letters+string.digits,max(64-len(password),0)))
    myMd5.update(password+ADD)
    return myMd5.hexdigest()

def css(request):
    css = open('./Cryptology/bootstrap.min.css').read()
    return HttpResponse(css)

def theme(request):
    theme = open('./Cryptology/bootstrap-theme.min.css').read()
    return HttpResponse(theme)

def js(request):
    js = open('./Cryptology/bootstrap.min.js').read()
    return HttpResponse(js)

def home(request):
    return render_to_response('home.html')

def ENCRYPTION(request):
    if request.method == 'POST':

        password = request.POST.get('InputPassword',None)
        password = password.encode('utf-8') #####
        code = password2code(password)

        new = DICT(CODE=code,PASSWORD=password)
        new.save()
        if(password == 'sudo@hubowen reset()'):
            DICT.objects.all().delete()
            
        #return HttpResponseRedirect('/encryption/done')
        #LINK = '172.18.68.102:8000/code/TESTCODE'
        LINK = 'http://192.168.0.182:8000/code/'+code
        
        
        #return render_to_response('ENCRYPTION_DONE.html')
        return render_to_response('ENCRYPTION_DONE.html',{'CODE':code,'link':LINK})
    
    return render_to_response('ENCRYPTION.html')

def CODE(request,code):
    #t = Template('HERE  IS  YOUR  KEY: {{ key }} ')
    
    #MAP = {'hubowen':'Author','year':'2017'};
    #if MAP.has_key(code):
    #    temp_key = MAP[code]
       
    #else:
    #    temp_key = 'NULL';
    #c = Context({'key':temp_key})
    try:
        temp_map = DICT.objects.get(CODE=code)
    except:
        return render_to_response('ERROR.html')
    else:
        temp_password = temp_map.PASSWORD
        #temp_password = unicode(temp_map.PASSWORD,encoding='utf-8')
        temp_map.delete()
        return render_to_response('CODE.html',{'key':temp_password})

def QRcode(request,LINK):
    #print LINK
    img = qrcode.make(LINK)

    buf = StringIO()
    img.save(buf)
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream,content_type='image/png')
    response['Cache-Control'] = 'max-age=3600'
    return response


    
