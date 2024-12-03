##### Compilers Move Loads/Stores
![[Screenshot 2024-10-24 at 2.11.26 PM.png | center | 500]]
##### `pthreads` and reordering
- many pthreads functions **prevent reordering**
	- everything before function call actually happens before
- includes **preventing some optimizations**
	- e.g. keeping global variable in register for too long

**implementations**:
1. prevent compiler reordering
2. use special instructions, ex. x86 `mfence` “memory fence” instruction
##### Definitions
- **mutual exclusion**: ensuring only one thread does a particular thing at a time
- **critical section**: code that exactly one thread can execute at a time
- **lock**: object only one thread can hold at a time
##### The Lock Primitive
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
##### `pthread mutex`
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
![[Screenshot 2024-10-24 at 2.41.30 PM.png]]
##### Deadlock Examples
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
![[Screenshot 2024-10-24 at 2.51.04 PM.png | center | 500]]

*example - deadlock with free space*
![[Screenshot 2024-10-24 at 2.53.55 PM.png | center | 500]]

**unlucky timeline**
![[Screenshot 2024-10-24 at 2.54.18 PM.png | center | 500]]
##### Deadlock
- circular waiting for **resources**
- often non-deterministic in practice
- most common example: **when acquiring multiple locks**

**requirements**
1. **mutual exclusion**
2. **hold and wait**: thread holding a resource waits to acquire another resource
3. **no preemption of resources**: resources are only released voluntarily
4. **circular wait**: there exists a set $\{T_1,…T_n\}$ of waiting threads such that $T_1$ is waiting for a resource hold by $T_2$, … $T_n$ is waiting for a resource hold by $T_1$

*exercise*
![[Screenshot 2024-10-24 at 3.09.53 PM.png]]
##### Deadlock Prevention Techniques
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