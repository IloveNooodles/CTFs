#!/bin/bash

#
# launch
#
/usr/bin/qemu-system-x86_64 \
	-m 128M \
	-kernel ./bzImage \
	-initrd ./initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-no-reboot \
	-cpu kvm64,+smap,+smep\
	-append "console=ttyS0 kaslr kpti=1 quiet panic=0"
