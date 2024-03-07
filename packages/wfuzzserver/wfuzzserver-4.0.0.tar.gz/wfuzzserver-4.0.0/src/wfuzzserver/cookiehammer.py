from queue import PriorityQueue
from queue import Queue
from threading import Thread
import time
import json
import requests
import random
import string
from urllib.parse import urlparse
from dicttoxml import dicttoxml
import xmltodict
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

requests.packages.urllib3.disable_warnings()
normalval="discobiscuits"
badval="discobiscuits'!@#$%^&*)(?><\",\\n\\r嘍嘊'!@#$%^&*)(?><\","
def narrower(request, factors, param_groups):
    """
    takes a list of parameters and narrows it down to parameters that cause anomalies
    returns list
    """
    anomalous_params = []
    threadpool = ThreadPoolExecutor(max_workers=mem.var['threads'])
    futures = (threadpool.submit(bruter, request, factors, params) for params in param_groups)
    for i, result in enumerate(as_completed(futures)):
        if result.result():
            anomalous_params.extend(slicer(result.result()))
        if mem.var['kill']:
            return anomalous_params
        print('%s Processing chunks: %i/%-6i' % (info, i + 1, len(param_groups)), end='\r')
    return anomalous_params
    
def bruter(request, factors, params, mode='bruteforce'):
    """
    returns anomaly detection result for a chunk of parameters
    returns list
    """
    if mem.var['kill']:
        return []
    response = requester(request, params)
    #conclusion = error_handler(response, factors)
    #if conclusion == 'retry':
    #    return bruter(request, factors, params, mode=mode)
    #elif conclusion == 'kill':
    #    mem.var['kill'] = True
    #    return []
    comparison_result = compare(response, factors, params)
    if mode == 'verify':
        return comparison_result[0]
    return comparison_result[1]
def get_params(include):
    """
    loads parameters from JSON/query string
    returns parameter dict
    """
    params = {}
    if include:
        if include.startswith('{'):
            try:
                params = json.loads(str(include).replace('\'', '"'))
                if type(params) != dict:
                    return {}
                return params
            except json.decoder.JSONDecodeError:
                return {}
        else:
            cleaned = include.split('?')[-1]
            parts = cleaned.split('&')
            for part in parts:
                each = part.split('=')
                try:
                    params[each[0]] = each[1]
                except IndexError:
                    params = {}
    return params

def create_query_string(params):
    """
    creates a query string from a list of parameters
    returns str
    """
    query_string = ''
    for param in params:
        pair = param + '=' + random_str(4) + '&'
        query_string += pair
    if query_string.endswith('&'):
	    query_string = query_string[:-1]
    return '?' + query_string
    
def requester(request, payload={}):
    """
    central function for making http requests
    returns str on error otherwise response object of requests library
    """
    if len(request.get('include', '')) != 0:
        payload.update(request['include'])
    if mem.var['stable']:
        mem.var['delay'] = random.choice(range(3, 10))
    time.sleep(mem.var['delay'])
    url = request['url']
    if mem.var['kill']:
        return 'killed'
    try:
        if request['method'] == 'GET':
            response = requests.get(url,
                params=payload,
                headers=request['headers'],
                verify=False,
                allow_redirects=False,
                timeout=mem.var['timeout'],
            )
        elif request['method'] == 'JSON':
            request['headers']['Content-Type'] = 'application/json'
            if mem.var['include'] and '$arjun$' in mem.var['include']:
                payload = mem.var['include'].replace('$arjun$',
                    json.dumps(payload).rstrip('}').lstrip('{'))
                response = requests.post(url,
                    data=payload,
                    headers=request['headers'],
                    verify=False,
                    allow_redirects=False,
                    timeout=mem.var['timeout'],
                )
            else:
                response = requests.post(url,
                    json=payload,
                    headers=request['headers'],
                    verify=False,
                    allow_redirects=False,
                    timeout=mem.var['timeout'],
                )
        elif request['method'] == 'XML':
            request['headers']['Content-Type'] = 'application/xml'
            payload = mem.var['include'].replace('$arjun$',
                dict_to_xml(payload))
            response = requests.post(url,
                data=payload,
                headers=request['headers'],
                verify=False,
                allow_redirects=False,
                timeout=mem.var['timeout'],
            )
        else:
            response = requests.post(url,
                data=payload,
                headers=request['headers'],
                verify=False,
                allow_redirects=False,
                timeout=mem.var['timeout'],
            )
        return response
    except Exception as e:
        return str(e)
        
