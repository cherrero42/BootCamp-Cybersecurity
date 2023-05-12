# Tsunami

_____________________________________
 Bootcamp Cybersecurity | 42 Málaga
 
 T   s   u   n   a   m   i
_____________________________________


Buffer & stack overflows are a well-known technique that still cause many of the most used
vulnerabilities by attackers. With Visual C++ 6.0, we create a C program that causes a simple
buffer overflow in a Windows XP 32-bit environment.

In order to run this type of exploit, you will need a vulnerable environment.
We use Windows XP machine ready for developing from dvgamerr/win-xp-sp3
We check that this library is loaded in the system
```bash
    tasklist /m msvcrt.dll 
```

The procedure is based on two phases, the creation of the vulnerable program [code_vulnerability.c] 
and the construction of the payload that will be sent to it during execution.
Once you have created the vulnerable executable, you will build a payload that will
take advantage of the program to execute code.
After creating and verifying that the developed application is vulnerable, it is time to create an exploit that
allows to take advantage of that vulnerability.
When the vulnerable function call occurs, calls the DLL msvcrt.dll, where is the C function strcpy.
After the call strcpy occurs, the will push on stack the return address (ret address).

We put a NULL (0x00, 0) on the stack, to delimit the end of the string from cmd.exe--> "cmd.exe\00".
This can cause us problems with strcpy, if strcpy detects a 0 in a string, it stops copying the rest of the string.
Then we push "cmd.exe" on the stack (push 'c', push 'm', push 'd', push '.', etc...), and then know its address on the stack itself, to pass it to System() as an argument.
```bash
    offset kernel32.dll LoadLibraryA -> \x7C\x80\x1D\x7B
```
We need the address of the System() function in the DLL msvcrt.dll
```bash
    offset msvcrt.dll system -> \x77\xc2\x93\xc7
```

• Creation of the exploit [tsunami.c]. The program is called tsunami.exe and receive a single parameter as an argument.
• Payload creation, which will automatically open the Windows XP calculator when the vulnerability is exploited.
• The payload contains the code to be executed in shellcode.
There is an address of an instruction of a JMP ESP. EIP would take that address, execute the JMP ESP,
and "fall" where ESP points to, that we would change it to our shellcode, so it is would execute.
```bash
    kernel32.dll for code useable with the esp register: 0x7C86467B : jmp esp
```



May 2023

## Documentation

[Documentation](https://wiki.elhacker.net/bugs-y-exploits/overflows-y-shellcodes/exploits-y-stack-overflows-en-windows#TOC--Como-le-pasamos-al-programa-la-shellcode)

<p align="center"> <img src="https://github.com/cherrero42/BootCamp-Cybersecurity/blob/986cfa1465ca49f84dd0edeb9448a382820fb6a6/tsunami/tsunami.jpeg" /> </p>



