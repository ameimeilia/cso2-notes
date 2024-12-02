##### Space on Demand
- allocate space for the stack only when needed
- space doesn’t need to be initially empty
- only change: load form file, etc. instead of allocating empty page
- loading program can be **merely creating empty page table**
- everything else can be handled **in response to page faults**

*example*
![[Screenshot 2024-09-26 at 2.15.48 PM.png]]
1. pushq triggers exception
2. hardware wants to access address 0x7FFFBFF8
3. OS looks up what should be there: stack
4. exception handler: OS allocates more stack space
5. OS updates the page table then returns to retry the instruction
##### Extra Sharing
- sharing writable data is ok until either process modifies it
- ex. default value of global variables might not change
- use the page table to indicate to the CPI that some shared part is read-only
- processor will trigger a fault when it’s written
##### Copy-on-write and Page Tables
1. copy process duplicates page table
2. both processes share all physical pages, both are marked as read-only
3. page fault is triggered when either process tries to write to a read-only page
4. OS copies the page, creating a new physical page
5. OS reruns the write instruction
![[Screenshot 2024-09-26 at 2.42.50 PM.png]]

**`fork` with copy-on-write, if parent writes first**
![[Screenshot 2024-09-26 at 2.41.31 PM.png]]
##### `mmap`
- function to “map”/link a file to memory
```C
int file = open("somefile.dat", O_RDWR);
// data is region of memory that represents file
char *data = mmap(..., file, 0);
// read byte 6 from somefile.dat
char seventh_char = data[6];
// modify byte 100 of somefile.dat
data[100] = 'x';
// can continue to use 'data' like array
```

**Linux maps: list of maps**
- OS tracks list of `struct vm_area_struct` with:
	1. virtual address start, end
	2. permissions
	3. offset in backing file (if any)
	4. pointer to backing file (if any)

*exercise - page table lookup*
![[Screenshot 2024-09-30 at 1.38.26 AM.png]]
##### Page Tricks Generally
- deliberately **make program trigger page/protection fault**
- but **don’t assume page/protection fault is an error**
- have **separate data structures** represent logically allocated memory
- page table is for the hardware and not the OS

tricks:
	1. allocating space on demand
	2. loading code/data from files on disk on demand
	3. copy-on-write
	4. saving data temporarily to disk, reloading to memory on demand (“swapping”)
	5. detecting whether memory was read/written recently
	6. stopping in a debugger when a variable is modified
	7. sharing memory between programs on two different machines

**Hardware Help for Page Table Tricks**
- information about the address causing the fault (e.g. special register with memory address accessed)
- (by default) rerun faulting instruction when returning from exception
- precise exceptions: no side effects from faulting instruction or after (e.g. pushq that caused fault did not change %rsp before fault)
##### Page Tables in Memory
- page tables have to be encoded into memory
![[Screenshot 2024-09-26 at 3.07.18 PM.png]]

**Memory Access with Page Table**
![[Screenshot 2024-09-30 at 1.48.16 AM.png]]

*exercise*
![[Screenshot 2024-09-30 at 2.05.44 AM.png]]

