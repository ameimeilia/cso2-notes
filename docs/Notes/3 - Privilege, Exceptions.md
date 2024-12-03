##### Kernel Mode
![[Screenshot 2024-09-09 at 2.08.32 PM.png | center | 500]]
- user mode/kernel mode determined by extra one-bit register
- certain operation only allows in kernel mode, ex. talking to an I/O device
- in kernel mode, OS controls access to hardware
- enforces only trusted accesses
- user mode programs must call OS routines to access hard drive
- since OS controls access, hardware stays simpler

**What Runs in Kernel Mode?**
- system boots
- OS switches to user mode to run program code

**Controlled Entry to Kernel Mode**\
	1. user program needs OS, invokes a system call
	2. user program is interrupted, control given to OS
	3. OS runs in kernel mode at specified location (location can’t be changed without privileged instruction)
	4. OS figures out what operation the program wants and ensures it is valid
	5. complete operation and restore user saved state
![[Screenshot 2024-09-09 at 2.19.52 PM.png | center | 500]]
##### Linux x86-64 System Calls
- before `syscall`:
	- `%rax` : system call number
	- `%rdi, %rsi, %rdx, %r10, %r8, %r9`: args
- after `syscall`
	- `%rax`: return value
	- on error → `%rax` contains -1 times “error number”

*example - Hello World*
![[Screenshot 2024-09-09 at 2.35.01 PM.png]]

**Linux System Call Examples**
1. `mmap, brk`: allocate memory
2. `fork`: create new process
3. `execve`: run a program in the current process
4. `_exit`: terminate a process
5. `open, read, write`: access files
6. `socket, accept, getpeername`: socket-related

**System Call Wrappers**
- functions with purpose to convert from a normal function call to a system call
![[Screenshot 2024-09-09 at 2.43.34 PM.png | center | 500]]

*example usage*
![[Screenshot 2024-09-09 at 2.42.02 PM.png | center | 500]]

**`strace hello_world`**
- Linux tool to trace system calls
![[Screenshot 2024-09-09 at 2.44.39 PM.png | center | 500]]
##### Memory Protection
**Address Space**
- programs have the illusion of their own memory → “virtual memory”
- methods of mapping:
	1. map Program B to other memory
	2. do not map Program B → segmentation fault
![[Screenshot 2024-09-09 at 2.51.06 PM.png | center | 500]]

- one program cannot access another program’s memory without deliberately allowing it
![[Screenshot 2024-09-10 at 2.18.05 PM.png | center | 500]]
- Program A will always have the expected result
- Program B might crash because the OS may not map program B addresses
