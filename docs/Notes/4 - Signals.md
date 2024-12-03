---
layout: default
title: Signals
parent: Notes
nav_order: 4
---
# Signals

{: .highlight }
> Slides: [signals](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/signals.pdf)

## Signals
- Unix-like operating system feature
- similar to exceptions, but for processes
- can be triggered by external processes
	- kill command/system call
- can be triggered by special events
	- pressing ctrl+C
	- other events that would normally terminate program (seg fault, illegal instruction, /0)
- can invoke *signal handler*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-15 at 5.26.16 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**Exceptions vs. Signals**

| (hardware) exceptions       | signals                         |
| --------------------------- | ------------------------------- |
| handler runs in kernel mode | handler runs in user mode       |
| hardware decides when       | OS decides when                 |
| hardware needs to save PC   | OS needs to save PC + registers |
| processor PC changes        | thread program counter changes  |
**Example Signal Program**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-15 at 5.18.19 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-15 at 5.19.05 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

**’Forwarding’ Exception as Signal**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-10 at 3.10.34 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## Signal API
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
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-12 at 2.28.03 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

*example*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-18 at 12.04.01 AM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## Signal Handler Unsafety
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
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-18 at 10.08.11 AM.png' | relative_url}}" alt="Screenshot">
</div>
## Signal Handler Safety
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
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-09-22 at 1.04.27 AM.png' | relative_url}}" alt="Screenshot" width="500">
</div>