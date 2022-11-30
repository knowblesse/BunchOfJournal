# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 19:27:51 2017

@author: Jeong Ji Hoon
@ Knowblesse

Description:
    Fetch HTML data from the JoN Web archive and Save to .txt
    JoN archive access permission is needed.
    Only use this script on university's network.
"""
# Import Modules
import urllib3
from html.parser import HTMLParser
import re

############## C L A S S E S ##############
    
""" Abstract URL Parser """
class JNAbstractAddParser(HTMLParser):
    # Get URL of Abstracts
    def __init__(self, year, issue):
        HTMLParser.__init__(self)
        self.SectionFlag = False # Flag for Behavioral/Cognitive Section
        self.AbsUrl = []
        self.urlform = '/content/'+str(year)+'/'+str(issue)+'/\d{1,4}'
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href':
                    self.AbsUrl.append(attr[1])
    def getAbstractURL(self):
        outputUrl = []
        for url in self.AbsUrl:
            _r = re.match(self.urlform, url)
            if _r:
                outputUrl.append(_r[0])
        return outputUrl
        
""" Abstract Preview Page Parser """        
class JNAbstractParser(HTMLParser):
    # Get data from the abstract page
    def __init__(self):
        HTMLParser.__init__(self)
        self.abstractDivFound = False
        self.abstractFound = False
        self.abstractEnd = False
        self.OutputData = []
        
    def handle_starttag(self, tag, attrs):
        if self.abstractDivFound == False:
            if tag == 'div':
                for attr in attrs:
                    if attr[0] == 'id':
                        if 'abstract' in attr[1]:
                            self.abstractDivFound = True
        else:
            if tag == 'p':
                self.abstractFound = True

    def handle_endtag(self, tag):
        if self.abstractFound and (not self.abstractEnd):
            if tag == 'p':
                self.abstractEnd = True
            
    def handle_data(self, data):
        if self.abstractFound and (not self.abstractEnd):
            self.OutputData.append(data)
            
    def getAbstract(self):
        return  "".join(self.OutputData)


############## P A R A M T S ##############       
YEAR = 2022 # 어떤 년도에 나온 글들을 뽑아올지.
IssueNum = 50 # 몇번쨰 Issue 까지 글을 뽑아올지. 최대는 50


############## M E T H O D S ##############

""" Create Abstract File"""
yearCode = YEAR - 1980 # Volumn number. 2018년 = 38, 2017년 = 37
sizeAbstract = 0
# Issue Num 이 정의되어 있지 않다면다면 그냥 끝까지 받아옴
if "IssueNum" not in globals():
    IssueNum = 50

for issue in range(1,IssueNum+1):
    
    AbstractData = []
    
    # Setup URL Connection
    url = 'http://www.jneurosci.org/content/' + str(yearCode) + '/' + str(issue)
    http = urllib3.PoolManager()
    r = http.request('GET',url)
    data = r.data.decode('utf-8')
    
    # Get Abstract URL Data            
    parser = JNAbstractAddParser(yearCode, issue)
    parser.feed(data)
    urldata = parser.getAbstractURL()
    sizeAbstract = sizeAbstract + len(urldata)
    print('Processing 00', end='')
    numProcessed = 0
    for abstract in urldata:
        http = urllib3.PoolManager()
        r = http.request('GET','http://www.jneurosci.org'+abstract)
        data = r.data.decode('utf-8')
        parser = JNAbstractParser()
        parser.feed(data)
        if parser.abstractFound:
            AbstractData.append(parser.getAbstract())
            numProcessed += 1
            print(f'\b\b{numProcessed:02d}', end='')
    print('')
    # Write File
    try:
        with open('Abstracts_' + str(YEAR) + '.txt', 'a', encoding='UTF-8') as f:
            for dat in AbstractData:
                f.writelines(dat)
                f.write('\n\n')
            f.writelines('\n\n\n\n')
    except IOError as err:
        print('Error : ' + str(err))
    
    print('Year ' + str(YEAR) + ' Issue ' + str(issue) + ' Data is Successfully fetched.')
    print('%5.2f%% Completed\n'% (issue/IssueNum*100))
        