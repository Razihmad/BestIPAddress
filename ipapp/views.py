from django.shortcuts import redirect, render
from .models import Allip, City,Bestip
import requests, json, string, random, datetime
from django.contrib import messages
import urllib.request


# It generate the random string which we use for the session id in generating new ip address
def get_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# This function first connect to the proxy then return the ip address of that proxy server
def get_ip(id,city):
    r = requests.get('https://utilities.tk/network/info').json()
    return r['ip'], r['timezone']



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
                        messages.info(request,"No more ip in this city ")
                        return redirect('home')
                        break
                else:
                    continue
            except requests.exceptions.ProxyError:
                continue
            except requests.exceptions.SSLError:
                continue
            except requests.exceptions.ConnectionError:
                messages.info(request,"Please change the city there is no possible connection IP")
                return redirect('home')
            except requests.exceptions.HTTPError:
                continue
            except urllib.error.URLError:
                messages.info(request,"Please change the city there is no possible connection IP")
                return redirect('home')
            if score['success'] == True:

                if score['fraud_score'] <= s:
                    city = score['city']
                    ip = ip
                    login_id = 'customer-Smdevops-cc-US-city-' + city + '-sesstime-20-sessid-' + session_id
                    password = ~
                    f_score = score['fraud_score']
                    d = Allip(ip = ip,score = score['fraud_score'],city = score['city'])
                    d.save()
                    if (ip,city,session_id,f_score) not in Bestip.objects.values_list('ip', 'city','session_id','score'):
                        data = Bestip(ip = ip,city = city,session_id = session_id,password = password,score = score['fraud_score'],login = login_id,timezone = timezone)
                        data.save()
                        return render(request, 'ip.html', {'ip':ip,'login':'customer-Smdevops-cc-US-city-' + city + '-sesstime-20-sessid-' + session_id})
                    
                        break
                    else:
                        messages.info(request,f"You already have this ip address with {f_score} score in your database !! ")
                        return redirect('home')
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
