from django.shortcuts import render
import requests
# Create your views here.


def req(request):
    response = requests.get('https://api.github.com/events')
    print(response.content)  # 字节
    response.encoding = 'utf-8'
    print(response.text)
    return render(request, 'req.html', {'result': response.text})
