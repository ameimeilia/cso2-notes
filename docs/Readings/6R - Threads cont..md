---
layout: default
title: Threads
parent: Readings
nav_order: 6
---
# Threads
### 3 `fork` et al.
- **`fork`**: Creates a new process.
- **`waitpid`**: Removes a process.
#### 3.1 New process, what’s in memory?
- Challenge when creating a new process: determining what to put in its memory (since it has its own address space).
- **Copy memory from the parent process**: New process gets a copy of the parent's memory, which allows arbitrary setup. However, copying large amounts of memory can be inefficient.
- **Copy-on-write**:
- Adds a special bit to each page table entry.
	- When writing to a page, the memory management unit (MMU) duplicates the page only when needed.
	- Reduces unnecessary memory copying, copying only when a write occurs.
- **`fork` creates a copy of memory** from the parent, followed by a system call (e.g., `execve`) to replace the memory with new contents if needed.
#### 3.2 Using `fork`
**`fork`** is a system call wrapper that creates a new process.
- It is invoked once but returns twice: once in each process.
- **Child process**: Returns a value of `0`.
- **Parent process**: Returns the child's unique process identifier (PID).

**Fork bombing**
- denial-of-service attack where a process continually forks itself to deplete available system resources
#### 3.3 Replacing memory
- **Pattern for launching a new program**:
    1. Parent process **`fork`s** to create a child process.
    2. Child process replaces its memory with new code using **`execve`** or a similar function.

**`execve` function**:
```
#include <unistd.h>

int execve(const char *filename, char *const argv[], char *const envp[]);
```
- **`filename`**: Path to the executable binary file.
- **`argv`**: Array of argument strings passed to the new program.
    - Conventionally, `argv[0]` contains the filename.
    - Must include a **`NULL` pointer** to mark the end of the array.
- **`envp`**: Array of environment strings (in `key=value` form).
    - Must include a **`NULL` pointer** to mark the end of the array.
- **Behavior**: If no errors occur, `execve` overwrites the child process's memory with the new program's memory and starts executing the new code. It does **not return** if successful.
### 3.4 Using `waitpid`
**Common flow in a process launcher**:
1. Parent process **`fork`s**.
2. Child process replaces memory with new code (via `execve`).
3. Child process runs.
4. Child process terminates.
5. Parent process handles errors or displays information if the child crashed.

**Zombie processes**:
- When a child process terminates, it becomes a **zombie**.
- A zombie process remains in the OS process list but is not scheduled, and its memory is freed.
- The parent can **reap** the zombie process using **`waitpid`** to remove it from the process list and retrieve its exit status.

*example - fork, waitpid, and retrieving the exit status*
```C
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        printf("This is the child process\n");
        return 12;
    } else {
        printf("This is the parent process\n");
        int status;
        waitpid(pid, &status, 0);
        printf("Child exited with status code: %d\n", WEXITSTATUS(status));
        return 0;
    }
}

/* will print either
 *
 * This is the parent process
 * This is the child process
 * Child exited with status code: 12
 *
 * OR 
 *
 * This is the child process
 * This is the parent process
 * Child exited with status code: 12
 */
```
- **`status` integer**: Contains additional information about the process's termination, such as whether it was terminated by a signal, accessible through other macros like `WEXITSTATUS`.
### 4 File descriptors
- **File descriptors**: Integers used by POSIX systems to access open files.
- Each process has a table of pointers to **open file descriptions** (metadata for accessing open files).
- File descriptors index into this table.
    - **0** = standard input (`stdin`)
    - **1** = standard output (`stdout`)
    - **2** = standard error (`stderr`)
- Functions:
    - **`open()`**: Adds a file descriptor by creating a new open file description.
    - **`close()`**: Removes an entry from the table. Resources are freed when no pointers reference the open file description.
- **`fork()`**: Copies the file descriptor table, so the child process shares the same open files.
- **`execv()`**: Does not change the file descriptors.
#### 4.1 `dup2`
**`dup2(X, Y)`**: Copies file descriptor `X` onto `Y`, making both refer to the same open file description.
- Used to redirect stdin, stdout, or stderr (e.g., redirecting output to a file).


*example*
```C
#include <unistd.h>
#include <stdio.h>

int main() {
    printf("This is before open\n"); fflush(stdout);
    // fd = file descriptor of output.txt
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC);
    if (fd < 0) { printf("Error in open\n"); return 1; }
    printf("This is after open\n"); fflush(stdout);
    dup2(fd, 1); // redirects stdout to output.txt
    printf("This is after dup2\n"); fflush(stdout);
    // close fd for output.txt 
    // fd is no longer valid but stdout is still redirected through dup2()
    close(fd);
    printf("This is after close\n"); fflush(stdout);
    return 0;
}
```

will output to the terminal: 
```
This is before open
This is after open
```

and output to `output.txt`:
```
This is after dup2
This is after close
```
#### 4.2 `pipe`
- **`pipe()`**: Creates a pair of file descriptors connected to each other.
    - One is the **write end** (for writing), the other is the **read end** (for reading).
    - Data written to the write end can be read from the read end.
- **`dup2` + `pipe()`**: Enables **pipelines** like `./first | ./second`, where the output of one command becomes the input for the next.
    - Pipes have a limited buffer, so writing may block until data is read.