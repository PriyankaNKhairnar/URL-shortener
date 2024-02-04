from django.shortcuts import render,redirect,get_object_or_404
from django.shortcuts import HttpResponse
from .models import LongToShort
from ip2geotools.databases.noncommercial import DbIpCity

def hello_world(request):
    return HttpResponse("Hello World!")

def home_page(request):
    form={
        "submitted":False,
        "error":False
        }

    if request.method =='POST':
        long_url=request.POST['longurl']
        short_url=request.POST['custom_name']
        
        try:
        
            obj=LongToShort(long_url=long_url, short_url=short_url,
                country="",country_count="", clicks=0, dclicks=0, mclicks=0)
            obj.save()

            date=obj.date
            clicks=obj.clicks

            form["long_url"]=long_url
            form["short_url"]=request.build_absolute_uri()+short_url
            form["date"]=date
            form["clicks"]=clicks
            form["submitted"]=True
        except:
            form['error']=True
    return render(request,'index.html',form)

def redirect_url(request,short_url):
    row=LongToShort.objects.filter(short_url=short_url)
    if len(row) == 0:
        return HttpResponse("No such short url here")
    obj=row[0]
    long_url=obj.long_url


    obj.clicks=obj.clicks+1
    obj.save()
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

    if 'mobile' in user_agent:
        obj.mclicks = obj.mclicks+1
        obj.save()
    else:
        obj.dclicks=obj.dclicks+1
        obj.save()

    ip = get_client_ip(request)
    response = DbIpCity.get(ip, api_key='free')

    
    country = obj.country
    country_count = obj.country_count

    country_list = str(country).split(',') if country else []
    country_count_list = str(country_count).split(',') if country_count else []

    if response.country in country_list:
        index = country_list.index(response.country)
        country_count_list[index] = str(int(country_count_list[index]) + 1)
    else:
        country_list.append(response.country)
        country_count_list.append('1')

    obj.country = ','.join(country_list)
    obj.country_count = ','.join(country_count_list)
    obj.save()
        


    return redirect(long_url)



def all_analytics(request):

    row=LongToShort.objects.all()

    context={
        "row":row
        }
    return render(request,"all-analytics.html",context)

def analytics(request, id):
    pk= int(id)

    item_row = get_object_or_404(LongToShort, pk=pk)


    countries = str(item_row.country).split(',') if item_row.country else []
    country_counts = str(item_row.country_count).split(',') if item_row.country_count else []
    
    country_counts = [int(i) for i in country_counts]


    context = {"item_row": item_row, "countries":countries, "country_counts":country_counts}
    return render(request,'analytics.html', context)

            # Testing the geo-agent function
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location(request):
    response = DbIpCity.get(get_client_ip(request), api_key='free')
    return HttpResponse('Request was made from: ' + response.country)
   