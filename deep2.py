import getch
#turns off insecure platform warning from requests.  
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

import requests
import threading
from threading import Thread
import time
import os
from subprocess import check_output
import sys
import traceback


class Deep:
  def __init__(self, args=[]):
    if len(args)<1:
      self.print_help()
      exit()

    self.listening=False
    self.failed=[]    #failed urls
    self.path='/home/ball-tongue/deep/'
    self.args=args
    self.target=''
    self.switches={}
    self.switches['-t'] = 0
    self.switches['--dir'] = 'None'
    self.switches['--file'] = 'None'
    self.switches['-p'] = '80'
    self.switches['-f'] = ''  #only show these
    self.switches['-rm'] = '' #don't show these
    self.switches['--threads'] = 10  #play with
    self.switches['--timeout'] = 5
    self.switches['--tries'] = 2
    self.switches['--useragent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'    #recent chrome.
    self.switches['--protocol'] = 'http'
    self.parse_args()
    self.convert_args()            
    self.check_scan_type()  #cleans up -w & -wf arg logic.
    if self.target=='':
      print 'you must provide a target ip or url'
      print 'use --help to see usage'
      exit()
    self.load_file()
    self.set_filters()
    self.scanned_count = 0
    self.start()


  def print_progress(self):      #might implement with an nmap style keypress to get current progress.
   sys.stdout.write(str(self.scanned_count) + ' scanned.  ' + str((self.scanned_count+.0)/self.list_length)+'% finished.')

  
  def show(self, url, code, req):
    url=url.split(':'+self.switches['-p'])[1]
    padding=20-len(url)
    spaces=' '*padding
    meaning=''
    if code in self.filters:
      meaning=self.filters[code]
    msg=url+spaces+code.strip()+'   ' + meaning.strip()
    sys.stdout.write(msg+'\n')  #note to self: stdout.write avoids the spacing issues that usually pop up when threading


  def check_page(self, url):
    self.scanned_count = self.scanned_count+1
    for each in range(0,self.switches['--tries']):
      try:  #leave the loop as soon as you get a response
        r=requests.get(url, timeout=self.switches['--timeout'])
        code=str(r.status_code)
        if self.passes_filters(code):
          #could pass r elsewhere and do a regex check or something as well
          self.show(url, code, r)
        break
      except:
        self.failed.append(url)

    time.sleep(self.switches['-t'])  #

  
  def passes_filters(self, code):
    if self.switches['-f']==[''] and self.switches['-rm']==['']: #no filters
      return True
    if self.switches['-f']!=[''] and self.switches['-rm']!=['']: #both applied
      print 'use -f or -rm, not both'
      exit()
    if self.switches['-f']==['']:  #if -rm is being used
      if code not in self.switches['-rm']:
        return True
      else:
        return False
    if self.switches['-rm']==['']:  #if -f is being used
      if code in self.switches['-f']:
        return True
      else:
        return False
    
    print 'idk what happened here.'
    return True  #?


  def start(self):
    self.target.replace('www.', '')
    #cut proto out of target url
    try:self.target = self.target.split('://')[1]
    except:pass      
    #build the url up with the right protocol and port.  
    self.target=self.switches['--protocol']+'://'+self.target
    self.target=self.target+':'+self.switches['-p']
    headers={'User-Agent':self.switches['--useragent']}

    while len(self.wordlist)>0:
      target_url=self.target+'/'+self.wordlist[0] #these two lines pop the next target file/dir into target_url
      self.wordlist.remove(self.wordlist[0])
      while threading.active_count()>self.switches['--threads']: #don't exceed max threads
        time.sleep(0.05)      #not sure what would be best here, honestly
      Thread(target=self.check_page, args=(target_url,)).start() #scan page


  def set_filters(self):
    self.filters={}
    self.filters['200'] = 'ok'
    self.filters['301'] = 'redirect'
    self.filters['302'] = 'redirect'
    self.filters['303'] = 'redirect'
    self.filters['307'] = 'redirect'
    self.filters['308'] = 'redirect'
    self.filters['400'] = 'bad request'
    self.filters['401'] = 'unauthorized'
    self.filters['403'] = 'forbidden'
    self.filters['404'] = 'not found'
    self.filters['463'] = 'resource unavailable'
    self.switches['-f'] = self.switches['-f'].split(',')    #break input (port1,port2,etc...) up into a list for passes_filters
    self.switches['-rm'] = self.switches['-rm'].split(',')

  
  def load_file(self):  #open the the file with all of the file/directory names and put them in a list
    f=open(self.word_file, 'r')
    raw=''
    for each in f.read():
      raw=raw+each
    f.close()
    lines=raw.split('\n')
    self.list_length=len(lines)
    self.wordlist=lines


  def convert_args(self):  #this converts all the necessary args (strings when entered) into ints
    try:
      self.switches['-t']=int(self.switches['-t'])
    except:
      print 'invalid arg type: ' + self.switches['-t']
      exit
    try:
      self.switches['--threads']=int(self.switches['--threads'])
    except:
      print 'invalid arg type: ' + self.switches['--threads']
      exit()
    try:
      self.switches['--timeout'] = int(self.switches['--timeout'])
    except:
      print 'invalid arg type: ' + self.switches['--timeout']
      exit()
    try:
      self.switches['--tries'] = int(self.switches['--tries'])
    except:
      print 'invalid arg type: ' + self.switches['--tries']
      exit()


  def check_scan_type(self):
    valid_args=['common', 'extra', 'crazy', 'all']
    if self.switches['--dir']!='None' and self.switches['--file']!='None':
      print 'cannot run directory scan and file scan simultaneously.'
      exit()
    if self.switches['--dir']=='None' and self.switches['--file']=='None':
      self.switches['--file']='common'

    if self.switches['--dir'] != 'None': #if directory mode
      if self.switches['--dir'] in valid_args:
        self.word_file=self.path+'wordlist/dir_'+self.switches['--dir']
      else:  #if passing a filename
        self.word_file=self.switches['--dir']

    if self.switches['--file'] != 'None': #if filename mode
      if self.switches['--file'] in valid_args:
        self.word_file=self.path+'wordlist/file_'+self.switches['--file']
      else:  #if passing a filename
        self.word_file=self.switches['--file']
    
    if not self.test_file(self.word_file):
      print 'file not found: ' + self.word_file
      exit()


  def test_file(self, filename):
    try:
      f=open(filename, 'r')
      f.close()
      return True
    except:
      return False


  def parse_args(self):
    if '--help' in self.args or '-h' in self.args or '/?' in self.args:
      self.print_help()
      exit()

    for each in self.args:
      if each in self.switches:
        argument=self.args[self.args.index(each)+1]
        self.switches[each]=argument
        self.args.remove(argument)  #remove arg from list
      elif self.args.index(each)==len(self.args)-1 or '.' in each:  #if this arg is probably the target
        self.target=each
      else:
        print 'invalid arg: ' + each
        print 'use --help to see usage'
        exit()


  def print_help(self):
    msg='''usage: deep <args> target (ip or domain name)
    args:
    -t  <seconds>        
        time between requests

    --dir <options/filename> 
        scan for directories
        options: common, extra, crazy, all

    --file <options/filename>
        scan for files
        options: common, extra, crazy, all

    -p <port>
        set the port to connect on 

    -f <code1,code2,etc...>
        only display pages with a particular response code/codes
        ex.  "deep -f 200,401,402 test.com" only displays pages that responded with 200,401, or 404 

    -rm <code1,code2,etc...>
        display pages that responded with anything but a particular code/codes
        ex.  "deep -rm 400 test.com" displays every page that doesn't respond with code 400

    --threads <number of threads>
        specify the number of threads to use.  default is 10
        going too high with this might cause DoS
        

    --timeout <seconds>
        specify how long to wait for a page to respond

    --tries <number of attempts>
        specify the number of times to try requesting a page before giving up.

    --useragent <user-agent string>
        specify a user-agent string to use for requests
        default is Chrome

    --help/-h
        display usage page.

    '''
    print msg



#############################################################
#if len(sys.argv)<2:
  
#  exit()

deep = Deep(sys.argv[1:])






###############################
#not in use
'''
  def find_interface(self):
    interfaces=[]
    rx_stats=[]
    tx_stats=[]
    lines=check_output(['ifconfig', '-s']).split('\n')
    for each in lines[1:]:
      interfaces.append(each.split(' ')[0])
      #rx_stats.append(int(each.split(' ')[3]))
      #tx_stats.append(int(each.split(' ')[7]))
    #for each in range(0, len(interfaces)):
    #  print interfaces[each] + 'rx: ' + str(rx_stats[each])
    for each in interfaces: print each
'''