class Request:
    def __init__(self,url,method,headers,body):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
    #we should check if those types are allowed before conversion
    #the conversion methods should return the prep object
    def isGetAllowed(self):
        pass
    def isPostFormAllowed(self):
        pass
    def isPostJsonAllowed(self):
        pass
    def isPostXmlAllowed(self):
        pass
    def isPostMultipartAllowed(self):
        pass
    def isPutFormAllowed(self):
        pass
    def isPutJsonAllowed(self):
        pass
    def isPutXmlAllowed(self):
        pass
    def isPutMultipartAllowed(self):
        pass
    def isPatchFormAllowed(self):
        pass
    def isPatchJsonAllowed(self):
        pass
    def isPatchXmlAllowed(self):
        pass
    def isPatchMultipartAllowed(self):
        pass
    def toGet(self):
        pass
    def toPostForm(self):
        pass
    def toPostMultipart(self):
        pass
    def toPostXml(self):
        pass    
    def toPostJson(self):
        pass
    def toPutForm(self):
        pass
    def toPutMultipart(self):
        pass
    def toPutXml(self):
        pass    
    def toPutJson(self):
        pass
    def toPatchForm(self):
        pass
    def toPatchMultipart(self):
        pass
    def toPatchXml(self):
        pass    
    def toPatchJson(self):
        pass
        
class Result:
    def __init__(self,url,method,headers,body,query,status_code):
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.query = query
        self.status_code = status_code
        
