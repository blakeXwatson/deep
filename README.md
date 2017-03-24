# deep
Remote File/Directory Fuzzer, Lan Host Enumerator, Port/Vulnerability Scanner

Currently in Alpha
Current version = v0.3

Setup-----------------------------------------
deep is written for python 2.7 (python 3 will not work)

repositories in use:
  threading
  time
  requests
  sys
  os
  subprocess
  
 All of these should be installed by default.  If, for whatever reason, a package cannot be found, use pip install to download and install it.
 
 deep requires numerous wordlists, stored in an adjacent folder called wordlist, in order to function.
 These wordlists are included on the github page in the folder "wordlist"
 
 ---------------------------------------------------------------------------------------
 
 Functions:
   deep is currently able to fuzz remote http server in order to reveal directories and files, and filter output by response code and filetype.
   
-n <name>  -- domain name of target "xxxx.xxx"

-?/-help/--help  -- print commands

-f  Ok/N/F/Bad/R/Un  -- filter output by response type.
  available options are:

    Ok -  code 200
    N -   code 404 (not found)
    F -   code 403 (forbidden)
    Bad - code 400 (bad request)
    R -   redirect
    Un -  code 401 (unauthorized)

filetype <extension> (only look for files with the given extension)

-t <time(seconds)>  -- set wait time between requests

-w <option>/-w <wordlist>  -- set the wordlist to use.

  available options are:
    common           (common directory names)
    all              (all directory names in default wordlist)
    +/plus/more  (a more intensive directory search than common)
    ++ / -crazy      (a more intensive directory search than -plus)
    <wordlist>        (enter the path to your own wordlist)

-wf <option>/ -wf <wordlist>  -- search for filenames instead of directories.
  Same options as -w
  
  


