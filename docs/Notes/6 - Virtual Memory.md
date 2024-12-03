---
layout: default
title: Virtual Memory
parent: Notes
nav_order: 6
---
# Virtual Memory
{: .highlight }
Slides: [vm](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/vm.pdf)
## Address Translation
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-24 at 3.00.13 PM.png' | relative_url}}" alt="Screenshot" width="600">
</div>
## Toy Program Memory
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-24 at 2.37.07 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-24 at 2.41.58 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## Toy Page Table Lookup
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-24 at 2.47.04 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## Virtual Address Sizes
- virtual address sizes are not always the size of pointers, sometimes part of the pointer is not used
- virtual address size is amount actually used for mapping
## Address Space Size
- amount that can be addressed, based on number of unique addresses
- eg. 32-bit virtual address = $2^{32}$ byte virtual address space
- eg. 20-bit physical address = $2^{20}$ byte physical address space

*exercise - page table size*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-29 at 11.27.33 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

*exercise - page table lookup*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-24 at 3.29.25 PM.png' | relative_url}}" alt="Screenshot">
</div>
## Permission Bits
- additional bits in page table entry that define:
	- user mode access
	- read, write, execute permissions
- checked by hardware, like the valid bit
## Space on Demand
- allocate space for the stack only when needed
- space doesn’t need to be initially empty
- only change: load form file, etc. instead of allocating empty page
- loading program can be **merely creating empty page table**
- everything else can be handled **in response to page faults**

*example*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-26 at 2.15.48 PM.png' | relative_url}}" alt="Screenshot">
</div>
1. pushq triggers exception
2. hardware wants to access address 0x7FFFBFF8
3. OS looks up what should be there: stack
4. exception handler: OS allocates more stack space
5. OS updates the page table then returns to retry the instruction
## Extra Sharing
- sharing writable data is ok until either process modifies it
- ex. default value of global variables might not change
- use the page table to indicate to the CPI that some shared part is read-only
- processor will trigger a fault when it’s written
## Copy-on-write and Page Tables
1. copy process duplicates page table
2. both processes share all physical pages, both are marked as read-only
3. page fault is triggered when either process tries to write to a read-only page
4. OS copies the page, creating a new physical page
5. OS reruns the write instruction
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-26 at 2.42.50 PM.png' | relative_url}}" alt="Screenshot">
</div>

**`fork` with copy-on-write, if parent writes first**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-26 at 2.41.31 PM.png' | relative_url}}" alt="Screenshot">
</div>

## `mmap`
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
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-30 at 1.38.26 AM.png' | relative_url}}" alt="Screenshot">
</div>
## Page Tricks Generally
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
## Page Tables in Memory
- page tables have to be encoded into memory
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-26 at 3.07.18 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Memory Access with Page Table**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-30 at 1.48.16 AM.png' | relative_url}}" alt="Screenshot">
</div>

*exercise*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-30 at 2.05.44 AM.png' | relative_url}}" alt="Screenshot">
</div>

*example - pagetable lookup*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-01 at 2.10.26 PM.png' | relative_url}}" alt="Screenshot">
</div>

## `translate()`
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-05 at 5.46.22 PM.png' | relative_url}}" alt="Screenshot">
</div>

## `page_allocate()`
- allocates a page table with a valid entry for arg, then make all other entries invalid
- if the page table is already allocated, simply add the valid entry

## `posix_memalign`

```C
void *result;
error_code = posix_memalign(&result, alingment, size);
```
- allocates `size` bytes
- chooses address that is multiple of `alignment`
- `error_code` indicates if out-of-memory, etc.
- fills in `result`

## Two-level Page Tables
- lookup implemented in hardware → must be simple → split up address bits
- should not involve many memory accesses → tree with many children from each node

## Two-level Page Table Lookup
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-01 at 3.56.36 PM.png' | relative_url}}" alt="Screenshot">
</div>

*another view*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-01 at 3.56.51 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Multi-level Page Tables
- VPN split into pieces for each level of page table
- top levels: page table entries point to next page table
- bottom level: page table entry points to destination page
- validity checks at *each level*

## 2-level Splitting
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-01 at 3.49.28 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

*example - 2 level page table lookups*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-01 at 3.08.58 PM.png' | relative_url}}" alt="Screenshot">
</div>

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-01 at 3.42.38 PM.png' | relative_url}}" alt="Screenshot">
</div>

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 2.17.04 PM.png' | relative_url}}" alt="Screenshot">
</div>



