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
![[Screenshot 2024-09-10 at 2.21.03 PM.png | center | 500]]

- utilizes time multiplexing: sharing the processor’s time
![[Screenshot 2024-09-10 at 2.22.34 PM.png | center | 400]]
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
![[Screenshot 2024-09-10 at 2.32.56 PM.png]]
##### Exceptions vs Context Switch
![[Screenshot 2024-09-10 at 2.59.40 PM.png]]
##### Signals
- Unix-like operating system feature
- similar to exceptions, but for processes
- can be triggered by external processes
	- kill command/system call
- can be triggered by special events
	- pressing ctrl+C
	- other events that would normally terminate program (seg fault, illegal instruction, /0)
- can invoke *signal handler*
![[Screenshot 2024-09-15 at 5.26.16 PM.png | center | 500]]

**Exceptions vs. Signals**

| (hardware) exceptions       | signals                         |
| --------------------------- | ------------------------------- |
| handler runs in kernel mode | handler runs in user mode       |
| hardware decides when       | OS decides when                 |
| hardware needs to save PC   | OS needs to save PC + registers |
| processor PC changes        | thread program counter changes  |
**Example Signal Program**
![[Screenshot 2024-09-15 at 5.18.19 PM.png | center | 400]]

![[Screenshot 2024-09-15 at 5.19.05 PM.png | center | 400]]

**’Forwarding’ Exception as Signal**
![[Screenshot 2024-09-10 at 3.10.34 PM.png | center | 500]]
