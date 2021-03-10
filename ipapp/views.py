from django.shortcuts import redirect, render
from .models import City,Bestip
import requests
import json
import string
import random
import datetime
from django.contrib import messages


# It generate the random string which we use for the session id in generating new ip address
def get_random_string(length):

    s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return s


# This function first connect  to the proxy first then return the ip address of that proxy server
def get_ip(id):
    proxies = {
        'http': 'http://sudhanshumewati:UFgPvV3Tbv806WeC_country-UnitedStates_session-' + id + '@proxy.packetstream.io:31112',
        'https': 'http://sudhanshumewati:UFgPvV3Tbv806WeC_country-UnitedStates_session-' + id + '@proxy.packetstream.io:31112'
    }
    res = requests.get('https://ipinfo.io', proxies=proxies)
    data = res.json()
    ip = data['ip']
    return ip


# This function gives you the fraud_score of the ip address
def quality_score(ip):
    url = 'https://ipqualityscore.com/api/json/ip/4ZHhcIZms4aaj2ff95kMdfoHvbfxynVi/' + \
        ip + '?strictness=1&allow_public_access_points=true'
    score = requests.get(url='https://ipqualityscore.com/api/json/ip/4ZHhcIZms4aaj2ff95kMdfoHvbfxynVi/' +
                         ip+'?strictness=1&allow_public_access_points=true').json()
    return score

# Views for this project  
def home(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        s = request.POST.get('fraud_s')
        s = int(s)

        while True:
            n = random.randint(1, 8)
            session_id = get_random_string(n)
            try:

                ip = get_ip(id=session_id)
                score = quality_score(ip)
            except requests.exceptions.ProxyError:
                continue
            except requests.exceptions.SSLError:
                continue
            if score['success'] == True:

                if score['fraud_score'] <= s:
                    city = score['city']
                    ip = ip
                    login = 'customer-hk2020-cc-US-city-' + score['city'] + '-sesstime-20-sessid-'+session_id
                    password = 123456
                    data = Bestip(ip = ip,city = city,login = login,session_id = session_id,password = password,score = score['fraud_score'])
                    data.save()
                    return render(request, 'ip.html', {'ip':ip,'login':'customer-hk2020-cc-US-city-' + score['city'] + '-sesstime-20-sessid-'+session_id})
                    break
                else:
                    continue
            else:
                return render(request,'error.html',{'messages':score['message']})

                break    
    return render(request,'home.html',{'cities':City.objects.all,'ips':Bestip.objects.all})
    
def addcity(request):
    if request.method == 'POST':
        city_name =  request.POST.get('city_name')
        city_name = city_name.capitalize()
        city = City(name = city_name)
        city.save()
        messages.success(request,"City Has Been Added Successfully")
        return redirect('home')
    return render(request,'addcity.html',{'cities':City.objects.all})