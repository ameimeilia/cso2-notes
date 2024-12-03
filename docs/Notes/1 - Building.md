---
layout: default
title: Building
parent: Notes
nav_order: 1
---
# Building
{: .highlight }
Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/building.pdf
##### C/Pointer Review
<div style="text-align: center">
  <img src="{{ C+PointersReview | center | relative_url }}" alt="Screenshot">
</div>
##### Dynamic vs. Static Linking
**Dynamic Linking**
- fewer copies of std lib machine code on system
- automatically get library changes
- fewer copies in memory
- possibly slower to startup/run
- libc.so is “c standard library,” dynamic library, shared library, “shared object”
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 12.04.42 AM.png | relative_url }}" alt="Screenshot">
</div>

**Static Linking**
- libc.a file
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 12.23.21 AM.png | relative_url }}" alt="Screenshot">
</div>
##### Static vs. Shared Libraries
**Static Libraries**
- `lib[name].a`
- internally: archive of `.io` files with index
- creation: `ar rcs libfoo.a file1.o file2.o ...`
- usage: `cc ... -o program -L/path/to/lib ... -lfoo`

**Shared Libraries**
- `lib[name].so`
- creation:
	1. compile `.o` files with `-fPIC` (position independent code)
	2. `cc -shared ... -o lib[name].so`
- usage: `cc ... -o program -L/path/to/lib ... -lfoo` 
- `-L` sets path only when making executable
- runtime path set separately

**Finding Shared Libraries**
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 12.16.11 AM.png | relative_url }}" alt="Screenshot">
</div>
##### Libraries and Command Line
- linker processes files in order, put library at the end of the command
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 12.17.48 AM.png | relative_url }}" alt="Screenshot" width="400">
</div>

##### make
- runs commands based on what’s changed based on rules in `makefile`
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-08-29 at 3.14.46 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

**Make Rule Chains**
- runs commands if any prerequisite modified after target after making sure prerequisites up to date
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 12.26.18 AM.png | relative_url }}" alt="Screenshot" width="500">
</div>

**Running Make**
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 12.27.51 AM.png | relative_url }}" alt="Screenshot" width="400">
</div>

**Make Example**
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 12.50.45 AM.png | relative_url }}" alt="Screenshot">
</div>

**Phony Targets**
- common to have Makefile targets that aren’t files, or don’t build a file
- `make all` and  `make clean` where
```shell
clean:
	rm --force main.p extra.o

all: program1 program2 libfoo.a

# specifies that 'all' and 'clean' are not real files
.PHONY: all clean
```

**Conventional Targets**
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 12.59.25 AM.png | relative_url }}" alt="Screenshot" width="400">
</div>

**Redundancy with Variables/Macros**
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 1.04.17 AM.png | relative_url }}" alt="Screenshot">
</div>

**Conventional Variable Names**
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-09-09 at 1.02.25 AM.png | relative_url }}" alt="Screenshot" width="400">
</div>

**Pattern Rules/Built-In Rules**
<div style="text-align: center">
  <img src="{{ Screenshot 2024-09-09 at 1.11.31 AM.png | relative_url }}" alt="Screenshot">
</div>

