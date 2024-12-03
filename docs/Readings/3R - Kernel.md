### 1 Kernel Mode vs. User Mode
#### 1.1 Definitions
- **Kernel Mode**: The hardware allows full access to all operations. The code running in this mode is called the **kernel**.
- **User Mode**: Some operations are restricted. User-mode software must request the kernel to perform prohibited operations.
#### 1.2 Motivation
##### 1.2.1 Limiting Bugs’ Potential for Evil
- Running software in user mode limits the impact of software bugs. If a bug occurs, it will crash the program but not affect core functionalities like screen drawing or mouse tracking.
##### 1.2.2 Each Program Thinks it is in Control
- User mode provides an illusion of unlimited resources. The kernel and hardware manage memory and processes, ensuring programs cannot see or modify each other’s memory.
##### 1.2.3 Wrapper around Hardware
- The kernel handles hardware interactions, abstracting the complexities and protocols. User programs interact with hardware indirectly through the kernel.
##### 1.2.4 Multiple Users
- The kernel manages access control for hardware resources, enabling multiple user accounts and restricting access to assigned resources.
#### 1.3 Implementation

##### 1.3.1 Protected Instructions and Memory
**User Mode Restrictions**:
- Cannot access memory storing user account information.
- Cannot execute instructions for communication with hardware (e.g., disks, networks).
- Cannot execute instructions that switch to kernel mode.
##### 1.3.2 Mode Bit
- **Mode Register**:
    - A single-bit register indicates if the chip is in user mode or kernel mode.
    - Protected instructions check this bit and cause an exception if they are not allowed in user mode.
    - A special instruction changes the mode bit, allowing kernel mode to switch to user mode but not vice versa.
- **Modern Processors**:
    - Often have multiple operating modes with various privilege levels, enhancing functionalities like virtualization.
##### 1.3.3 Mode-switch via Exceptions
**Hardware Exceptions**:
- Used to switch to kernel mode.
- Results in several changes to processor state, including jumping to kernel-only code.
- Ensures that kernel code executes for the next instruction, preventing user code from running in kernel mode.
### 2 Exceptions
#### 2.1 Kinds
##### 2.1.1 Interrupts
- **Definition**: An interrupt is an event that occurs independently of the current code execution. It may be triggered by hardware events like mouse movements or network packet arrivals.
- **Function**: Allows the operating system to respond to events even if they occur while other programs are running. The system handles the interrupt, pauses the user code, processes the interrupt, and then resumes the user code as if nothing happened.
##### 2.1.2 Faults
- **Definition**: A fault occurs when an instruction fails during execution, such as dividing by zero or accessing invalid memory.
- **Responses**:
    - **Kernel Fixes**: The kernel may address and fix the problem, allowing the user code to retry.
    - **Process Termination**: If the fault cannot be fixed, the kernel may terminate the process.
- **Example**: A page fault in virtual memory occurs when a program accesses memory not yet assigned. The kernel assigns the memory and retries the access.
- **Signals**: On Unix-like systems, faults can be communicated to the user code via signals, though many programs may not handle these signals, resulting in process termination.
##### 2.1.3 Traps
- **Definition**: A trap is an exception triggered by a special instruction designed to generate exceptions. It is used to switch from user mode to kernel mode.
- **Function**: Core mechanism for system calls, allowing user programs to access protected kernel functionality. System calls provide interfaces for interacting with the file system, managing threads, and handling other protected operations.
- **System Call Interface**: Combines user-mode hardware interfaces and system calls to define what user mode code can access.
#### 2.2 Handling
- When an exception occurs, the processor switches to kernel mode and jumps to a special function in kernel code called an exception handler
##### 2.2.1 Save-Handle-Restore
The process for handling an exception involves the following steps:
1. **Save State**: The current processor state, including the program counter and mode bit, is saved to ensure the system can resume execution after handling the exception.
2. **Enter Kernel Mode**: The processor switches from user mode to kernel mode.
3. **Execute Exception Handler**: The processor jumps to a predefined exception handler designed to address the specific exception.
4. **Restore State**: Once the exception handler has finished, the processor state is restored to what it was before the exception occurred, and execution resumes in user mode.

- These steps, except for the execution of the handler, are typically handled automatically by the hardware.
##### 2.2.2 Which Handler?
- **Exception Table**: Determines which handler to run based on the type of exception. The exception table is an array of code addresses. Each entry corresponds to a specific type of exception.
- **Exception Number**: An index into the exception table. Different exceptions are associated with different numbers (e.g., divide-by-zero might use index 0).
- format is similar to a switch statement
##### 2.2.3 After the Handler
- **Resuming Execution**:
    - **Re-run Instruction**: For faults, the handler often tries to correct the issue and then re-executes the instruction that caused the fault.
    - **Continue**: For traps, the instruction following the one that caused the trap is executed.
    - **Abort**: Some exceptions result in aborting the execution of code, such as when the issue is irrecoverable.

**Exception Classes**:
- **Fault**: The handler typically retries the instruction.
- **Trap**: Executes the instruction after the trap.
- **Interrupt**: Processes each instruction once; has no specific triggering instruction.
- **Abort**: Stops execution and does not return.

**Aborts** can occur in various situations, such as memory inconsistencies or unrecoverable errors.
##### 2.2.4 Example: Linux system calls
In Linux:
- **System Calls**: Are handled via traps, specifically with exception number 128.
- **System Call Number**: Placed in `%rax` to specify which system call to execute.

*Example with `socket` Function*:
```
socket:
    endbr64 
    mov    $0x29,%eax
    syscall 
```
- `endbr64`: Part of security measures; ensures control flow integrity.
- `mov $0x29,%eax`: Sets up the system call number (41 for `socket`).
- `syscall`: Triggers a trap, jumping to the kernel’s exception handler for number 128.

**System Call Handling**:
- The kernel’s exception handler at index 128 verifies the syscall number and then calls the appropriate handler for the specific syscall (e.g., `system_call_handler[41]` for `socket`).
- After executing, the processor state is restored, and control returns to user code.

**System Call Wrappers**:
- **User Libraries**: Provide higher-level interfaces (e.g., `malloc`, `printf`) that internally use system calls for functionality.

This layered approach ensures that user programs can interact with hardware and kernel features safely and efficiently, with minimal direct handling of low-level details.
### 3 Processes and Threads
- **process**: a software-only operating system construct that roughly parallels the end-user idea of a running program
