# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 19:27:51 2017

@author: Jeong Ji Hoon
@ Knowblesse

Description:
    Fetch HTML data from the JoN Web archive and get Statistics about # of papers in each division
    JoN archive access permission is needed.
    Only use this script on university's network.
"""
# Import Modules
import urllib3
from html.parser import HTMLParser

############## C L A S S E S ##############
""" Abstract URL Parser """
class JNStatParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.Section = [0,0,0,0,0]
        self.SectionTag = -1
        
    def handle_starttag(self, tag, attrs):
        if tag == 'h2':
            if ('id', 'cellular-molecular') in attrs:
                self.SectionTag = 0
            if ('id', 'development-plasticity-repair') in attrs:
                self.SectionTag = 1
            if ('id', 'systems-circuits') in attrs:
                self.SectionTag = 2
            if ('id', 'behavioral-cognitive') in attrs:
                self.SectionTag = 3
            if ('id', 'neurobiology-of-disease') in attrs:
                self.SectionTag = 4
        # Get Abstract Link        
        if self.SectionTag != -1:
            if  tag == 'h1':
                if ('class','highwire-cite-title') in attrs:
                    self.Section[self.SectionTag] = self.Section[self.SectionTag] + 1
    def getSectionStat(self):
        return self.Section
        
############## P A R A M T S ##############       
YEAR = 2012       

# 1 Cellular/Molecular
# 2 Development/Plasticity/Repair
# 3 Systems/Circuits
# 4 Behavioral/Cognitive
# 5 Neurobiology of Disease


############## M E T H O D S ##############

""" Create Abstract File"""
yearCode = YEAR - 1980
sizeSection = [0,0,0,0,0]

for issue in range(1,51):
    
    AbstractData = []
    
    # Setup URL Connection
    url = 'http://www.jneurosci.org/content/' + str(yearCode) + '/' + str(issue)
    http = urllib3.PoolManager()
    r = http.request('GET',url)
    data = r.data.decode('utf-8')
    
    
    parser = JNStatParser()
    parser.feed(data)
    
    for el in range(0,5):
        sizeSection[el] = sizeSection[el] + parser.getSectionStat()[el]    
    print('Year ' + str(YEAR) + ' Issue ' + str(issue) + ' Data is Successfully fetched.')
    print('%d%% Completed\n'% (issue*2))

print(sizeSection)