---
layout: default
title: Privilege, Exceptions
parent: Notes
nav_order: 3
---
# Privilege, Exceptions
{: .highlight }
Slides: tps://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/kernel.pdf
##### Kernel Mode
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 2.08.32 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>
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
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 2.19.52 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>
##### Linux x86-64 System Calls
- before `syscall`:
	- `%rax` : system call number
	- `%rdi, %rsi, %rdx, %r10, %r8, %r9`: args
- after `syscall`
	- `%rax`: return value
	- on error → `%rax` contains -1 times “error number”

*example - Hello World*
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 2.35.01 PM.png | relative_url }}" alt="Screenshot">
</div>

**Linux System Call Examples**
1. `mmap, brk`: allocate memory
2. `fork`: create new process
3. `execve`: run a program in the current process
4. `_exit`: terminate a process
5. `open, read, write`: access files
6. `socket, accept, getpeername`: socket-related

**System Call Wrappers**
- functions with purpose to convert from a normal function call to a system call
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 2.43.34 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

*example usage*
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 2.42.02 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

**`strace hello_world`**
- Linux tool to trace system calls
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 2.44.39 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>
##### Memory Protection
**Address Space**
- programs have the illusion of their own memory → “virtual memory”
- methods of mapping:
	1. map Program B to other memory
	2. do not map Program B → segmentation fault
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 2.51.06 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

- one program cannot access another program’s memory without deliberately allowing it
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-10 at 2.18.05 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>
- Program A will always have the expected result
- Program B might crash because the OS may not map program B addresses
##### Exceptions
- hardware calls OS specified routine
	1. switch to kernel mode
	2. call OS-designated function

**Types of Exceptions**
1. system calls: intentional, kernel calls OS
2. errors/events in programs:
	- memory not in address space (segmentation faullt)
	- privileged instruction
	- divide by zero, invalid instruction

- these exceptions are *synchronous*: trigged by current program

3. external: I/O, etc.
	- timer: configured by OS to run OS at certain time
	- I/O devices: key presses, hard drives, networks
	- hardware is broken (ex. memory parity error)

- these exceptions are *asynchronous*: not triggered by running program

**General Exception Process**
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-10 at 2.21.03 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

- utilizes time multiplexing: sharing the processor’s time
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-10 at 2.22.34 PM.png | relative_url }}" alt="Screenshot" width="400">
</div>
##### Exception Patterns with I/O
**Input**
- *Case 1*: input available now
	- exception: device provides input
	- handler: OS stores input for later
	- exception (syscall): program requests input
	- handler: OS returns input
- *Case 2*: input not available now
	- exception (syscall): program requests input
	- handler: OS has no input, so OS context switches
	- exception: device provides input
	- handler: OS retrieves input
	- handler: (possibly) OS switches back to initial program that requested input

**Output**
- *Case 1*: output available now
	- exception (syscall): program produces output
	- handler: OS sends output to device
- *Case 2*: output not available now
	- exception (syscall): program produces output
	- handler: OS realizes device can’t accept output yet
	- exception: device ready for output
	- handler: OS send output
##### Threads and Processes
**Threads**
- illusion of own processor
	- own register values
	- own program counter value

**Processes**
- *process* = thread(s) + address space
- illusion of *dedicated machine*:
	- thread = illusions of own CPU
	- process could have multiple threads with independent registers
	- address space = illusion of own memory
##### Switching Programs
**Context Switching**: OS switches to another thread
1. OS starts running (some sort of exception)
2. save old registers + program counter + address mapping in individual process’s process control block (PCB)
3. sets new registers + address mapping, jump to new program counter
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-10 at 2.32.56 PM.png | relative_url }}" alt="Screenshot">
</div>
##### Exceptions vs Context Switch
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-10 at 2.59.40 PM.png | relative_url }}" alt="Screenshot">
</div>