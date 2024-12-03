---
layout: default
title: Synchronization, Deadlock
parent: Notes
nav_order: 9
---
# Synchronization, Deadlock
{: .highlight }
Slides: [sync](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/sync.pdf), [deadlock](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/deadlock.pdf)
## Atomic Operation
- operation that runs to completion or not at all
- most machines: loading/storing (aligned) values is atomic:
	- ex. can’t get x = 3 from x ← 1 and x ← 2 running in parallel
	- aligned = address of word is multiple of word size
- some instructions are not atomic, ex:
	- x86: integer `add` constant to memory location
	- many CPUs: loading/storing values that cross cache blocks

**What is actually atomic?**
- assume load/stores of ‘words’
- processor designer will specify what is atomic
- if not specified, not assume atomic
## Thinking about Race Conditions
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-27 at 6.28.46 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**Lost `add`**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-27 at 6.36.55 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-27 at 6.38.24 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
- occurs on multiple cores since `add` is implemented with multiple steps (load, add, store internally)
- can be interleaved with what other cores do
## Compilers Move Loads/Stores
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-24 at 2.11.26 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## `pthreads` and reordering
- many pthreads functions **prevent reordering**
	- everything before function call actually happens before
- includes **preventing some optimizations**
	- e.g. keeping global variable in register for too long

**implementations**:
1. prevent compiler reordering
2. use special instructions, ex. x86 `mfence` “memory fence” instruction
## Definitions
- **mutual exclusion**: ensuring only one thread does a particular thing at a time
- **critical section**: code that exactly one thread can execute at a time
- **lock**: object only one thread can hold at a time
## The Lock Primitive
- locks: an object with (at least) two operations:
	1. *acquire* or *lock*: **wait** until lock is free, then “grab” it
	2. *release* or *unlock*: let others use lock
- typical usage: everyone acquires lock before using shared resource
- ideal wait: not using processor, OS can context switch to other programs

*example*

```C
Lock(account_lock);
balance += ...;
Unlock(account_lock);
```

## `pthread mutex`
- rule: unlock from same thread you lock in

```C
#include <pthread.h>

pthread_mutex_t account_lock;
pthread_mutex_init(&account_lock, NULL);
// or: pthread_mutex_t account_lock = PTHREAD_MUTEX_INITIALIZER; 
pthread_mutex_lock(&account_lock);
balance += ...;
pthread_mutex_unlock(&account_lock);
```

*exercise*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-24 at 2.41.30 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Deadlock Examples
*example - moving two files*
- Thread 1: MoveFile(A, B, “foo”)
- Thread 2: MoveFile(B, A, “bar”)

```C
struct Dir { 
	mutex_t lock; HashMap entries; 
};
void MoveFile(Dir *from_dir, Dir *to_dir, string filename) { 
	mutex_lock(&from_dir−>lock); 
	mutex_lock(&to_dir−>lock); 
	
	Map_put(to_dir−>entries, filename, Map_get(from_dir−>entries, filename)); 
	Map_erase(from_dir−>entries, filename); 
	
	mutex_unlock(&to_dir−>lock); 
	mutex_unlock(&from_dir−>lock); 
}
```

**unlucky timeline**
- Thread 1 holds A lock, waiting for Thread 2 to release B lock
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-24 at 2.51.04 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

*example - deadlock with free space*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-24 at 2.53.55 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**unlucky timeline**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-24 at 2.54.18 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Deadlock
- circular waiting for **resources**
- often non-deterministic in practice
- most common example: **when acquiring multiple locks**

**requirements**
1. **mutual exclusion**
2. **hold and wait**: thread holding a resource waits to acquire another resource
3. **no preemption of resources**: resources are only released voluntarily
4. **circular wait**: there exists a set $\{T_1,…T_n\}$ of waiting threads such that $T_1$ is waiting for a resource hold by $T_2$, … $T_n$ is waiting for a resource hold by $T_1$

*exercise*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-24 at 3.09.53 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Deadlock Prevention Techniques
1. **infinite resources**: no mutual exclusion
2. **no shared resources**: no mutual exclusion
3. **no waiting**: no hold and wait/preemption
	- “busy signal,” abort and retry revoke/preempt resources
4. acquire resources in **consistent order**: no circular wait
5. request **all resources at once**: no hold and wait

**Acquiring Locks in Consistent Order**

```C
MoveFile(Dir* from_dir, Dir* to_dir, string filename) {
	if (from_dir−>path < to_dir−>path) { 
		lock(&from_dir−>lock); 
		lock(&to_dir−>lock);
	} else {
		lock(&to_dir−>lock);
		lock(&from_dir−>lock);
	}
	...
}
```

## Barriers
- wait for all computations to finish

