##### Why `fork/exec`?
- alternative: only have one function to spawn a new program:
	- Windows `CreateProcess()`; POSIX’s `posix_spawn`
- API needs to be more complicated to set new program state
- OS is simpler, doesn’t need intermediate child step
##### `wait/waitpid`
- `pid_t waitpid(pid_t pid, int * status, int options)`
- waits for a child process (with pid=`pid`) to finish
- sets `*status` to its “status information”
- `pid = -1`: wait for any child process
- `options`: `0` for no options

*example*
![[Screenshot 2024-09-22 at 3.33.00 PM.png | center | 400]]

*waitpid pattern*
![[Screenshot 2024-09-22 at 3.36.04 PM.png]]

![[Screenshot 2024-09-22 at 3.40.58 PM.png]]

*waitpid exercise*
![[Screenshot 2024-09-22 at 3.51.28 PM.png]]![[Screenshot 2024-09-22 at 4.01.04 PM.png]]
##### POSIX command-line features
- searching for programs uses the `PATH` variable → `/bin`, `/usr/bin`, `.`
	- `ls -l` → `/bin/ls -l`
	- `make` → `/usr/bin/make`
- running in background
	- `./someprogram &`
	- redirection: pass output to a file or stream
	- `./someprogram >output.txt`
	- `./someprogram <input.txt`
- pipelines: pass output to another program/utility
	- `./someprogram | ./somefilter`
##### File Descriptors
- fork copies open file list, exec preserves open files
```C
// process table
struct process_info {
	... // pid, register files, page table, ptr, etc.
	struct open_file_description *files[SIZE];
	...
};
...
process->files[file_descriptor]
```
- Unix: every process has an array of open file descriptions
- “open file”: terminal, socket, regular file, pipe
- file descriptor = int index into array
	- usually used with system calls
	- stdio.h FILE\*s usually have file descriptor + buffer

**Special File Descriptors**
- file descriptor 0 = standard input
- file descriptor 1 = standard output
- file descriptor 2 = standard error
- constants in `unistd.h`: `STDIN_FILENO`, `STDOUT_FILENO`, `STDERR_FILENO`

**`close`**
- `int close(int fd)`: returns 0 on success, -1 on error
- closes the file descriptor, deallocating the array index
- does not affect other file descriptors that point to the same object
- resources deallocated when the last file descriptor for an open file is closed
##### Redirecting with `exec`
- perform redirection after forking
![[Screenshot 2024-09-22 at 4.32.49 PM.png | center | 500]] 

*example*
redirection: `./program >output.txt`
1. open `output.txt` for writing, get new file number
2. make that new file descriptor `stdout` (FD 1) using `dup2(oldfd, newfd)`
3. exec, preserving new stdout/stdin/stderr

*example - dup2() redirects stdout to output.txt*
![[Screenshot 2024-09-22 at 8.09.46 PM.png]]
##### open/dup/close/etc. and fd array
```C
struct process_info {
	...
	struct open_file_description *files[NUM];
};
```
- open: `files[new_fd] = ...;`
- dup2(from, to): `files[to] = files[from];`
- close: `files[fd] = NULL;`
- fork: `for (int i = ...) { child->files[i] = parent->files[i]; }`
##### pipes
- `pipe()` system call allocates a buffer in the kernel that allows for read/write
![[Screenshot 2024-09-22 at 9.09.12 PM.png | center | 300]]

*example*
![[Screenshot 2024-09-22 at 9.17.21 PM.png]]

**Pipe and Pipelines**
- create pipe in parent, redirect in children
![[Screenshot 2024-09-22 at 9.29.20 PM.png]]![[Screenshot 2024-09-22 at 9.30.39 PM.png | center | 500]]
##### The Status
- status code encodes both return value and if exit was abnormal
- `W*` macros to decode it
![[Screenshot 2024-09-24 at 2.19.55 PM.png | center | 500]]
##### Open Files and File Descriptors
- when a process is forked, it inherits the parent’s file descriptors
	- preserved across exec()
	- point to the same slot in the system open file table
	- only when the last fd is closed that was associated with a particular open file, is the file actually closed
- separate calls to open have separate states
	- if parent opens file X, then child opens file X, the resulting fds are not shared

*example - unshared seek pointers*
```C
// if "foo.txt" contains "AB"
int fd1 = open("foo.txt", O_RDONLY);
int fd2 = open("foo.txt", O_RDONLY);
char c;
read(fd1, &c, 1);
char d;
read(fd2, &d, 1);
// expected result: c = 'A', d = 'A'
```

*example - shared seek pointers*
```C
// if "foo.txt" contains "AB"
int fd1 = open("foo.txt", O_RDONLY);
dup2(fd, 100);
char c;
read(fd1, &c, 1);
char d;
read(fd2, &d, 1);
// expected result: c = 'A', d = 'B'
```

*example - shared seek pointers 2*
```C
// if "foo.txt" contains "AB"
int fd1 = open("foo.txt", O_RDONLY);
pid_t p = fork();
if (p == 0) {
	char c;
	read(fd, &c, 1);
	...
} else {
	char d;
	sleep(1);
	read(fd, &d, 1);
	...
}
// expected result: c = 'A', d = 'B'
```