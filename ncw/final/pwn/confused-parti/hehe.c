
if(ioctl_num == 0x1771){
        if(ioctl_param >= 0 && ioctl_param <= 9){
            current_index = (int)ioctl_param;
            printk(KERN_INFO "index setted at %d\n", current_index);
        }
    }

    else if(ioctl_num == 0x1772){
           printk(KERN_INFO "size setted at 0x%lx\n", (size_t)ioctl_param);
           heap[current_index].size = (size_t)ioctl_param;
           heap[current_index].buf = (char *)kmalloc(heap[current_index].size, GFP_KERNEL);
           if(!heap[current_index].buf){
            printk(KERN_INFO "not malloced \n");
           }
           else{
            printk(KERN_INFO "malloced 0x%lx\n", heap[current_index].buf);
           }
    }

    else if(ioctl_num == 0x1774){
        printk(KERN_INFO "freeing index 0x%lx\n", heap[current_index].buf);
        kfree(heap[current_index].buf);
    }


	else if(ioctl_num == 0x7331){
		unsigned char write_buffer[256];
         	if (_copy_from_user(write_buffer, (char *)ioctl_param, 500) != 0) {
	 		printk(KERN_ALERT "WRITING ERROR!\n");
		}

}