class Fuzzer(Thread):
    def __init__(self,queue,url,method,headers,session_cookies,body,num_of_cookies,num_of_threads,delay,wordlist,value_type,custom_value):
        Thread.__init__(self)
        self.results_queue = queue
        self.url = url
        self.method = method
        self.headers = headers
        self.body = body
        self.delay = delay
        self.session_cookies = session_cookies
        self.num_of_cookies = num_of_cookies
        self.num_of_threads = num_of_threads
        self.wordlist = wordlist
        self.cookie_groups=[]
        self.value_type = value_type
        self.custom_value = custom_value
        self.lines=[]
        self.baseParams = {}
        self.baseCookies = {}
        self.addthose = []
        self.originalresponse = {}
        with open(wordlist) as read:
            self.lines=read.read().splitlines()
        
    def brute(self,cookies_group):
        cookies_group.update(self.baseCookies)
        response = self.request(cookies_group)
        #now we compare to original if not similar then return params_group else return None
        res = self.compare(response)
        if res[2]!="":
            #print(response.text)
            return {"reflects":res[0],"different_type":res[1],"diffs":res[2],"cookies":cookies_group,"value_type":self.value_type}
        return None
    def formCookieHeader(self,cookies_group):
        cookiestr=""
        for cookie in cookies_group:
            cookiestr=cookiestr+cookie+"="+cookies_group[cookie]+"; "
        return cookiestr.strip().strip(';')
       
    def request(self,cookies_group):
        self.removeContentType()
        self.setHeaderValue(self.headers,"Cookie",self.formCookieHeader(cookies_group))
        self.baseParams.update({"rand":''.join(random.choices(string.ascii_lowercase+string.digits, k=5))})
        req = requests.Request(method="get", url=self.url, headers=self.headers,params=self.baseParams) #,cookies=cookies_group)
        prep = req.prepare()
        #prep.headers=headers_group
        resp = None
        with requests.Session() as session:
            #session.proxies = {"http":"http://127.0.0.1:8080","https":"http://127.0.0.1:8080"}
            try:
                resp = session.send(prep, verify=False,allow_redirects=False)
                if resp == None:
                    try:
                        resp = session.send(prep, verify=False,allow_redirects=False)
                    except:
                        pass
            except:
                try:
                    resp = session.send(prep, verify=False,allow_redirects=False)
                    if resp == None:
                        try:
                            resp = session.send(prep, verify=False,allow_redirects=False)
                        except:
                            pass
                except:
                    pass
        return resp
        
    def isJsonBody(self):
        try:
            j=json.loads(self.body)
            if type(j)==dict:
                return True
            else:
                return False
        except:
            return False
    
    def isXmlBody(self):
        try:
            xmltodict.parse(self.body)
            return True
        except:
            return False
            
    def parseMultipart(self):
        params = {}
        boundary = self.getHeaderValue(headers,"Content-Type")
        if boundary != None:
            boundary = boundary.split("oundary=")[-1]
        bodyparts = self.body.strip('--').split(boundary)
        parts = []
        for part in bodyparts:
            if part != '':
                parts.append(part.strip('--').strip())
        for item in parts:
            value = item.split('\n\n',1)[1]
            chunks = item.split()
            name = chunks[2].split('=')[1].strip('";\'')
            if chunks[3].startswith("filename="):
                filename = chunks[3].split('=')[1].strip('";\'')
            params.update({name:value})
        return params
            
    def getParams(self):
        query = ""
        if '?' in self.url and not self.url.endswith('?'):
            query = self.url.split('?',1)[1]
        self.url = self.url.split('?')[0]
        if query != "":
            paramchunks = query.split('&')
            for chunk in paramchunks:
                minichunk = chunk.split('=')
                if len(minichunk)>1:
                    self.baseParams.update({minichunk[0]:minichunk[1]})
                else:
                    self.baseParams.update({minichunk[0]:""})
        if self.body!="":
            ctype = self.getHeaderValue(self.headers,"Content-Type")
            if ctype == None:
                ctype=""          
            if "boundary" in ctype.lower():
                self.baseParams.update(self.parseMultipart())
            elif self.isJsonBody():
                try:
                    self.baseParams.update(json.loads(self.body))
                except:
                    pass
            
            elif self.isXmlBody():
                try:
                    params = xmltodict.parse(self.body)
                    if len(params) == 1 and params["root"]:
                        self.baseParams.update(params["root"])
                    else:
                        self.baseParams.update(params)
                except:
                    pass
            else:
                paramchunks = self.body.split('&')
                for chunk in paramchunks:
                    minichunk = chunk.split('=')
                    if len(minichunk)>1:
                        self.baseParams.update({minichunk[0]:minichunk[1]})
                    else:
                        self.baseParams.update({minichunk[0]:""})
    def removeContentType(self):
        for header in self.headers:
            if header.lower()=="content-type":
                del self.headers[header] 
                return
            
    def setHeaderValue(self,headers,headername,new_value):
        for header in headers:
            if header.lower() == headername.lower():
                headers[header] = new_value
                return headers
        headers[headername] = new_value
        return headers
        
    def getHeaderValue(self,headers,headername):
        for header in headers:
            if header.lower() == headername.lower():
                return headers[header]
        return None
    
    def numOfHeader(self,headers,headername):
        count = 0
        for header in headers:
            if header.lower() == headername.lower():
                count+=1
        return count
    
    def getHeaderName(self,headers,headername):
        count = 0
        for header in headers:
            if header.lower() == headername.lower():
                return header
        return None
        
    def getResponseProps(self,response):
        try:
            num_of_bytes = int(self.getHeaderValue(response.headers,"Content-Length"))
        except:
            num_of_bytes = len(response.content)
        num_of_words = len(response.content.split())
        headerstr=str(response.headers)
        num_of_reflects = response.text.count("discobiscuits")+response.text.count("172.172.172.172")+headerstr.count("discobiscuits")+headerstr.count("172.172.172.172")
        num_of_headers = len(response.headers)
        content_type = self.getHeaderValue(response.headers,"content-type")
        status_code = response.status_code
        num_of_cookies = self.numOfHeader(response.headers,"set-cookie")
        num_of_lines = len(response.text.split("\n"))
        size_of_headers = len(str(response.headers))
        return {"size_of_headers":size_of_headers,"num_of_lines":num_of_lines,"num_of_cookies":num_of_cookies,"status_code":status_code,"num_of_bytes":num_of_bytes,"num_of_words":num_of_words,"num_of_reflects":num_of_reflects,"num_of_headers":num_of_headers,"content_type":content_type}
            
    def compare(self,response):
        if response == None:
            return (0,False,"")
        diffs=""
        rate = 0
        diff = False #different content type
        props = self.getResponseProps(response)
        if props["num_of_reflects"] > 0: #!= self.originalresponse[reqtype]["num_of_reflects"]:
            diffs+="Reflect-"
            rate+=1
        if self.originalresponse == {}:
            return (props["num_of_reflects"],diff,diffs.strip("-"))
        if props["content_type"]!=self.originalresponse["content_type"]:
            diffs+="Content_Type-"
            rate+=1
            diff = True
        if props["status_code"]!=self.originalresponse["status_code"]:
            diffs+="Status_Code-"
            rate+=1
        if props["num_of_words"]!=self.originalresponse["num_of_words"]:
            diffs+="Words-"
            rate+=1
        if props["num_of_lines"]!=self.originalresponse["num_of_lines"]:
            diffs+="Lines-"
            rate+=1
        if abs(props["num_of_bytes"]-self.originalresponse["num_of_bytes"]) > 5:
            diffs+="Body Size-"
            rate+=1
        if props["num_of_headers"]!=self.originalresponse["num_of_headers"]:
            diffs+="Headers Number-"
            rate+=1
        if props["num_of_cookies"]!=self.originalresponse["num_of_cookies"]:
            diffs+="Cookies-"
            rate+=1
        if abs(props["size_of_headers"]-self.originalresponse["size_of_headers"]) > 5:
            diffs+="Headers Size-"
            rate+=1
        return (props["num_of_reflects"],diff,diffs.strip("-"))
        
    def filterHeaders(self):
        for header in self.headers.copy():
            if header.lower().startswith("accept"):
                del self.headers[header]
            if header.lower().startswith("if-"):
                del self.headers[header]
            if header.lower() == "connection":
                del self.headers[header]
            if header.lower().startswith("upgrade-insecure-requests"):
                del self.headers[header]
            if header.lower().startswith("sec-fetch-"):
                del self.headers[header]
            if header.lower() == "te":
                del self.headers[header]
            
    def calculateOriginal(self):
        #we set the "Accept-Encoding: identity" to prevent compressed responses
        try:
            req = requests.Request(method="get", url=self.url, headers=self.headers,params=self.baseParams)
            prep = req.prepare()
            response = None
            with requests.Session() as session:
                response = session.send(prep, verify=False,allow_redirects=False)
                if response == None:
                    response = session.send(prep, verify=False,allow_redirects=False)
            if response != None:
                self.originalresponse = self.getResponseProps(response)
                self.loadSetCookies(response)
        except:
            self.originalresponse = {}
    def chooseCookieValue(self):
        val = ""
        if self.value_type == "bad":
            val = badval
        elif self.value_type == "normal":
            val = normalval
        else:
            val = self.custom_value+"/discobiscuits"
        return val
        
    def loadCookies(self):
        cookiestr=self.getHeaderValue(self.headers,"cookie")
        cookies=cookiestr.split(';')
        for cookie in cookies:
            cookie=cookie.strip()
            parts=cookie.split('=')
            if len(parts)<2:
                parts[1] = ""
            if not parts[0] in self.session_cookies:
                self.addthose.append(parts[0])
            else:
                self.baseCookies.update({parts[0]:parts[1]})
    def loadSetCookies(self,response):
        for header in response.headers:
            if header.lower() == "set-cookie":
                name = response.headers[header].split('=')[0]
                if not name in self.session_cookies:
                    if not name in self.addthose:
                        self.addthose.append(name)
    def run(self):
        #set accept-encoding to identity to avoid compressed response
        self.headers = self.setHeaderValue(self.headers,"Accept-Encoding","identity")
        #get base params
        self.getParams()
        #get base cookies
        self.loadCookies()
        #calculate original response
        self.calculateOriginal()
        #add host header is not there
        hostname = urlparse(self.url).netloc
        if self.getHeaderName(self.headers,"host") == None:
            self.headers["Host"] = hostname
        # add newly discovered cookies to list
        print(self.baseCookies)
        for entry in self.addthose:
            self.lines.append(entry)
        #divide parameters into groups
        chunk = {}
        for i in range(len(self.lines)):
            chunk.update({self.lines[i]:self.chooseCookieValue()})
            if i % self.num_of_cookies == 0:
                self.cookie_groups.append(chunk)
                chunk={}
        if i % self.num_of_cookies != 0:
            if chunk != {}:
                self.cookie_groups.append(chunk)
        #print just to be sure
        #print(self.param_groups)   #verified now go on
        if self.delay <= 0 and self.num_of_threads > 1:
            #send them to pool
            threadpool = ThreadPoolExecutor(max_workers=self.num_of_threads)
            #try to pass both reqtype and params_group to brute then make the compare in brute and return None if similar or params_group if not similar
            #futures = (threadpool.submit(self.brute, grp) for grp in self.param_groups)
            futures=[]
            for grp in self.cookie_groups:
                futures.append(threadpool.submit(self.brute, grp))
            for i, result in enumerate(as_completed(futures)):
                if result.result():
                    self.results_queue.put(result.result())
        else:
            for grp in self.cookie_groups:
                result = self.brute(grp)
                if result:
                    self.results_queue.put(result)
                if self.delay > 0:
                    time.sleep(self.delay)
        self.results_queue.put(None)
        
