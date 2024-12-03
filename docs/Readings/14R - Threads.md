---
layout: default
title: Threads
parent: Readings
nav_order: 10
---
# Threads
### Managing Thread Existence
- every process has at least one thread, the main thread
- each other thread is created by invoking a system call
#### `pthread_create`
 - creates a new thread using the following arguments:
![[Screenshot 2024-10-27 at 8.31.39 PM.png]]
##### `pthread_attr_t`
- usually just passing `NULL` is ok
- **Thread Attributes**: Controls thread behavior, requiring:
    - **Initialization**: `pthread_attr_init` to set up, `pthread_attr_destroy` to free resources afterward.
    - **Attributes to Set**: Priority, stack size, and detach state (joinable vs. detached).
*example - skeleton to create a thread*
```C
pthread_attr_t attr;
pthread_attr_init(&attr);
pthread_t id;
void *argument = /* ... initialize this here */
/* ... use various pthread_attr_setXXXX functions to set behavior ... */
pthread_create(&id, &attr, run_this, argument);
pthread_attr_destroy(&attr);
```
#### `pthread_attr_setdetachstate` and `pthread_join`
Every created thread is either joinable or detached:
1. `pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE)`
	- default attribute
	- thread will continue to exist after exiting until `pthread_join` is called
	- joinable threads **must** be joined before exiting

2. `pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED)`
	- OS reclaims resources immediately upon thread termination
	- exit status is lost, `pthread_join` cannot be used by other threads
	- detached threads can’t be waiting for, so when the main thread exits any detached threads will terminate

**Using `pthread_join(id, &retval)`**:
- invoking thread waits until the thread `id` terminates and stores the result in `&retval`
- possible values of result:
	1. return value of the start function of the terminated thread
	2. argument passed into `pthread_exit` to terminate the thread early
	3. special value `PTHREAD_CANCELED` if the thread was stopped by another thread
#### Crashing
- a crash in any thread due to an unhandled signal terminates the entire program
- signals are delivered to specific threads, so any signal handlers will be run by the thread the OS believes is the recipient of the signal
### Synchronization with pthreads
#### Mutex
- only allows one thread to hold the lock at a time, ensuring exclusive access
```C
pthread_mutex_t mutex;    // declare a mutex variable

void *thread_function(void *) {
    /* ... */
    pthread_mutex_lock(&mutex);
    /* only one thread can get here at a time */
    pthread_mutex_unlock(&mutex);
    /* ... */
}

int main(int argc, const char *argv[]) {
    /* ... */
    pthread_mutex_init(&mutex, NULL);    // initialize the mutex
    for(int i=0; i<THREADCOUNT; i+=1) {
        /* ... */
        pthread_create(&id[i], NULL, thread_function, &arg[i]);
    }
    /* ... */
}
```

**Additional Functionality**:
- `pthread_mutex_trylock`: Attempts to acquire the lock without waiting if it’s unavailable.
- `pthread_mutex_destroy`: free resources allocated by `init`
#### On Sharing Mutexes (and other synchronization objects)
- shared mutex objects are modified directly using pointers
- mutexes can be shared via global variables or passing pointers
```C
typedef struct {
    pthread_mutex_t *ptr_to_mutex;
    ...
} task_description;

void *thread_function(void *args) {
    task_description *task = (task_description *)args;
    /* ... */
    pthread_mutex_lock(args->ptr_to_mutex);
    /* only one thread can get here at a time */
    pthread_mutex_unlock(args->ptr_to_mutex);
    /* ... */
}

int main(int argc, const char *argv[]) {
    pthread_mutex_t mutex;
    task_description tasks[THREADCOUNT];
    /* ... */
    pthread_mutex_init(&mutex, NULL);
    for(int i=0; i<THREADCOUNT; i+=1) {
        tasks[i].ptr_to_mutex = &mutex;
        /* ... */
        pthread_create(&id[i], NULL, thread_function, tasks+i);
    }
    /* ... */
}
```
#### Barrier
- acts as a synchronization point, allowing threads to wait until all have reached a specific point
- barrier objects must be shared between threads, like mutexes
```C
pthread_barrier_t barrier;

void *thread_function(void *) {
    /* ... */
    /* each thread reaches here at its own time */
    pthread_barrier_wait(&barrier);    // wait until all arrived to proceed
    /* all threads proceed from here together */
    /* ... */
}

int main(int argc, const char *argv[]) {
    /* ... */
    // initialize, specify number of threads required to meet
    pthread_barrier_init(&barrier, NULL, THREADCOUNT);
    for(int i=0; i<THREADCOUNT; i+=1) {
        /* ... */
        pthread_create(&id[i], NULL, thread_function, &arg[i]);
    }
    // clean up with pthread_barrier_destroy
    /* ... */
}
```
#### Reader-writer lock
- allows either multiple readers (unsynchronized data) or a single writer (ex. mutex), but not both simultaneously

**Functions**:
- **Initialization**: `pthread_rwlock_init`, has many attributes
- **Locking**:
	- `pthread_rwlock_rdlock` for readers
	- `pthread_rwlock_wrlock` for writers
- **Timed Lock**: `pthread_rwlock_timedrdlock` and `pthread_rwlock_timedwrlock`, which wait up to a specified time.
- **Unlocking**: `pthread_rwlock_unlock` to release any type of lock
- **Destruction**: `pthread_rwlock_destroy` to free any allocated resources
#### Monitors
- uses condition variables with a mutex to create a monitor, allowing threads to wait for specific conditions

**Functions**:
- **`pthread_cond_init`**: create a condition variable.
- **`pthread_cond_wait`**: atomically unlocks the mutex and places the thread in a wait queue; locks the mutex again once woken.
- **`pthread_cond_timedwait`**: Like `pthread_cond_wait`, but stops waiting after a specified time.
- **`pthread_cond_destroy`**: free any allocated resources