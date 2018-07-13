# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:51:00 2017

@author: Jeong Ji Hoon
@ Knowblesse

Description:
    Fetch HTML data from the JoN Web archive and Save to .txt
    This program fetches Full Text Version
    JoN archive access permission is needed.
    Only use this script on university's network.
"""
# Import Modules
import urllib3
from html.parser import HTMLParser

############## C L A S S E S ##############
    
""" Abstract URL Parser """
class JNFullTextAddParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.SectionFlag = False # Flag for Behavioral/Cognitive Section
        self.AbsUrl = []
    def handle_starttag(self, tag, attrs):
        
        if tag == 'h2':
            if ('id', 'behavioral-cognitive') in attrs: # Find Only Behavioral/Cognitive Section of the page
                self.SectionFlag = True
            if ('id', 'neurobiology-of-disease') in attrs:
                self.SectionFlag = False
        # Get Abstract Link        
        if self.SectionFlag:
            if  tag == 'div':
                if ('class','highwire-article-citation highwire-citation-type-highwire-article tooltip-enable') in attrs:
                    for attr in attrs:
                        if attr[0] == 'data-pisa':
                            self.AbsUrl.append(attr[1][7:]) # Delete first part 'jneuro;' and only save the page number 
    def getFullTextURL(self):
        return self.AbsUrl
        
""" Full Text Page Parser """        
class JNFTParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.StartFetching = False
        self.IsData = False
        self.OutputData = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'div': # 내용 시작하는 시점.
            if ('class','section abstract') in attrs:
                self.StartFetching = True
        if tag == 'div': # 내용 시작하는 시점.
            if ('class','section fn-group') in attrs:
                self.StartFetching = False
        if self.StartFetching: # fetching을 시작. 이후 p tag에 대해서는 전부 데이터로 입력받음.
            if tag == 'p':
                self.IsData = True
            
    def handle_endtag(self, tag):
        if tag == 'p':
            self.IsData = False
            
    def handle_data(self, data):
        if self.StartFetching & self.IsData:
            self.OutputData.append(data)
            
    def getFullText(self):
        return  "".join(self.OutputData)


############## P A R A M T S ##############       
YEAR = 2016       


############## M E T H O D S ##############

""" Create Abstract File"""
yearCode = YEAR - 1980
size = 0

for issue in range(1,50):
    
    Data = []
    
    # Setup URL Connection
    url = 'http://www.jneurosci.org/content/' + str(yearCode) + '/' + str(issue)
    
    # Get HTML Data from given url
    http = urllib3.PoolManager()
    r = http.request('GET',url)
    data = r.data.decode('utf-8')
    
    # Get Abstract URL Data            
    parser = JNFullTextAddParser()
    parser.feed(data)
    urldata = parser.getFullTextURL()
    size = size + len(urldata)
    
    for FTAdd in urldata:
        http = urllib3.PoolManager()
        url_FullText = 'http://www.jneurosci.org/content/'+FTAdd
        r = http.request('GET', url_FullText)
        data = r.data.decode('utf-8')
        parser = JNFTParser()
        parser.feed(data)
        Data.extend([parser.getFullText()])
    
    # Write File
    try:
        with open('FullText_' + str(YEAR) + '.txt', 'a', encoding='UTF-8') as f:
            for dat in Data:
                f.writelines(dat)
                f.write('\n')
            f.writelines('\n\n')
    except IOError as err:
        print('Error : ' + str(err))
    
    print('Year ' + str(YEAR) + ' Issue ' + str(issue) + ' Data is Successfully fetched.')
    print('%d%% Completed\n'% (issue*2))
        