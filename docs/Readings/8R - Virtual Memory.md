---
layout: default
title: Virtual Memory
parent: readings
nav_order: 7
---
# Virtual Memory
### 1 Introduction
Virtual memory provides key functions for hardware and operating system collaboration:
- Gives each process the illusion it is the only one in memory.
- Creates the illusion that all possible addresses exist regardless of physical memory.
- Ensures memory protection so user-mode code cannot access kernel memory.
- Enables efficient inter-process communication.
### 2.2 Pages
Memory addresses are split into:
- **Page number** (high-order bits).
- **Page offset** (low-order bits).

- Memory access translates **virtual addresses** to **physical addresses** through:
    1. **Virtual page number** used to index the page table and retrieve a **page table entry**. (location stored in register that is changed on each context switch)
    2. **Page table entry** contains protection flags and physical page number or unmapped flag.
    3. Concatenating the physical page number and page offset forms the **physical address**.
- **Page faults** occur when an access fails (e.g., unmapped virtual pages).
- Optimizations like the **Translation Lookaside Buffer (TLB)** speed up the translation process.
#### 2.2.1 Protection… but side channels?
- Only kernel-mode code can modify page tables, and all memory accesses are guarded by them.
- **Side channels** (e.g., timing attacks) can leak information, bypassing full memory protection.
### 3 Page Tables
**Page tables** map virtual page numbers to page table entries (physical page number + flags).
#### 3.1 Single-level page tables
- Early systems with small addressable spaces used single-level page tables.
- **Page Table Base Register (PTBR)** holds the location of the page table.
- Example: A system with 16-bit virtual addresses maps virtual to physical addresses.
- **Limitations**: Single-level page tables are inefficient for 32-bit and larger address spaces.