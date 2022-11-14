#!/bin/bash

#
# launch
#
/usr/bin/qemu-system-x86_64\
	-m 256M\
	-kernel ./bzImage\
	-initrd ./initramfs.cpio.gz \
	-nographic \
	-monitor none \
	-no-reboot \
	-cpu kvm64,+smep\
	-append "console=ttyS0 kaslr kpti nosmap quiet panic=1 oops=panic"\
	-smp 2\
