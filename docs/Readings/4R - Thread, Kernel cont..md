---
layout: default
title: Thread, Kernel cont.
parent: Readings
nav_order: 5
---
# Thread, Kernel cont.
### Thread
#### 1.1 Multitasking
- **Multitasking**: Running multiple flows of code concurrently.
- **Preemptive multitasking**:
    - Controlled by OS, hardware, or external systems.
    - Task’s access to processor/resources can be preempted (taken away) by an asynchronous event (e.g., interrupt).
- **Cooperative multitasking**:
    - Controlled by a library manually invoked by code.
    - Tasks must willingly give up control of processor/resources.
#### 1.2 Processes
- **Process**:
    - OS construct representing a running program.
    - Has private state: registers, condition codes, virtual address space, and kernel-managed resources (e.g., file descriptors).
- **Process Abstraction**:
    - Acts like a virtual machine with its own processor cores and memory.
    - OS uses kernel-only data structures to track processes.
    - Relevant process data is loaded into hardware registers and memory, enabling interaction with the correct process's memory and state.
##### 1.2.1 Virtual address spaces
- **Virtual Address Space**:
    - Represents the process’s memory.
    - Each process has its own, preventing memory interference between programs.
- **Address Translation**:
    - Hardware converts program addresses to physical hardware addresses.
    - The OS controls active address spaces by adjusting special registers.
#### 1.3 Threads
- Limited private state: mainly program registers and condition codes.
- Each thread has its own program registers and program counter.
- Threads can modify registers and program counters independently, without affecting other programs.
#### 1.4 Multi-threaded Processes
- All threads in a process share the same virtual address space and kernel-managed resources (e.g., file descriptors).
- Each thread has its own stack, managed by the `%rsp` register.
- Heap, code, and global variables are shared among all threads, as they are stored at known virtual addresses.
#### 2.1 Context Switches
- Process of changing the loaded state of a thread or process on a processor core.
- Typically occurs when handling exceptions.
#### 2.2 Preemptive multitasking
- OS schedules both processes and threads, using periodic interrupts to switch between them.
- Hardware timer generates a **timer interrupt** every few milliseconds for automated context switching.
- Creates the illusion of running more processes than available processor cores.
- OS also switches context when a program waits for input.
#### 2.3 Cooperative multitasking
- Used by some older systems (e.g., 1980s Windows/Mac OS) or modern systems for resource-constrained hardware.
- Processes voluntarily release control; otherwise, an infinite loop can freeze the system.
- Modern cooperative multitasking is often user-mode event libraries (e.g., fibers, coroutines, async/await, tasklets, etc.).
#### 2.4 Hardware multitasking
- Some processors support scheduling multiple threads on the same core using **hyperthreading** or **simultaneous multithreading**.
- This makes the core appear as multiple cores to the OS.
### Kernel
#### 2.3 Exception-Like Constructs
##### 2.3.1 Signals
- signals enable communication from kernel → user code, vs. exceptions enable communication from user code → kernel
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-10 at 5.04.49 PM.png' | relative_url}}" alt="Screenshot">
</div>

- Signals are like interrupts but for kernel-to-user communication.
- A signal can suspend the currently running code, run a signal handler (if defined), and resume the interrupted code afterward.
- If no handler is registered, the default action is taken (often terminating the process).

**Command line and signals**
- **SIGINT** (Ctrl+C): Interrupt signal that stops a running process (can be handled to do other tasks).
- **SIGTSTP** (Ctrl+Z): Suspends the process, allowing it to be resumed later (in the foreground with `fg` or background with `bg`).
- **SIGTERM**: Terminate signal sent by `kill <pid>` (where `<pid>` is the process ID), asking the process to shut down (can be handled to save work).
- **SIGKILL**: handleable kill signal (`kill -9 <pid>`), immediately terminates the process.
##### 2.3.1.1 Signal safety
- **Async-signal-safe functions**: A list of functions guaranteed to behave correctly even if a signal handler interrupts them.

*example*: signal override, custom signal handler. (`write()` is safe to use in signal handlers)
``` C
static void handler(int signum) {
    write(1, "Provide end-of-file to end program.\n", strlen("Provide end-of-file to end program.\n"));
}
```
- **Unsafe functions**: Functions like `malloc()` should not be called inside signal handlers, as they may cause corruption.
##### 2.3.1.2 Blocking signals and handling signals without signal handlers
- **Blocking signals**: Prevents signals from being handled during critical sections of code, allowing for safe execution before processing the signal

*example*: blocking `SIGINT` using `sigprocmask`
```C
sigset_t sigint_as_set;
sigemptyset(&sigint_as_set);
sigaddset(&sigint_as_set, SIGINT);
sigprocmask(SIG_BLOCK, &sigint_as_set, NULL);
... /* do stuff without signal handler running yet */
sigprocmask(SIG_UNBLOCK, &sigint_as_set, NULL);
```

- if a signal is sent to a process while it is blocked, the OS will track that it is _pending_.
- when the pending signal is unblocked, its signal handler will be run

**Handling signals without signal handlers**:
- `sigsuspend`: Temporarily unblocks a signal to handle it.
- `sigwait`: Waits for a signal and handles it by returning, rather than using a signal handler.