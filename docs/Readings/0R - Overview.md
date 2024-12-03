---
layout: default
title: Overview
parent: readings
nav_order: 1
---
# Overview
### Course Outline
#### 1 Interrupts: safe communication with hardware
- **interrupts**: incoming signal from wire → processor suspends current program and runs an interrupt handler in the OS
- used in the case of I/O devices, impossible code, code that needs to be fixed
- benefits:
	1. no need to frequently check for new input
	2. only trusted code handles I/O devices
	3. separation between peripheral drivers and user code
- interrupt handling is a subset of **exception handling** dealing with hardware
#### 2 Virtual Memory: the illusion of isolation
- **virtual memory**: tools that provide address-space separation between concurrent processes

*example* - where `translation` is an **address translation** data structure changed by the OS when changing processes
```C
movq 20(%eax), %ebx
# written in C as
`ebx = memory[20 + eax]`
# would actually be implemented as
`ebx = memory[translation[20 + eax]]`
```

- address translation requirements:
	1. a data structure that hardware can read
	2. OS/**kernel** that can modify memory regular user code cannot
	3. optimization to make it almost as efficient as direct memory access
#### 3 Networking: connecting to other computers
- **DNS** and **TCP/IP**: often used any time networked communication is undertaken
#### 4 Caching: avoiding repetitive work
- **cache**: used to increase efficiency when accessing repetitive addresses by loading a copy of memory from DRAM to SRAM
- why memory caching matters:
	1. code with good locality can be an order of magnitude faster than code with poor locality
	2. caching is becoming a way that program security can be compromised by looking for side effects of computation that remain visible in the cache
#### 5 Synchronization: concurrency requires coordination
- getting multiple concurrent actions to interact properly is complex
- how to negotiate **coordination** between concurrent threads and processes:
	1. What does it mean to wait for another agent?
	2. What happens if two agents are both waiting for the other to act first?
	3. How does all of this manifest in hardware and software?
#### 6 Processors: idle = wasteful
- **pipelining**: assembly-line decomposition of work that increases the **latency** (i.e., the number of picoseconds needed for one instruction to be completed) but also the overall **throughput** of instructions (i.e., the number of instructions completed per microsecond)
- **forwarding**: taking information from an incomplete previous instruction to execute a following instruction
- **out-of-order execution**: picking a future instruction with fewer dependencies to execute first
- **speculative execution**: picking one of the instruction sequences that *might* be next to execute when it is unclear, discarding results if wrong (ex. conditional)