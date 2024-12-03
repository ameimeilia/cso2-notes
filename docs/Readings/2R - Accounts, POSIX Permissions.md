### Accounts
#### 1 Per-process permissions
- **Function Invocation**: `open("file.txt", O_RDONLY)` is a C function that sets `%rax` to a system call number and triggers the system call exception handler via the `syscall` assembly operation.
- **Exception Handler**: The operating system's exception handler, running in privileged mode, determines if the file should be opened for the process.
- **Decision Process**: The OS could make the decision arbitrarily but typically compares two structures:
	  1. Permissions of the process
	  2. Restrictions of the requested resource
- **OS Process Management**:
	  1. Tracks processor state when suspended by an exception.
	  2. Maintains the base address of the page table.
	  3. Keeps a list of open file descriptors.
	  4. Stores process-related information (e.g., process name, runtime, priority).
	  5. Often tracks the user account running the process.
#### 2 User accounts
- **Common User Account Components**:
    1. Login name (e.g., `mst3k`).
    2. Real name (e.g., `M. S. Theater`).
    3. Home directory (e.g., `/home/mst3k` for storing user preferences).
    4. Cryptographic hash of the password (passwords are hashed for security, not stored as plain text).
    5. Set of groups the user belongs to (represented as an integer and string).
- **Permissions**:
    - Permissions are typically listed per resource, not per user.
    - Resource access is controlled by specifying which users or groups may access it.
*example: `ls -l`*
```shell
-rwxr-x--- 4 mst3k coa     371 Jan 18  2019 file.txt
# '-': normal file
# 'rwx' and 'mst3k': user 'mst3k' can read, write, and execute
# 'r-x' and 'coa': group coa can read and execute
# '---': processes running under user accounts other than 'mst3k' and not belonging to group 'coa' have no permissions
# '371': file contains 371 bytes of data
# 'Jan 18 2019': file modified on this date
# 'file.txt': name of the file
```

- **File Access Based on Metadata**: The operating system checks file metadata and compares it with the user and groups of the requesting process before granting access.
- **Bypassing OS Protections**: User accounts and protections can be bypassed if physical access to the machine allows booting from alternative media, as the protections are software-based, not hardware-enforced.
- **Logged-In User Process**: Being logged in means all processes started by the user session will use the same user account in the operating system's bookkeeping.
 - **User Accounts on Android**: Android creates a different user account for each app.
#### 3 One account to rule them all
-  **`root`** or **superuser**: special account/group that bypasses normal account rules
- **Changing User Accounts**:
    - The superuser can act as any user freely.
    - Other accounts may act as different users but only after typing a password.
- **Privileges and Identity Confirmation**:
    - Similar to hardware's privileged mode, gaining higher privileges requires OS-owned software (like a password confirmation).
- **Risks of Using Administrator Accounts Directly**:
    - Running a computer from the administrator account is risky because it allows processes to bypass protections.
    - This gives processes full control over the system.
#### 4 Authentication outside the Kernel
- kernel tracks **user IDs (UIDs)** and **group IDs (GIDs)** to correctly implement system calls.
- **System call handlers** within the kernel make **authorization decisions**, determining what actions programs are permitted to perform.
- **Limited Kernel Responsibility**: The kernel does not track detailed user account information such as account names and passwords.
- **Libraries and utilities** that come with the OS manage a database of user names and passwords
- **Running as Root**:
    - Utilities that **authenticate users** (e.g., checking passwords) run as the special user **`root`**.
        - This is either because they are run by the kernel at boot.
        - Or because their executable files are marked with the `setuid` bit, indicating they should run with root privileges.
    - Since authentication utilities run as **root**, the kernel permits them to **change the user IDs** of the programs they execute.
        - This allows authenticated users to run programs under their own user IDs after successful authentication.
#### 5 Daemons
- **Daemons**:
    - Background processes that run in a manner similar to interrupt handlers.
    - Daemons sit idle in memory, only using CPU when internal, OS-moderated events (like data arriving on a socket) occur.
- **Function of Daemons**:
    - One key purpose of daemons is to provide controlled access to a different user account, typically the `root` account.
- **Printing Management**:
    - Linux systems often use **CUPS (Common UNIX Printing System)** to manage printing.
    - The **`cupsd`** daemon handles print jobs, which may involve large data being slowly sent
    - Print jobs are **spooled** into files while printing to protect their contents from other users.
    - These files are locked down to a special account, usually **`root`**, so that only **`cupsd`** (running as `root`) can access them.
- **How Printing Works**:
    - Programs send print job information to **`cupsd`**, typically via a socket.
    - Since **`cupsd`** runs as `root`, it can spool print data to a secure file owned by `root` and handle system calls restricted to the `root` account for printing.
