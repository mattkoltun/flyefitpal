# flyefitpal

A quick way to book your gym session with https://www.flyefit.ie/. 


## Requirements
You need to have a Google Chrome installed on the computer you run the program on.

## Install

Install the requirements
```
pip install -r requirements.txt
```

## Run 

In your favourite shell run the command:

(Make sure that time slot is exactly the same as on the website for the given site!)

```
# activate the 
# ./main.py -e <email> -p <password> -s <site> -t <time_slot> 
./main.py -e me@mail.com -p itsme -s Swords -t '07:00 - 08:15' 

```



## Help

```
./main.py --help
                                                                                            
Synopsis:                                                                                   
        main.py -e <email> -p <password> -s <site> -t <time_slot>

          e.g.    main.py -e me@exmaple.com -p supersecret123 -s 'Liffey Valley' -t '13:30 - 14:45'                                                                     
        -e, --email             : Login email                                               
        -p, --password          : Login password                                            
        -s, --site              : Gym location, must be exactly the same as on the Website  
                                        e.g. 'Liffey Valey', 'Cork City', 'CHQ', 'Swords'   
        -t, --time              : Session time (24hrs format), must be exactly the same as on the Website
                                        e.g. '05:30 - 06:45', '15:00 - 16:15', '10:15 - 11:30'
        -h, --help              : Print this message                                        
```
                                                                                            
