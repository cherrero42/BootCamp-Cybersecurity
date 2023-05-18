# iron_dome

_____________________________________
 Bootcamp Cybersecurity | 42 Málaga
 
     i  r  o  n  _  d  o  m  e
_____________________________________

You will create a program called irondome that meets the following specifications.
• It will be developed for the Linux platform.
• The program will only execute when launched as root.
• The program will run in the background as a daemon or service.
• The program will monitor a critical zone in perpetuity. This route must be indicated as an argument.
•If more than one argument is provided, these will correspond to the file extensions
to be observed. Otherwise, all files will be monitored.
•The program will detect disk read abuse.
•The program will detect intensive use of cryptographic activity.
•The program will detect changes in the entropy of the files.
•The program should never exceed 100 MB of memory in use.
All alerts should be reported in the /var/log/irondome/irondome.log file.


May 2023