from io import BytesIO
from tkinter import Image
import wolframalpha
import requests
from IPython import display
from PIL import Image

def nutrients(food): 
    food=food+"nutritional info"
    app_id="RLWKY9-EUT258WJ5X"
    client=wolframalpha.Client(app_id)
    res=client.query(food)
    url=res.pod[1].subpod.img.src
    # print(url)
    response=requests.get(url)
    img=Image.open(BytesIO(response.content))
    # print(res)
    ans=next(res.results).text
    li = list(ans.split(" "))
    print(li)
    
    dict={}
    i = 0
    li2=[]
    length = len(li)
    li2=li[10:]
    s='fat'
    while i < length:
        if s == li2[i]:
            break
        i=i+1
    print(s)
    print(li2[i+1])
    print(li2[i+2])
    if li2[i+2]=='g':
        dict[s]=int(li2[i+1])*1000
    elif li[i+2]=='μg':
        dict[s]=int(li2[i+1])/1000
    else:
        dict[s]=int(li2[i+1])


    print(dict)
    i = 0
    length = len(li)
    # li=li[20:]
    s='carbohydrates'
    while i < length:
        if s == li[i]:
            break
        i=i+1
    print(s)
    print(li[i+1])
    print(li[i+2])
    if li[i+2]=='g':
        dict[s]=int(li[i+1])*1000
    elif li[i+2]=='μg':
        dict[s]=int(li[i+1])/1000
    else:
        dict[s]=int(li[i+1])

    i = 0
    length = len(li)
    # li=li[0:]
    s='cholesterol'
    while i < length:
        if s == li[i]:
            break
        i=i+1
    print(s)
    print(li[i+1])
    print(li[i+2])
    if li[i+2]=='g':
        dict[s]=int(li[i+1])*1000
    elif li[i+2]=='μg':
        dict[s]=int(li[i+1])/1000
    else:
        dict[s]=int(li[i+1])

    i = 0
    length = len(li)
    li=li[10:]
    s='protein'
    while i < length:
        if s == li[i]:
            break
        i=i+1
    print(s)
    print(li[i+1])
    print(li[i+2])
    if li[i+2]=='g':
        dict[s]=int(li[i+1])*1000
    elif li[i+2]=='μg':
        dict[s]=int(li[i+1])/1000
    else:
        dict[s]=int(li[i+1])

    i = 0
    length = len(li)
    # li=li[10:]
    s='sodium'
    while i < length:
        if s == li[i]:
            break
        i=i+1
    print(s)
    print(li[i+1])
    print(li[i+2])
    if li[i+2]=='g':
        dict[s]=int(li[i+1])*1000
    elif li[i+2]=='μg':
        dict[s]=int(li[i+1])/1000
    else:
        dict[s]=int(li[i+1])
    # print(type(ans))
    print(dict)
    return [dict, url]

    # Image(url)
    # print(img)
    # return Image(url)
    # next(ans)
    
nutrients("apple")