# Stockholm

_____________________________________
 Bootcamp Cybersecurity | 42 Málaga
 
 S  t  o  c  k  h  o  l  m
_____________________________________

This program encrypt files in your computer but act only on files with the extensions that were affected by Wannacry!
    [https://recursos.bps.com.es/files/796/67.pdf]
The strong key with which the files are encrypted is created with cryptography module and is at least 16 characters long 
and is save in the file [master.key].

The program has this arguments:

    • the option "--help" or "-h" to display help.
    
    • the option "–-version" or "-v" to show the version of the program.
    
    • the option "–-reverse" or "-r" followed by the key entered as an argument to reverse the infection.
    
    • the option "–-silent" or "-s" will stop any output.
    
    • the option "–-dir" or "-d" to choose the dir where the encrypted files will be saved [/infection/].
    
    • the option "–-output" or "-o" to choose the dir where the decrypted files will be saved [/infection/].
    
    • the option "–log" to produce a log file [_stockholm.log].
    
The program shows each encrypted file during the process unless option is indicated "–silent" or "-s".

The program renames all the files in the mentioned folder adding the ".ft" extension.
If they already have this extension, they will not be renamed.

Be carefull, the infection folder is in the user’s HOME directory!!

May 2023


<p align="center"> <img src="https://github.com/cherrero42/BootCamp-Cybersecurity/blob/fb6ed97dc3e25d7f6f3ab007740ab83603551deb/stockholm/stockholm.jpeg" /> </p>
