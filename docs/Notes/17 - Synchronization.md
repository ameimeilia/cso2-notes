##### Barriers
- wait for all computations to finish
```C
barrier.Initialize(NumberOfThreads)
barrier.Wait()    // return after all threads have waited
```
![[Screenshot 2024-11-05 at 10.42.18 PM.png | center | 400]]

- useful for reuse structure in simulations
*example - reuse with barriers*
![[Screenshot 2024-10-29 at 2.10.59 PM.png | center | 500]]

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
![[Screenshot 2024-10-29 at 2.18.32 PM.png | center | 500]]
##### Monitors/Condition Variables
- **locks** for mutual exclusion
- **condition variables** for waiting for event
	- represents **list of waiting threads**
	- operations: wait (for event); signal/broadcast (that event happened)
- **monitor** = lock + 0 or more condition variables + shared data
![[Screenshot 2024-10-29 at 2.26.50 PM.png | center | 500]]

**`condvar` operations**
`Wait(cv, lock)`: **unlock** lock, add current thread to cv queue, and **reacquire** lock before returning
![[Screenshot 2024-10-29 at 2.29.23 PM.png | center | 500]]
![[Screenshot 2024-10-29 at 2.30.15 PM.png | center | 500]]

`Broadcast(cv)`: remove all from cv queue
![[Screenshot 2024-10-29 at 2.30.37 PM.png | center | 500]]

`Signal(cv)`: remove one from cv queue
![[Screenshot 2024-10-29 at 2.31.00 PM.png | center | 500]]
##### `pthread` cv usage
![[Screenshot 2024-11-05 at 11.00.36 PM.png | center | 500]]

**WaitForFinish Timeline 1**
![[Screenshot 2024-11-05 at 11.02.17 PM.png | center | 500]]

**WaitForFinish Timeline 2**
![[Screenshot 2024-11-05 at 11.05.56 PM.png | center | 500]]

**Why Use a `while` loop?**
```C
while (!finished) {
	pthread_cond_Wait(&finished_cv, &lock);
}
```
- `pthread_cond_wait` might have “spurious wakeups”: when `wait` returns even though nothing happened
##### Hoare vs Mesa Monitors
- **Hoare-style Monitors**: the signal “hands off” the lock to the awoken thread
- **Mesa-style Monitors**: any eligible thread gets the lock next
- current threading libraries use Mesa-style
- another reason why the `while` loop is necessary
##### Producer/Consumer
![[Screenshot 2024-10-29 at 2.38.47 PM.png | center | 400]]
- shared buffer (queue) of fixed size
- one or more producers insert into queue, one or more consumers remove from queue
- producers/consumers don’t work in lockstep

**Unbounded Buffer Producer/Consumer**
![[Screenshot 2024-11-05 at 11.16.57 PM.png | center | 550]]

*0 Iterations of Loop*
![[Screenshot 2024-11-05 at 11.22.32 PM.png | center | 550]]

*1 Iteration of Loop*
![[Screenshot 2024-11-05 at 11.26.38 PM.png | center | 550]]

*2+ Iterations of Loop: Spurious Wakeup or 3+ Threads, shows Mesa-style*
![[Screenshot 2024-11-05 at 11.30.54 PM.png]]

**Bounded Buffer Producer/Consumer**
![[Screenshot 2024-11-05 at 11.41.52 PM.png]]
##### Monitor Pattern
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
![[Screenshot 2024-11-05 at 11.55.23 PM.png | center | 550]]

*exercise: one-use barrier*
![[Screenshot 2024-11-05 at 11.58.00 PM.png | center | 500]]
##### Generalizing Locks: Semaphores
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
##### Modifying Cache Blocks in Parallel
- typically caches only allow modifications to different parts of one cache block to happen one at a time:
	1. processor “locks” 64-bytes cache block, fetching latest version
	2. processor updates 4 bytes of 64-byte cache block
	3. later, processor might give up cache block
![[Screenshot 2024-11-06 at 12.06.57 AM.png | center | 500]]

**Performance vs Array Element Gap**
- above 64 bytes, the two cache blocks are different, so there is no interference
![[Screenshot 2024-11-06 at 12.07.18 AM.png | center | 500]]
##### False Sharing
- two things that are actually independent but accesses get synchronized
- solution: separate them

*exercise - where is false sharing likely to occur?*
![[Screenshot 2024-11-06 at 12.12.30 AM.png | center | 500]]