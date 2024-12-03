##### `fork`
*example - outputs depend on timing*
![[Screenshot 2024-09-22 at 2.27.27 PM.png | center | 500]]

*example - 2 processes are completely independent after fork*
![[Screenshot 2024-09-22 at 2.30.11 PM.png | center | 500]]
##### `exec`
- `exec*`: replaces current program with new program
	- `*`: multiple variants
	- same pid, new process image
- `int execv(const char *path, const char **argv`)
	- `*path`: new program to run
	- `**argv`: array of arguments, terminated by null pointer

*example*
![[Screenshot 2024-09-22 at 3.08.29 PM.png | center | 500]]

*exec in the kernel*
![[Screenshot 2024-09-22 at 3.13.10 PM.png]]