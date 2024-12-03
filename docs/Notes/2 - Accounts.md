---
layout: default
title: Accounts
parent: Notes
nav_order: 2
---
# Accounts
> [!note]
> Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/accounts.pdf
##### POSIX User IDs and Groups
**User IDs**
- every process has a user ID that is used to decide what the process is authorized to do
- `uid_t geteuid();` gets the current process’s “effective” user ID, used for all permission checks
- effective user ID is a unique number that the kernel knows

**Groups**
``` shell
gid_t getegid(void);   # process's "effective" group ID

int getgroups(int size, gid_t list[])   # process's extra group IDs
```

##### POSIX File Permissions and Encoding
- POSIX files have a very restricted access control list:
	1. one user ID: read/write/execute bits for user, “owner” that can also change permissions
	2. one group ID: read/write/execute bits for group
	3. default setting: read/write/execute

**Encoding**
- permissions encoded as 9-bit number, can write as octal: XYZ
- octal divided in 3-bit parts: user permissions (X), group permissions (Y), other permission (Z)
- each 3-bit part has a bit for ‘read’ (4), ‘write’ (2), ‘execute’ (1)
- for directories: read = `ls`, write = add and remove files, execute = `cd`

*example*
```
700 -> 111, 000, 000: user can rwx, group none, other none
451 -> 100, 101, 001: user can r, group can rx, other x
```

**Setting Permissions**
```shell
chmod 700 file

# or

chmod u=rwx, og=  file
```

**Adding Permissions**
```shell
# add user read and execute
chmod u+rx foo

# remove other read, write execute; set user to read and execute
chmod o-rwx, u=rx foo
```

##### POSIX/NTFS ACLs
- more flexible access control lists

**POSIX ACL Syntax**
- can specify multiple users and multiple groups
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 11.05.14 AM.png | relative_url }}" alt="Screenshot" width="500">
</div>

**POSIX ACLs on command line**
```shell
# would see something similar to example above
getfacl file

# add line to ACL, tj1a given no access
setfacl -m 'user:tj1a:---' file

# remove line from ACL
setfacl -x 'user:tj1a' file

# add to ACL, but read what to add from a file
setfacl -M acl.txt file

# remove from ACL, but read what to remove from a file
setfacl -X acl.txt file
```

##### Authorization Checking on Unix
- handler for system calls checks permissions for:
	1. files (open, rename, etc): file/directory permissions include UID or GIDprocesses (kill, etc): process UID = user UID

**Superuser**
- user ID 0 is superuser/root
- some OS functionality only works for UID 0:
	- shutdown, mount new file systems, etc.
- automatically passes essentially all permission checks

**Superuser vs. Kernel Mode**
- processor has 2 modes:
	1. kernel mode (what the core part of US uses)
	2. user mode (everything else)
- superusers are sill in user mode
- superuser : OS as kernel mode : hardware
##### Login Process
1. check if password is correct
2. change user ID
3. runs shell

**1. Unix Password Storage**
- typical single-user system
	- only readable by root/superuser
- department machines: network service
	- Kerberos/Active Directory:
	- server takes (encrypted) passwords, gives tokens
	- can cryptographically verify token come from server

**2. Changing User IDs**
- `int setuid(uid_t uid)`
- if superuser: sets effective UID to value passed in
- system starts in/login programs run as superuser
- login program “gives up” special access
##### `sudo`
- allows system administrator to configure superuser permissions to certain users for certain commands in the `sudoers` file

**set-user-ID sudo**
- extra metadata bit on executables: set-user-ID
- if set: `exec()` syscall changes effective UID to owner’s ID
	- “extra” user IDs track who original user was
- sudo program: owned by root, marked set-user-ID
- marking `setuid`: `chmod u+s`

**uses for `setuid` programs**
1. mount USB stick
	- `setuid` program controls option to kernel mount syscall
	- makes sure user can’t mess up sensitive directories, filesystems on normal hard disks, new `setiud` root files
2. control access to device: printer, monitor, etc.
	- `setuid` program talks to device + decides who can
3. write to secure log file
	- `setuid` program ensures that log is append-only for normal users
4. bind to a particular port number <1024
	- `setuid` program creates socket, then becomes not root

**Privilege Escalation**
- logic errors in checking delegated operations that allow more privileges
- *example*: code execution/corruption in utilities that run with high privilege → buffer overflow, command injection