class CookieHammer:
    def __init__(self,url,method="GET",headers={},session_cookies=[],body="",num_of_cookies=20,num_of_threads=10,delay=0,wordlist="burp7070/headers.lst",value_type="normal",custom_value=""):
        self.results_queue = Queue()
        self.url = url
        self.method = method
        self.headers = headers
        self.num_of_cookies = num_of_cookies
        self.num_of_threads = num_of_threads
        self.delay = delay
        self.body = body
        self.session_cookies = session_cookies
        self.value_type = value_type
        self.custom_value = custom_value
        self.wordlist = wordlist
        fuzzer = Fuzzer(self.results_queue,self.url,self.method,self.headers,self.session_cookies,self.body,self.num_of_cookies,self.num_of_threads,self.delay,self.wordlist,self.value_type,self.custom_value)
        fuzzer.start()
        
    def __iter__(self):
        return self

    def __next__(self):
        res = self.results_queue.get()
        self.results_queue.task_done()
        if not res:
            raise StopIteration
        return res
        

#results_queue=Queue()
#addthread=Thread(target = th, args = (results_queue, ))
#addthread.start()
ph = CookieHammer(url="https://0a0c00b9045364e28308239c00840076.web-security-academy.net/",method="get",headers={"Cookie":"session=vG5AtS7glMvzCPy9AbvIOsUOh0uheATR; fehost=prod-cache-01","Host":"0a0c00b9045364e28308239c00840076.web-security-academy.net","User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0"},session_cookies=["session"],body="",value_type="normal")
for p in ph: #ph.fuzz():
    print(p)
