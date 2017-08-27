from threading import Thread
import threading
import time
import requests
from requests.exceptions import HTTPError
import requests.packages.urllib3
import sys
import os
from subprocess import call

PAUSE=False


requests.packages.urllib3.disable_warnings()  #disables InsecurePlatformWarning and SNIMissingWarning
#resultfile = './out.txt'                                                    
path_to_wordlist=os.path.dirname(os.path.realpath(__file__))+'/wordlist/'   #tentative, till I figure out the bug

retries=0
wordlist='./wordlist/Directories_Common.wordlist'     #default wordlist
time_wait=0.05
TARGET=""
filter_type=''
filter_file_type=''
output=[]

contains_search=False

errorlist = {
200: "Ok", 
301: "Redirect", 
302: "Redirect", 
303: "Redirect", 
307: "Redirect",
308: "Redirect", 
400: "Bad Request", 
401: "Unauthorized", 
403: "Forbidden", 
404: "Not Found", 
463: "Resource Unavailable (unlisted error code, meaning may vary)"
}


def show(res, url):  #change later to save, sort/filter, etc...

  if (filter_type=='' or 'filetype' in filter_type) and res !='ERROR':
    print(url + (" "*(50-len(url) )) + res )#+ ' : ' + errorlist(res))
  elif filter_type=='Ok':
    if res=='Ok':
      print(url + (" "*(50-len(url) )) + res)
  elif filter_type=='N':
    if res=='Not Found':
      print(url + (" "*(50-len(url) )) + res)
  elif filter_type=='F':
    if res=='Forbidden':
      print(url + (" "*(50-len(url) )) + res)
  elif filter_type=='Bad':
    if res=='Bad Request':
      print(url + (" "*(50-len(url) )) + res)
  elif filter_type=='R':
    if res=='Redirect':
      print(url + (" "*(50-len(url) )) + res)
  elif filter_type=='Un':
    if res=='Unauthorized':
      print(url + (" "*(50-len(url) )) + res)
  
  
def kill():
  sys.exit()
  call(['killall',  'python'])  #worth a shot, I guess


def countdown(count):
  for each in range(-1*count, 0):
    print(str(-1*each) + "  ")
    time.sleep(1)




def poke(url):
  global PAUSE
  #lock = lambda a : lock(time.sleep(1)) if PAUSE else 1+1                        #this actually does the requesting
  while PAUSE:
    time.sleep(1)
  
  f_type=filter_file_type
  global output
  global retries
  
  if retries==-1:
    kill()
   
  if 'www' not in url: 
    url=url.replace('http://', 'http://www.')  #tentative fix
  if '.' in url:
    url_type= url.split('.')[2:]
    if '/' in url_type:
      url_type=url_type.split('/'[0])
   
  if f_type == url_type[-1] or f_type=='':
    
    file_type=url.split('.')[-1]
    quit=False


    #lock('a')

    try:
      
      r=requests.get(url, timeout=5)      
      r.close()
      r=str(r)
      code=r.split("[")[1].split("]")[0]
      code=int(code)
      response = errorlist[code]
    except KeyError:
      response = "code not found : "+str(code)
    except requests.exceptions.ConnectionError:
      if retries<2:
        print "Connection Error.\nRetrying in one second."
        #PAUSE=True
        #time.sleep(1)
        countdown(3)
        retries = retries + 1
        poke(url)  #no clue what this'll do
      else:
        print "Connection Failed.  Quitting..."
        retries=-1
        PAUSE=False
        t = Thread(target=kill, args=()) #should help kill the program if something goes wrong
        t.start()
      
      
        
    except:  #this just looked kinda off.  we'll see what happens
      lines.append(url[:-1].split("/")[-1])
      response = "ERROR"
    
    if quit==True:#
      sys.exit()#
    output.append([response, url])
    
    #t=Thread(target=show_progress, args=(url,))
    #t.start#show(response, url)  #this condition seems to be causing problems way downstream.  be cautious
    
    show(response, url)

def print_help():
  print('\n-n <name>  -- domain name of target \"xxxx.xxx\"\n')

  print('-?/-help/--help  -- print commands\n')

  print('-f  Ok/N/F/Bad/R/Un  -- filter output by response type.\n  available options are:\n\n    Ok -  code 200\n    N -   code 404 (not found)\n    F -   code 403 (forbidden)\n    Bad - code 400 (bad request)\n    R -   redirect\n    Un -  code 401 (unauthorized)\n')

  print('filetype <extension> (only look for files with the given extension)')
  
  print('\n-t <time(seconds)>  -- set wait time between requests')  
  
  print('\n-w <option>/-w <wordlist>  -- set the wordlist to use.')
  print('\n  available options are:\n    common           (common directory names)')
  print('    all              (all directory names in default wordlist)')
  print('    +/plus/more  (a more intensive directory search than common)\n    ++ / -crazy      (a more intensive directory search than -plus)')

  print('    <wordlist>        (enter the path to your own wordlist)\n')
  print('-wf <option>/ -wf <wordlist>  -- search for filenames instead of directories.\n  Same options as -w\n')
  #print('-contains <options>/-contains <expression>  -- check the urls returned for an expression or pattern')
  #print('  forms (look for web pages containing forms)\n  nf (look for pages with custom 404 pages)\n  of (ignore missing pages that didn\'t return an error code)\n  <expression> (look for pages containing the given string)')

  #need a "not" contains too.  there might be a sneaky way around recoding shit

  print('\nMore later')  
  sys.exit()


