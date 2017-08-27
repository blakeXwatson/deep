Updated recently.
Better, faster, etc...

usage: deep <args> target (ip or domain name)
    
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
        going too high with this might DoS the target
        
    --timeout <seconds>
        specify how long to wait for a page to respond

    --tries <number of attempts>
        specify the number of times to try requesting a page before giving up.

    --useragent <user-agent string>
        specify a user-agent string to use for requests
        default is Chrome

    --help/-h
        display usage page.
