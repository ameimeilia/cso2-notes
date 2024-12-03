---
layout: default
title: Sync, Deadlock
parent: readings
nav_order: 11
---
# Sync, Deadlock
## Synchronization Primitives
### Atomic Operation
- action(s) appears to execute in a single step without interference from other actions.
- **Implementation**:
    - In single-threaded systems, the OS may disable interrupts to ensure completion
    - In multi-threaded systems, atomicity typically requires hardware support
- atomic operations are often slower and only a limited number are provided
- **Read/Modify/Write Atomic Operations**: processors typically guarantee that loading and storing pointer-sized values from memory into a register is atomic
- **Reordering and Optimizations**:
    - **Memory Reordering**: Compilers and processors may reorder instructions for efficiency, affecting shared data across threads.
    - **Preventing Optimizations**: To avoid unintended reordering, synchronization constructs are used, which prevent the compiler/processor from reordering critical sections.
### Semaphore
- controls access to a certain number or type of resources

**Types**:
1. **Counting Semaphore**: Tracks the count of available resources.
2. **Binary Semaphore**: Indicates if a resource is available (true/false).
**Main Operations**:
1. **Acquire/Wait**: Attempts to acquire a resource, decrement count; if unavailable (count = 0), suspends until available. Also known as P, wait, down, acquire, pend, or decrement.
2. **Acquire if Possible**: Attempts to acquire without blocking, returning success if available and failure if not. Often achieved through a non-blocking flag on Acquire/Wait.
3. **Release**: Increments the count, potentially reactivating waiting processes. Also known as V, signal, up, release, post, vacate, or increment.
### Mutex/Lock
- mutual exclusion, ensures exclusive access to a resource for one thread or process at a time.
- Can be implemented as a binary semaphore, with an added rule that only the acquiring thread can release it
- usually more complex to provide additional features
- **Operations**: Uses similar terminology to semaphore operations.
### Condition Variable
- not a variable in the usual sense but a tool for managing the synchronization of threads.

**Components**:
1. **Assertion**: Condition that must be true for operation to proceed (not always explicitly stored).
2. **Wait Queue**: Collection of threads waiting for the assertion to become true.
3. **Ready Queue (Optional)**: Holds threads ready to run when the assertion is true but not yet scheduled

- **Use with Mutex**: Often paired with a mutex to form a monitor, providing structured thread control.
### Monitor
- a combination of a mutex and a condition variable

**Operations**:
1. **Wait**: Suspends the thread until the condition is true, releasing the mutex.
2. **Signal/Notify**: Wakes one waiting thread, which re-acquires the mutex and resumes operation.
3. **Broadcast/NotifyAll**: Wakes all waiting threads, which then compete to re-acquire the mutex.
### Reader-writer lock
- allows shared (read-only) access or exclusive (write) access to a resource.

**Operations**:
1. **Begin Read**: Increments readers if no writers are active; otherwise, waits for writers to finish.
2. **End Read**: Decrements the reader count.
3. **Begin Write**: Waits for all readers/writers to finish before setting writer count to 1.
4. **End Write**: Resets writer count to 0.
### Barrier
- a synchronization point where processes wait until a set number of processes have arrived.

**Operation**:
1. **Arrive**: Increments a counter; if it reaches the target count, all waiting processes resume, and the counter resets, otherwise suspend the arriving process
### Transaction
- a set of operations that either all happen or none happen, ensuring consistency.
- **Implementation**:
    - Mutexes and monitors can enforce transactions, but **optimistic** approaches are common (e.g., read-copy-update).
    - **Read-Copy-Update**:
        - Snapshot values of variables, compute a result, lock access, validate snapshots, and apply or retry if values have changed.
## Deadlock
### Definition
- **Deadlock**: Occurs when a cycle of agents (threads or processes) each hold a resource while waiting for another in the cycle to release a resource.
- **Livelock**: Agents switch states without progress, often due to repeated deadlock detection and attempts to resolve it that return to deadlock.
### Necessary Conditions (Coffman Conditions)
Deadlock can occur when all of the following four conditions are present simultaneously:
1. **Mutual Exclusion**: Resources can be used by only one agent at a time.
2. **Hold-and-Wait**: Agents can hold resources while waiting for additional resources.
3. **No Preemption**: Resources cannot be forcibly taken from an agent.
4. **Circular Wait**: A cycle of agents each waiting for resources held by the next agent in the cycle.
### Detection
#### Exact Detection
- Uses a **resource allocation graph**:
	- **Agent Nodes**: Point to resources they are waiting for.
	- **Resource Nodes**: Point to agents holding them and count available instances.
- Deadlock exists if there’s a cycle in the graph.
- Resource allocation graph construction can be checked for deadlock each time a resource is allocated
#### Heuristic Detection
- Detects probable deadlock by checking if all threads are suspended waiting on resources.
- Heuristics are simpler but less precise, often used when exact detection is unavailable.
### Recovery
Once deadlock is detected, potential solutions include:
- **Resource Removal**: Remove resources from one thread, risking synchronization issues
- **Thread Rewind**: Revert a thread to a pre-resource state; requires careful bookkeeping and avoids irreversible actions
- **Thread Termination**: Forcefully kill a thread, relying on the requesting process to handle the error
### Prevention
#### 5.1 Static Approaches
- **Deadlock-Free Code**: Structuring code to avoid deadlock (e.g., Dining Philosophers solutions).
- **Specialized Language Constructs**: Some languages (e.g., Java’s `synchronized`) reduce certain deadlock risks.
- **Deadlock-Free APIs**: Message-passing APIs and lock-free structures minimize shared memory and prevent common deadlocks.
- **Compile-Time Proofs**: Research tools attempt to prove deadlock absence at compile-time, though not yet mainstream.
#### 5.2 Dynamic Approaches
- **Banker's Algorithm**:
	- **Resource Maximum**: Agents declare the maximum resources they will need upfront.
	- **Safety Check**: The system only grants resource requests that ensure other agents can eventually complete and release resources.
	- Less common in modern software due to complexity; static approaches or detect-kill-restart methods are generally preferred.