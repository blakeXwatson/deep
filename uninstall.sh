#!/bin/bash
if [ ! $(whoami|grep root) ]; then sudo su; fi
unlink /bin/deep||true


