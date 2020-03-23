import datetime
from django.shortcuts import render
from django.http import Http404, HttpResponse

HTML = """
<!DOCTTYPE html>
<html lang = "es">
<head>
<meta http-equiv = "content-type" content = "text/html; charset=utf-8">
<meta name="robots" content = "NONE,NOARCHIVE">
<title>Hola mundo</title>
<style type = "text/css">
html *{padding:0; margin:0;}
body *{padding:10px 20px;}
body * *{padding:0;}
body {font:small sans-serif;}
body>div{border-bottom:1px solid #ddd;}
h1 {font-wigth:normal;}
#summary {background: #e0ebff;}
</style>
</head>
<body>
<div id="summary">
<h1>Hola mundo</h1>
</div>
</body><html>"""

def hola(request):
    return HttpResponse(HTML)
def fecha_actual(request):
    ahora = datetime.datetime.now()
    return render(request,'fecha_actual.html',{'fecha_actual':ahora})
def horas_adelante(request,horas):
    try:
        horas = int(horas)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now()+datetime.timedelta(hours=horas)
    return render(request, 'horas_adelante.html',{'hora_siguiente':dt,'horas':horas})

def mostrar_navegador(request):
    try:
        ua = request.META['HTTP_USER_AGENT']
    except KeyError:
        ua = 'unkown'
    return HttpResponse("Tu navegador es %s" % ua)

def atributos_meta(request):
    valor = request.META.items()
    valor.sort()
    html =[]
    for k, v in valor:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k,v))
    return HttpResponse('<table>%s</table>'%'\n'.join(html))
