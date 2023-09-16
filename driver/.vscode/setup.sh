cd /usr/src/linux-headers-5.19.0-46-generic/include
sudo ln -s asm-generic asm
cd /usr/src/linux-headers-5.19.0-46-generic/include/asm
sudo ln -s ../linux/thread_info.h
sudo ln -s ../linux/processor.h
sudo ln -s ../linux/pgtable.h
sudo ln -s ../linux/elf.h
sudo ln -s ../linux/mem_encrypt.h
sudo ln -s ../linux/jump_label.h
sudo ln -s ../linux/vmalloc.h
