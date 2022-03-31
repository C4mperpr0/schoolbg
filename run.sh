#!/bin/sh

sshpass -p advgauss ssh root@192.168.103.135 'systemctl suspend'

#scp -r imgs/ root@192.168.103.135:/home/stollj01/Downloads

export SSHPASS=ry3AvbWO0oupYX9HCMzp0Axx

sshpass -e scp testfile.csv user@example.com:/uploads/