```C
barrier.Initialize(NumberOfThreads)
barrier.Wait()    // return after all threads have waited
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 10.42.18 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

- useful for reuse structure in simulations
*example - reuse with barriers*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.10.59 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**`pthread` barriers**

```C
pthread_barrier_t barrier;
pthread_barrier_init(
	&barrier,
	NULL /* attributes */,
	numberOfThreads
);
... 
... 
pthread_barrier_wait(&barrier);
```

*exercise - pthreads barriers*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.18.32 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Monitors/Condition Variables
- **locks** for mutual exclusion
- **condition variables** for waiting for event
	- represents **list of waiting threads**
	- operations: wait (for event); signal/broadcast (that event happened)
- **monitor** = lock + 0 or more condition variables + shared data
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.26.50 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**`condvar` operations**
`Wait(cv, lock)`: **unlock** lock, add current thread to cv queue, and **reacquire** lock before returning
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.29.23 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.30.15 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

`Broadcast(cv)`: remove all from cv queue
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.30.37 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

`Signal(cv)`: remove one from cv queue
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.31.00 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## `pthread` cv usage
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.00.36 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**WaitForFinish Timeline 1**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.02.17 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**WaitForFinish Timeline 2**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.05.56 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**Why Use a `while` loop?**

```C
while (!finished) {
	pthread_cond_Wait(&finished_cv, &lock);
}
```

- `pthread_cond_wait` might have “spurious wakeups”: when `wait` returns even though nothing happened

## Hoare vs Mesa Monitors
- **Hoare-style Monitors**: the signal “hands off” the lock to the awoken thread
- **Mesa-style Monitors**: any eligible thread gets the lock next
- current threading libraries use Mesa-style
- another reason why the `while` loop is necessary

## Producer/Consumer
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-29 at 2.38.47 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>
- shared buffer (queue) of fixed size
- one or more producers insert into queue, one or more consumers remove from queue
- producers/consumers don’t work in lockstep

**Unbounded Buffer Producer/Consumer**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.16.57 PM.png' | relative_url}}" alt="Screenshot" width="550">
</div>

*0 Iterations of Loop*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.22.32 PM.png' | relative_url}}" alt="Screenshot" width="550">
</div>

*1 Iteration of Loop*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.26.38 PM.png' | relative_url}}" alt="Screenshot" width="550">
</div>

*2+ Iterations of Loop: Spurious Wakeup or 3+ Threads, shows Mesa-style*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.30.54 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Bounded Buffer Producer/Consumer**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.41.52 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Monitor Pattern

```C
pthread_mutex_t mutex;
pthread_cond_t cv;
pthread_mutex_init(&mutex, NULL);
pthread_cond_init(&cv, NULL);
// --OR--
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cv = PTHREAD_COND_INITIALIZER;

pthread_mutex_lock(&lock);
while (!condition A) { 
	pthread_cond_wait(&condvar_for_A, &lock); 
} 
... /* manipulate shared data, changing other conditions */ 
if (set condition A) { 
	pthread_cond_broadcast(&condvar_for_A); 
	/* or signal, if only one thread cares */ 
}
if (set condition B) { 
	pthread_cond_broadcast(&condvar_for_B); 
	/* or signal, if only one thread cares */ 
} 
... 
pthread_mutex_unlock(&lock)

// when done:
...
pthread_cond_destroy(&cv);
pthread_mutex_destroy(&mutex);
```

 **Monitors Rules of Thumb**
 - never touch shared data without holding the lock
 - keep lock held for **entire operation**
 - create `condvar` for every kind of scenario waited for
 - always write **loop** calling `cond_wait` to wait for condition X
 - broadcast/signal condition variable **every time you change X**

*exercise: wait for both finished*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.55.23 PM.png' | relative_url}}" alt="Screenshot" width="550">
</div>

*exercise: one-use barrier*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-05 at 11.58.00 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Generalizing Locks: Semaphores
- has a non-negative integer **value** and two operations:
	1. **P()** or **down** or **wait**: wait for semaphore to become positive (>0), then decrement by 1
	2. **V()** or **up** or **signal** or **post**: increment semaphore by 1 (waking up thread if needed)
- **cannot read/write directly**: down/up operation is the only way to access (besides initialization)
- **never negative**: wait instead

*example - reserving books*

```C
Semaphore free_copies = Semaphore(3)
void ReserveBook() {
	// wait for copy to be free
	free_copies.down();
	... // ... then take reserved copy
}

void ReturnBook() {
	... // return reserved copy
	free_copies.up();
	// ... then wake up waiting thread
}
```

## Modifying Cache Blocks in Parallel
- typically caches only allow modifications to different parts of one cache block to happen one at a time:
	1. processor “locks” 64-bytes cache block, fetching latest version
	2. processor updates 4 bytes of 64-byte cache block
	3. later, processor might give up cache block
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-06 at 12.06.57 AM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**Performance vs Array Element Gap**
- above 64 bytes, the two cache blocks are different, so there is no interference
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-06 at 12.07.18 AM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## False Sharing
- two things that are actually independent but accesses get synchronized
- solution: separate them

*exercise - where is false sharing likely to occur?*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-06 at 12.12.30 AM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Transactions
- set of operations that occur atomically
- idea:
	- something higher-level handles locking
	- library/database/etc. makes “transaction” happen all at once

```C
BeginTransaction();
int FromOldBalance = GetBalance(FromAccount);
int ToOldBalance = GetBalance(ToAccount); 
SetBalance(FromAccount, FromOldBalance - 100); 
SetBalance(ToAccount, FromOldBalance + 100);
EndTransaction();
```

- **Consistency**: locking to make sure no other operations interfere
- **Durability**: making sure on crash, no partial transaction occurs

## Implementing Consistency
**Simple**
- only run one transaction at a time
- only one lock that each transaction holds for the duration of the transaction

**Locking**
- have locks for each individual thing
- acquire locks as we read/write, then release the locks at the end of the transaction
- if deadlock: **undo everything**, go back to `BeginTransaction()`, retry
	- possible solution: keep list of writes instead of writing, apply writes only at `EndTransaction()`

**Optimistic**
- on read: copy version # for value read
- on write: record value to be written, but don’t write yet
- on end transaction:
	- acquire locks on everything
	- make sure values read haven’t been changed since read
- if they have changed (different version #), retry transaction