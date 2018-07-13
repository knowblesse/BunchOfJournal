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

############## C L A S S E S ##############
    
""" Abstract URL Parser """
class JNAbstractAddParser(HTMLParser):
    # Get URL of Abstracts
    def __init__(self):
        HTMLParser.__init__(self)
        self.SectionFlag = False # Flag for Behavioral/Cognitive Section
        self.AbsUrl = []
    def handle_starttag(self, tag, attrs):
        
        if tag == 'h2':
            if ('id', 'behavioral-cognitive') in attrs: # Find Only Behavioral/Cognitive Section of the page
                self.SectionFlag = True
            if ('id', 'ResearchArticlesBehavioralCognitive') in attrs: # 2018년 용
                self.SectionFlag = True
            if ('id', 'neurobiology-of-disease') in attrs:
                self.SectionFlag = False
            if ('id', 'ResearchArticlesNeurobiologyofDisease') in attrs: # 2018년 용
                self.SectionFlag = False
        # Get Abstract Link        
        if self.SectionFlag:
            if  tag == 'div':
                if ('class','highwire-article-citation highwire-citation-type-highwire-article tooltip-enable') in attrs: # 2012년(?) 부터 2017년까지 를 위한 tag
                    for attr in attrs:
                        if attr[0] == 'data-url':
                            self.AbsUrl.append(attr[1])
                if ('class','highwire-article-citation highwire-citation-type-highwire-article tooltip-enable hasTooltip') in attrs: # 2018 년 데이터의 경우 tag class 가 이렇게 바뀜.
                    for attr in attrs:
                        if attr[0] == 'data-url':
                            self.AbsUrl.append(attr[1])
         
    def getAbstractPreviewURL(self):
        return self.AbsUrl
        
""" Abstract Preview Page Parser """        
class JNAbstractParser(HTMLParser):
    # Get data from the abstract page
    def __init__(self):
        HTMLParser.__init__(self)
        self.DataFlag = 0
        self.OutputData = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            if self.DataFlag == 0:
                self.DataFlag = 1
            
    def handle_endtag(self, tag):
        if tag == 'p':
            self.DataFlag = 2
            
    def handle_data(self, data):
        if self.DataFlag == 1:
            self.OutputData.append(data)
            
    def getAbstract(self):
        return  "".join(self.OutputData)


############## P A R A M T S ##############       
YEAR = 2018 # 어떤 년도에 나온 글들을 뽑아올지.
IssueNum = 22 # 몇번쨰 Issue 까지 글을 뽑아올지. 최대는 50


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
    parser = JNAbstractAddParser()
    parser.feed(data)
    urldata = parser.getAbstractPreviewURL()
    sizeAbstract = sizeAbstract + len(urldata)
    
    for abstract in urldata:
        http = urllib3.PoolManager()
        r = http.request('GET','http://www.jneurosci.org'+abstract)
        data = r.data.decode('utf-8')
        parser = JNAbstractParser()
        parser.feed(data)
        AbstractData.extend([parser.getAbstract()])
    
    # Write File
    try:
        with open('Abstracts_' + str(YEAR) + '.txt', 'a', encoding='UTF-8') as f:
            for dat in AbstractData:
                f.writelines(dat)
                f.write('\n')
            f.writelines('\n\n')
    except IOError as err:
        print('Error : ' + str(err))
    
    print('Year ' + str(YEAR) + ' Issue ' + str(issue) + ' Data is Successfully fetched.')
    print('%5.2f%% Completed\n'% (issue/IssueNum*100))
        