def set_wordlist(arg):
  global wordlist
  if arg=='common':
    wordlist=path_to_wordlist+'Directories_Common.wordlist'
  elif arg=='all':
    wordlist=path_to_wordlist+'Directories_All.wordlist'
  elif arg=='+' or arg=='plus' or arg=='more':
    wordlist=path_to_wordlist+'Directories_Extra.wordlist'
  elif arg=='++' or arg=='crazy':
    wordlist=path_to_wordlist+'Directories_Crazy.wordlist'
  else:
    wordlist = path_to_wordlist+arg
    try:
      f=open(wordlist, 'r')
      f.close()
    except IOError:
      print('The File ' + wordlist + ' Could Not Be Found in the folder ' + path_to_wordlist)
      sys.exit()


def set_wordlist_files(arg):
  global wordlist
  if arg=='common':
    wordlist=path_to_wordlist+'Filenames_Doted_Common.wordlist'
  elif arg=='all':
    wordlist=path_to_wordlist+'Filenames_Doted_All.wordlist'
  elif arg=='+' or arg=='plus' or arg=='more':
    wordlist=path_to_wordlist+'Filenames_Doted_Extra.wordlist'
  elif arg=='++' or arg=='crazy':
    wordlist=path_to_wordlist+'Filenames_Doted_Crazy.wordlist'
  else:
    wordlist = path_to_wordlist+arg
    try:
      f=open(wordlist, 'r')
      f.close()
    except IOError:
      print('The File ' + wordlist + ' Could Not Be Found in the folder ' + path_to_wordlist)
      sys.exit()



args=[]

if len(sys.argv) >1:
  args=sys.argv
  TARGET=str(sys.argv[1])
  #if 'www' not in TARGET: TARGET='www.'+TARGET #

  if "http://" not in TARGET: TARGET = "http://" + TARGET
  if TARGET[-1] != "/": TARGET = TARGET + "/"


for each in args:

  if each == '-?' or each == '-help' or each == '--help' or each =='/?' or each == '/help':
    print_help()
  
  if each == '-w':                                           #wordlist - directory search
    arg=args[args.index(each)+1]
    set_wordlist(arg)

  if each== '-wf':                                           #wordlist - file search
    try:
      arg=args[args.index(each)+1]
      set_wordlist_files(arg)
    except IndexError:
      print 'You must provide an argument for -wf\n'
      sys.exit()
    
  if each == '-n':                                           #target name
    TARGET = args[args.index(each)+1]
    if "http://" not in TARGET: TARGET = "http://" + TARGET
    if TARGET[-1] != "/": TARGET = TARGET + "/"
  
  if each == '-f':                                           #filter type
    filter_type = args[args.index(each)+1]
    if filter_type not in ['Ok','N','F','Bad','R','Un']:
      print 'filter type \"' + filter_type + '\" not recognized.  Enter -? for help\n'
      sys.exit()
    #if '-filetype=' in filter_type:#.contains('filetype='):
    #work out filter structure 
    #print('filter functionality incomplete')
   
  if each=='filetype':
    #filter_file_type=filter_type.split('=')[-1]
    filter_file_type = sys.argv[sys.argv.index(each)+1]
    #print filter_file_type

  if each == '-ports' or each == '-p':                       #port scan
    #nmap, run a basic scan and return   
    print('port scanning capabilities incomplete')  
  
  if each == '-fuzz':                                        #port fuzzer
    #basic port fuzzer
    print('port fuzzing capabilities incomplete')
  
  if each == '-t':                                           #wait time
    time_wait=float(sys.argv[sys.argv.index(each)+1])
  
  if each == '-contains':                                    #expression search/scrape
    print 'the -contains switch is not currently functional'
    sys.exit()

    

def find(argument, page):  #return line number that the argument is on, or -1 if it's not found
  lines=page.split('\n')
  for each in range(0,len(lines)):
    if argument in lines[each]:
      return each
  return -1
  
     

def find_and_print(argument, page):
  if argument in page:
    for each in page.split('\n'):
      if argument in each:
        line_number=str(lines.index(each))       
        ind = page.index(argument)
        if ind+250 < len(page):
          print 'Expression found on line ' +line_number + ' of file ' + url# + each[1]
          print '\n' + page[ind:ind+200]+'\n'
        else:
          print 'placeholder'
          print 'Expression found on line ' +'5' + ' of file ' + url#each[1]
          print '\n' + page[ind:]+'\n'




if TARGET=="" or len(sys.argv)==0:
  print_help()
 

fin = open(wordlist, "r")
lines = fin.readlines()

last=0

print('Scanning...\n')
for each in range(last, len(lines)):
  num_threads = threading.active_count()
  #print num_threads
  if num_threads < 20:
    addr=TARGET+lines[each]#+"/"
    addr=addr.replace("\n", "")
    t = Thread(target=poke, args=( addr,) )
      
    time.sleep(time_wait)  # avoid spiking traffic upon startup
    
    t.start()
  else:
    last = last -1
    time.sleep(0.4)

#############################################################the file stuff is pretty much ok.  time to move on





