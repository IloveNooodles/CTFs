#!/bin/bash

#
# launch
#
clear
/usr/bin/qemu-system-x86_64 \
	-m 128M \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-no-reboot \
	-cpu kvm64,+smep\
	-append "console=ttyS0 kaslr nosmap quiet panic=0"\
