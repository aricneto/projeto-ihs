# Setting up intellisense for vscode

## Linking

Many includes were moved around, so we have to do some symlink magic to get vscode to identify the headers:

    #include <asm-generic/barrier.h> -> was moved to asm/..
    $ sudo ln -s asm-generic asm

    malloc.h and thread_info.h moved to include/linux
    cd /usr/src/linux-headers/../include/asm
    $ sudo ln -s linux/thread_info.h
