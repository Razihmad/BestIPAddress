from django.shortcuts import redirect, render
from .models import Allip, City,Bestip
import requests
import json
import string
import random
import datetime
from django.contrib import messages
import urllib.request
import random


# It generate the random string which we use for the session id in generating new ip address
def get_random_string(length):

    s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return s


# This function first connect to the proxy then return the ip address of that proxy server
def get_ip(id,city):
    username = 'Smdevops'
    password = '123456'
    country = 'US'
    city = city
    # session = random.random()
    entry = ('http://customer-%s-cc-%s-city-%s-sessid-%s:%s@pr.oxylabs.io:7777' %
        (username, country, city, id, password))
    query = urllib.request.ProxyHandler({
        'http': entry,
        'https': entry,
    })
    execute = urllib.request.build_opener(query)
    data = execute.open('https://ipinfo.io').read()
    new_data = data.decode('utf-8')
    d = json.dumps(new_data)
    final_dictionary = json.loads(new_data) 
    return final_dictionary['ip'],final_dictionary['timezone']



# This function gives you the fraud_score of the ip address
def quality_score(ip):
    url = 'https://ipqualityscore.com/api/json/ip/4ZHhcIZms4aaj2ff95kMdfoHvbfxynVi/' + \
        ip + '?strictness=3&allow_public_access_points=true'
    score = requests.get(url='https://ipqualityscore.com/api/json/ip/4ZHhcIZms4aaj2ff95kMdfoHvbfxynVi/' +
                         ip+'?strictness=3&allow_public_access_points=true').json()
    return score
ses = []


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
                if session_id not in ses:
                    data = get_ip(id=session_id,city = city)
                    ip = data[0]
                    timezone = data[1]
                    score = quality_score(ip)
                    ses.append(session_id)
                    if (ip,city,score['fraud_score']) in Allip.objects.values_list('ip','city','score'):
                        messages.info("No more ip in this city ")
                        redirect('home')
                        break
                else:
                    continue
            except requests.exceptions.ProxyError:
                continue
            except requests.exceptions.SSLError:
                continue
            if score['success'] == True:

                if score['fraud_score'] <= s:
                    city = score['city']
                    ip = ip
                    login_id = 'customer-Smdevops-cc-US-city-' + city + '-sesstime-20-sessid-' + session_id
                    password = 123456
                    f_score = score['fraud_score']
                    d = Allip(ip = ip,score = score['fraud_score'],city = score['city'])
                    d.save()
                    if (ip,city,session_id,f_score) not in Bestip.objects.values_list('ip', 'city','session_id','score'):
                        data = Bestip(ip = ip,city = city,session_id = session_id,password = password,score = score['fraud_score'],login = login_id,timezone = timezone)
                        data.save()
                        return render(request, 'ip.html', {'ip':ip,'login':'customer-Smdevops-cc-US-city-' + city + '-sesstime-20-sessid-' + session_id})
                    
                        break
                    else:
                        messages.info(f"You already have this ip address with {f_score} score in your database !! ")
                        redirect('home')
                        break
                else:
                    d = Allip(ip = ip,score = score['fraud_score'],city = score['city'])
                    d.save()
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