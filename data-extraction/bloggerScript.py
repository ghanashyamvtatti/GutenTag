APIKEY = "AIzaSyCGcqTCiL-SBxkTqQxqR41zALDRwGj-E_k"
BASE  = "https://www.googleapis.com/blogger/v3"
import urllib3
from urllib.parse import urlencode
import json

def sendRequest(url,method,body):
    http= urllib3.PoolManager()
    method=method.upper()
    if method == "GET":
        try:
            response = http.request(method,url=url)
            return json.loads(response.data.decode('utf-8')), False
        except Exception as e:
            return e, True
    # elif method=="POST":
    #     encoded_data = urlencode({'arg': 'value'})
    #     response = http.request(method,url=url,body=encoded_data)

def getBlogID(blogURL = "https://blogger.googleblog.com"):
    url = "https://www.googleapis.com/blogger/v3/blogs/byurl?url="+str(blogURL)
    url += "&key="+str(APIKEY)
    response, err = sendRequest(url,"GET",None)
    if err:
        print("Error: ", response)
        return None
    #print("BlogID: ", response["id"])
    return response["id"]

def getPostList(blogID):
    url = "https://www.googleapis.com/blogger/v3/blogs/%s/posts"%str(blogID)
    url += "?key="+str(APIKEY)
    print(url)
    response, err = sendRequest(url,"GET",None)
    if err:
        print("Error: ", response)
        return None
    #print("BlogID: ", response["id"])
    return response


#blogID = getBlogID()
blogID = 2399953
response = getPostList(blogID)
print(response)

