# iron_dome

_____________________________________
 Bootcamp Cybersecurity | 42 Málaga
 
     i  r  o  n  _  d  o  m  e
_____________________________________


A program called irondome that meets the following specifications:

• Developed for the Linux platform.

• The program only execute when launched as root.

• The program run in the background as a daemon or service.

• The program monitor a critical zone in perpetuity. This route is indicated as an argument.

• If more than one argument is provided, these corresponds to the file extensions to be observed. Otherwise, all files are monitored.

• The program detect disk read abuse.

• The program detect intensive use of cryptographic activity.

• The program detect changes in the entropy of the files.

• The program should never exceed 100 MB of memory in use.

All alerts should be reported in the `/var/log/irondome/irondome.log` file.



May 2023

<p align="center"> <img src="https://github.com/cherrero42/BootCamp-Cybersecurity/blob/0b9187439c402644287d6f398b27825b337624e7/iron_dome/iron_dome.jpeg" /> </p>
