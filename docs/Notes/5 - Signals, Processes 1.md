##### Signal API
1. `sigaction`: register handler for signal
2. `kill`: sends signal to process using process ID
3. `pause`: put process to sleep until signal received
4. `sigprocmask`: temporarily block/unblock some signals from being received, making them pending

**`kill` Command**
- calls the `kill()` function
```shell
# sends SIGTERM (terminate)to PID 1234
kill 1234
# in C: kill(1234, SIGTERM)

# sends SIGUSR1 (user 1) to PID 1234
kill -USR1 1234
# in C: kill(1234, SIGUSR1)
```

- `kill()` not always immediate
![[Screenshot 2024-09-12 at 2.28.03 PM.png | center | 500]]

*example*
![[Screenshot 2024-09-18 at 12.04.01 AM.png | center | 500]]
##### Signal Handler Unsafety
*example*
```C
void foo() {
	/* SIGINT might happen while foo() is running */
	char *p = malloc(1024);
	p[0] = 'x';
}

/* signal handler for SIGINT (registered elsewhere with sigaction()) */
void handle_signint(){
	// printf might use malloc()
	printf("You pressed control-C.\n");
}
```
![[Screenshot 2024-09-18 at 10.08.11 AM.png]]
##### Signal Handler Safety
- POSIX defines “async-signal-safe” functions
- work correctly no matter what the function interrupts
- includes: `write`, `_exit`, `kill`
- does not include: `printf`, `malloc`, `exit`

**Blocking Signals**
- avoids having signal handlers anywhere
- use `sigprocmask()` or `pthread_sigmask`
- blocked signals are not delivered and become pending

**Controlling When Signals Are Handled**
1. block a signal
2. either unblock signals at certain times
	- `sigsuspend`: temporarily changes the signal mask and waits for a signal
	- `pselect`: unblock while checking for I/O
1. and/or use API for inspecting/changing pending signals
	- `sigwait`: wait for signal to become pending, instead of having signal handler

*example*
![[Screenshot 2024-09-22 at 1.04.27 AM.png | center | 500]]
##### POSIX Process Management
essential operations:
1. `getpid`: process information
2. `fork`: process creation
3. `exec`: running programs
4. `waitpid`: waiting for processes to finish
5. `exit`, `kill`: process destruction, ‘signaling’

**`fork`**
- `pid_t fork()`: copies the current process
- returns twice:
	1. in parent (original process): PID of new child process
	2. in child (new process): 0
- **everything (but PID) duplicated** in parent, child
	- memory, file descriptors, registers
![[Screenshot 2024-09-22 at 11.23.14 AM.png | center | 500]]

*example*
![[Screenshot 2024-09-22 at 11.30.08 AM.png]]