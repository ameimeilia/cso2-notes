---
layout: default
title: Compilation, Makefiles
parent: readings
nav_order: 2
---
# Compilation, Makefiles
### 1 `clang`/`gcc` modes review

| mode                               | action                                                                                                                                                                                                                |
| ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `clang -S foo.c`                   | **compile** the source file `foo.c` into the assembly file `foo.s`. Note that this also uses any files `foo.c` includes                                                                                               |
| `clang -c foo.s`                   | **assemble** `foo.s` into the object file `foo.o`                                                                                                                                                                     |
| `clang foo.o bar.o quux.o`         | **link** the object files `foo.o`, `bar.o`, and `quux.o` into an **executable** `a.out`. By default this also links in the _standard library_ (which contains functions like `printf` and `malloc`) to the executable |
| `clang -shared foo.o bar.o quux.o` | **link** the object files `foo.o`, `bar.o`, and `quux.o` into a **shared library** `a.out`                                                                                                                            |
| `clang -c foo.c`                   | **compile + assemble** `foo.c`, to produce the object file `foo.o`                                                                                                                                                    |
| `clang foo.c bar.c`                | **compile + assemble** `foo.c`, and **compile + assemble** `bar.c`, and **link** them together to generate `a.out`                                                                                                    |
| `clang -o exec foo.o bar.o quux.o` | link `foo.o`, `bar.o`, and `quux.o` into the executable `exec` (instead of `a.out`)                                                                                                                                   |
### 2 selected other `clang`/`gcc` options

| flag                                                                                 | action                                                                                                                                                    |
| ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-Wall`                                                                              | enable all warnings                                                                                                                                       |
| `-g`                                                                                 | generate information for debuggers                                                                                                                        |
| `-Og`, `-O1`, `-O2`, `-O3`, `-Os`, `-O`                                              | compiler optimizations: `-Og` optimizes for debugging; `-Os` optimizes for size; levels 0/1/2/3 of optimizations                                          |
| `-std=c11`, `-std=c99`, `-ansi`, …                                                   | ask the compiler/standard library to follow a particular version of the C standard                                                                        |
| `-fsanitize=address`, `-fsanitize=undefined`, `-fsanitize=thread`, `-fsanitize=leak` | enable various sanitizers that check for certain types of errors/bugs as the resulting executables run (must be supplied both when compiling and linking) |
### 3 producing and using libraries
- **library**: collection of related implementations provided as a _library file_ and (one or more) _header files_
- two types of library files:
	1. **dynamic libraries**: loaded from the library file while an executable is running, extension `.so` (Linux), `.dylib` (OS X), or `.dll` (Windows)
	2. **static libraries**: embedded into an executable when it is linked, extension `.a` (Linux, OS X), `.lib` (Windows).    
#### 3.1 producing and using static libraries (on Unix-like systems)
- static libraries are archives of object files produced with the `ar` command

```C
# after generating object files
ar -rcs libfoo.a quux.o bar.o
# creates library libfoo.a

# if `libfoo.a` is placed in a standard system directory
clang -o exec main.o -lfoo
# creates an executable linking main.o and libfoo.a

# if `libfoo.a` is not placed in a standard system directory, add -L
`clang -o exec main.o -LdirectoryContainingLibFoo -lfoo`
```

- put `-lXXX` flags last since the linker processes the files listed in order
#### 3.2 producing and using dynamic libraries (on Linux)
- files used in a dynamic library need to be compiled specially using `-fPIC` so they can be loaded anywhere in memory

```C
# generate a libaray by linking with -shared
clang -shared -o libfoo.so bar.o quux.o

# if `libfoo.so` is placed in one of the standard system directories
clang -o exec main.o -lfoo
# creates an executable `exec` that loads `libfoo.so` at runtime

# if `libfoo.so` is *not* placed in one these directories, then you will need to:
# 1. use `-Ldirectory` to specify the directory to the compiler when generating the  
# executable:
clang -o exec main.o -LdirectoryWithLibFoo -lfoo

# 2. tell the executable how to find the library when it runs by either:

# 2.1: specifying an rpath (runtime path) when generating the executable with an additional directory to search:
clang -o exec main.o ... -Wl,-rpath,directoryWithLibFoo
# `-Wl,X` says to pass an option to the linker program, which is typically `ld` on Linux

# 2.2: setting the `LD_LIBRARY_PATH` environment variable to contain the directory containing the library when the executable is run:
$ LD_LIBRARY_PATH=directoryWithLibFoo ./exec ...
# or
$ export LD_LIBRARY_PATH=directoryWithLibFoo
...
$ ./exec ...

# to specify multiple directories: 
LD_LIBRARY_PATH=directory1:directory2:directory3
```
### 4 Glossary
**header file** `.h`
- file that provides:
	1. the signatures of functions, but not their definitions
	2. the names and types of global variables, but not where in memory they go
	3. `typedef`s and `#define`s

**object file** `.o`
- file that contains assembled binary code in the target ISA, with metadata to allow the linker to place it in various locations in memory depending on what other linked files

**standard library**
- _library_ to which every program is linked by default
- `libc`: C _standard library_ defined by the C standard, `glibc` is the most pervasive implementation on Linux

**static library** `.a`
- file that contains one more more _object files_ with metadata needed to connect them into a running code system by the _linker_
- compile-time linkage means that each executable has its own copy of the library stored internally to the file, without external dependencies

**source file** `.c`
- file that provides:
	1. the implementation of functions
	2. the declaration and implementation of provided helper functions
	3. the memory in which to store global variables
### The make tool
- `make` reads `Makefile` to decide what commands to run to update the project
- checks file modification times to determine which commands to generate
#### Rules
- makefile **rules**
	1. **target**: name of file created/updated by the rule
	2. **dependencies**: if the *target* is missing/older than a dependency, *system commands* will be run
	3. **system commands**: shell commands that result in (re)making the *target*

*example* - build `hello.o` if `hello.c` or `hello.h` is newer than `hello.o`
```
hello.o: hello.c hello.h
	clang -c hello.c
```

- `make` executes the first rule unless specified
*example* - running `make` will ensure `hello.o` is up to date, running `make bye.o` will ensure `bye.o` is up to date
```
hello.o: hello.c hello.h
    clang -c hello.c

bye.o: bye.c bye.h
    clang -c bye.c
```

- if a dependency of an executed rule is the target of another rule, the other rule will be executed first
*example* - running `make` will ensure `runme` is up to date, executing `hello.o` and `bye.o` which are dependencies
```
runme: hello.o bye.o main.c main.h
    clang main.c hello.o bye.o -o runme

hello.o: hello.c hello.h
    clang -c hello.c

bye.o: bye.c bye.h
    clang -c bye.c
```
#### Pattern Rules
- Use `%.ending` as a target. `%` is a wild-card and can represent any name.
- Use `%.other_ending` as a dependency. `%` has the same meaning it did in the target.
- Use `$<` in the system commands as the name of the first dependency.
- Use `$@` in the system commands as the name of the target.

*example* - many makefiles will include a command like
```
%.o: %.c %.h config.h
    $(CC) -c $(CFLAGS) $< -o $@
```
![[Screenshot 2024-08-29 at 4.30.53 PM.png]]