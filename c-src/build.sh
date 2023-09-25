#!/bin/bash
rm main.exe

CFLAGS="-Wall -Wextra -pedantic"
# CFLAGS+=" -Werror"

# debug flag
CFLAGS+=" -DDEBUG"

gcc -o main.exe main.c $CFLAGS
