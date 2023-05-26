#!/bin/bash

ssh-keygen -A
/usr/sbin/sshd
tail -f /dev/null