#### 6 What is the operating system?
1. The code that resides in the privileged memory of every process and runs in privileged mode: the list of processes, exception handlers, system call code, etc.
2. All of a., plus the supplied wrapper functions like `open` and supplied headers and libraries that interface with a.
3. All of a., plus all of the processes that run as `root` and are automatically started during boot-up, plus all of the user account and file permission bookkeeping that helps provide user separation.
4. The subset of c. that was shipped together as a named system.
5. All of d., plus all the applications that came bundled with it.
6. The subset of d. that cannot be easily swapped out for other components.
### POSIX Permissions
#### 1 Users and Groups
- Every program runs as a specific **user**.
- New programs typically run as the same user as the program that started them (except in special cases, e.g., the login program running as `root`).
- To find out which user you are running as, use the `whoami` command.
- Each user has both a **name** and a **numerical ID** (the kernel uses the numerical ID).
- Users can belong to multiple **groups**.
    - To find a user's group memberships, use `groups <username>` or just `groups` for your own groups.
- Each file and directory has an **owner** and an **associated group** (only one group per file/directory).
- The owner of a file doesn't need to belong to the associated group.
#### 2 POSIX file permissions
- Permissions are divided into three types:
    - **r (read)**: Permission to read a file’s contents or list a directory’s contents.
    - **w (write)**: Permission to write to a file or add/remove items from a directory.
    - **x (execute)**: Permission to execute a file or access a directory’s contents.
- Permissions are applied to three classes of users, represented as a nine-bit number:
    - **u (owning user)**: Read/write/execute permissions for the user.
    - **g (owning group)**: Read/write/execute permissions for members of the owning group.
    - **o (others)**: Read/write/execute permissions for all other users.
- In `ls -l`, permissions are shown in letter form (e.g., `rw-rw----`):
    - `rwxrwxrwx` shows permissions for user, group, and others.
    - Example: `rw-rw----` means the user and group have read/write permissions, but others have none.
- Permissions can be modified using the **`chmod`** command:
    - Permissions can be set using octal notation or letter forms.
    - Example: `chmod 644 file` sets permissions to `rw-r--r--` (read/write for the user, read-only for others).
    - Example: `chmod ug+rw file` adds read/write permissions for the user and group.
##### 2.1 Defaults: the `umask`
- New files are created with all permissions except those blocked by the **`umask`**.
- The **`umask`** command shows the default permissions that are omitted from new files.
    - Example: `umask 0022` on department machines results in new files with `0755` permissions.
    - To see symbolic representation: use `umask -S` (e.g., `u=rwx,g=rx,o=rx`).
##### 2.2 setuid, setgid, and sticky
- POSIX systems have three additional file permission bits: **setuid**, **setgid**, and **sticky**. These are generally **not recommended** for use due to security risks.
##### `setuid`
- **Executable file**: Runs the file as the file owner instead of the user executing it.
    - Example: If `xyxxy` is owned by `mst3k` and has setuid, when `tj1a` runs it, it executes as `mst3k`.
    - Used in programs like `sudo`, but it can be dangerous as it may expose security vulnerabilities.
##### `setgid`
- **Executable file**: Works like setuid but applies to the **group** instead of the user.
    - Potential security risks make this unsafe unless absolutely necessary.
- **Directory**: New files in the directory inherit the directory’s group instead of the creator’s group.
    - This can be a security vulnerability unless used with caution.
##### `sticky`
- **Directory**: Files can only be removed/renamed by the file owner or directory owner (except for `root`).
    - Sometimes useful to set on directories.
- When using a four-digit octal with **`chmod`**, these permission bits are represented by the first digit (e.g., sticky may be useful; setuid/setgid should generally be avoided).
#### 3 Access Control Lists
- **Access Control Lists (ACLs)** provide more granular permissions than the traditional user-group-other distinction.
- ACLs are lists of user-permission pairs for each file, allowing multiple users or groups with different permissions.
- **Commands:**
    - `getfacl file`: Displays the full permission information for a file.
    - `setfacl`: Modifies or creates ACL entries for a file's permission list.
    - **Examples:**
		- `setfacl -m u:mst3k:rx`: Modifies user `mst3k`’s permissions to be `r` (read) and `x` (execute).
		- `setfacl -m g:lab_fall2019:r`: Modifies group `lab_fall2019`’s permissions to be `r` only (read).
		- `setfacl -x u:mst3k`: Removes user `mst3k` from the permission list.
- ACLs are a safe and flexible method when finer permission control is needed, although they are not commonly used.
#### 4 Executable text files
A file is executable in POSIX systems if:
1. It is an **executable binary** (e.g., ELF file), which can be loaded into memory and run.
2. It is a plain text file that contains a **shebang line**, which tells the system which interpreter to use for the file.
	- **Shebang**: A line starting with `#!/path/to/program` (e.g., `#!/bin/bash`), which makes the system execute the file using the specified interpreter.
	- Example: A file `gloop.sh` starting with `#!/bin/bash` can be executed by running `./gloop.sh`, equivalent to running `/bin/bash ./gloop.sh`.

- **quine**:program that displays its own contents
*examples*
```
#!/bin/cat
```

```
#!/bin/cat
Quines are interesting to create in many languages.
But if you use shebangs, they are trivial to create
using the interpreter "cat."
```