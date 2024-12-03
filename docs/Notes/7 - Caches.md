---
layout: default
title: Caches
parent: Notes
nav_order: 7
---
# Caches

{: .highlight }
> Slides: [caches](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/caching.pdf)

## Memory Hierarchy Assumptions
- **temporal locality**: caches should keep *recently accessed values*
- **spatial locality**: caches should *store adjacent values at the same time*

*example - locality*

```C
double computeMean(int length, double *values) {
	double total = 0.0;
	for (int i = 0; i< length; i++) {
		total += values[i];
	}
	return total / length;
}
```

- temporal locality: machine code of loop; `total`, `i`, `length` accessed repeatedly
- spatial locality: machine code of most consecutive instructions; `values[i]` and `values[i+1]` accessed

## Split Caches; Multiple Cores
- typically separate data and instruction caches for L1
- (almost) never going to read instructions as data or vice-versa
- can optimize instruction cache for different access pattern
- easier to build fast caches that handle less accesses at a time
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 2.40.57 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## One-block Cache
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 2.51.27 PM.png' | relative_url}}" alt="Screenshot" width="450">
</div>

## Direct-mapped Cache
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 3.36.06 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Tag-Index-Offset (TIO)
- depends on cache design
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 3.27.41 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**TIO Formulas (direct-mapped)**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 2.59.25 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>
- **cache size**: amount of *data* in cache, not including metadata (tags, valid bits, etc.)

*exercise - TIO*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-03 at 3.16.44 PM.png' | relative_url}}" alt="Screenshot" width="550">
</div>

## Direct-mapped Caches
*example - access pattern*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 9.36.59 PM.png' | relative_url}}" alt="Screenshot">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 9.37.14 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Mapping of sets to memory**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 9.40.47 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Misses
**Simulated Misses: BST Lookups**
*simulated 16KB direct-mapped data cache; excluding BST setup*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 9.43.22 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Actual Misses: BST Lookups**
*actual 32KB more complex data cache - using set-associative cache*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 9.46.30 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Simulated Misses: Matrix Multiplies**
*simulated 16KB direct-mapped cache; excluding initial load*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 10.02.41 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Actual Misses: Matrix Multiplies**
*actual 32KB more complex data cache; excluding matrix initial load*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-13 at 10.03.25 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Associativity
- multiple places to put values with the same index
- avoid misses from two active values using same set (**conflict misses**)

*cache operation*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 8.27.43 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

**Associative Lookup Possibilites**
1. none of the blocks for the index are valid
2. none of the valid blocks for the index match the tag
3. one of the blocks for the index is valid and matches the tag

- the least recently used (**LRU**) bit tracks which way was read least recently and is updated on every access
- once both ways are full, use the LRU bit to determine which way to replace to ensure temporal locality
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 8.32.05 PM.png' | relative_url}}" alt="Screenshot">
</div>

**Example Replacement Policies**
1. least recently used
	- takes advantage of temporal locality
	- at least $[log_2(E!)]$ bits per set for $E$-way cache
2. approximations of least recently used
	- implementing least recently used is expensive
	- really just need to “avoid recently used” - much faster/simpler
	- good approximations: $E$ to $2E$ bits
3. first-in, first-out
	- counter per set - where to replace next
4. (pseudo-) random
	- no extra information
	- actually works pretty well in practice

**Terminology**
1. **direct-mapped**: one block per set
2. **$E$-way set associative**: $E$ blocks per set, $E$ ways in the cache
3. **fully-associative**: one set total (everything in one set)

**TIO Formula Update**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 8.47.43 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

## Cache Accesses and C Code
*exercise - what data cache accesses does this function do?*

```C
int scaleFactor;

int scaleByFactor(int value) {
	return value * scaleFactor;
}
```

```
scaleByFactor:
	movl scaleFactor, %eax
	imull %edi, %eax
	ret
```

1. M[scaleFactor address] → eax
2. pop from stack for `ret`

**Misses and Code**
- suppose each time `scaleByFactor` is called in a loop:
	1. return address located at address `0x7ffffffe43b8`
	2. `scaleFactor` located at address `0x6bc3a0`

- with direct mapped 32KB cache with 64B blocks
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.02.48 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Exercise: C and Cache Misses

```C
int array[4];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0];
odd_sum += array[1];
even_sum += array[2];
odd_sum += array[3];
```

- how many data cache misses on a 1-set direct-mapped cache with 8B blocks?

**Possibilities**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.16.11 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.16.29 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.16.39 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**Aside: Alignment**
- compilers and malloc/new implementations usually try to **align** values
- align = make address be multiple of something
- most important reason: don’t cross cache block boundaries

## Exercises: C and Cache Misses

```C
int array[4];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0];
odd_sum += array[2];
even_sum += array[1];
odd_sum += array[3];
```

- assume `array[0]` at beginning of cache block
- how many data cache misses on a 1-set direct-mapped cache with 8B blocks?

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.25.26 PM.png' | relative_url}}" alt="Screenshot">
</div>

```C
int array[8];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0];
odd_sum += array[1];
even_sum += array[2];
odd_sum += array[3];
even_sum += array[4];
odd_sum += array[5];
even_sum += array[6];
odd_sum += array[7];
```

- how many data cache misses on a **2-set** direct-mapped cache with 8B blocks?

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.28.14 PM.png' | relative_url}}" alt="Screenshot">
</div>
- observation: what happens in set 0 doesn’t affect set 1
- when evaluating set 0 accesses, can ignore non-set 0 accesses/content

```C
int array[8];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0];
odd_sum += array[2];
even_sum += array[4];
odd_sum += array[6];
even_sum += array[1];
odd_sum += array[3];
even_sum += array[5];
odd_sum += array[7];
```

- how many data cache misses on a **2-set** direct-mapped cache with 8B blocks?

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 9.34.06 PM.png' | relative_url}}" alt="Screenshot">
</div>

```C
int array[1024];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0]; // miss -> in set 0
odd_sum += array[2]; // hit
even_sum += array[512]; // miss, offset by 2048B -> also in set 0
odd_sum += array[514]; // hit
even_sum += array[1]; // miss
odd_sum += array[3]; // hit
even_sum += array[511]; // miss -> at very last set
odd_sum += array[513]; // miss
```

- array[0] and array[512] are exactly 2KB apart
- how many data cache misses on a 2KB direct mapped cache with 16B blocks?

## Misses with Skipping

```C
int array1[512]; int array2[512];
...
for (int i = 0; i < 512; i += 1){
	sum += array1[i] * array2[i];
}
```

- about how many data cache misses on a 2KB direct-mapped cache with 16B cache blocks?
- depends on relative placement of array1 and array2

**Best/Worst Case**
`array1[i]` and `array2[i]` always different sets:
- = distance from `array1` to `array2` not multiple of # sets * bytes/set
- 2 misses every 4 `i`
- blocks of 4 `array_[X]` values loaded, then used 4 times before loading next block

`array1[i]` and `array2[i]` same sets:
-  = distance from `array1` to `array2` is multiple of # sets * bytes/set
- 2 misses every i
- block of 4 `array1[X]` values loaded, 1 value used from it, then block of 4 `array2[X]` values replaces it, 1 value used from it, …

**Worst Case in Practice**
- 2 rows of matrix
- often sizeof(row) bytes apart
- row size is multiple of # sets * bytes/block
- **takeaway**: always access arrays in row major order
## Mapping of Sets to Memory (3-way)
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-14 at 11.44.43 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Exercise: C and Cache Misses (Assoc.)

```C
int array[1024];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0]; // miss -> set 0, way 0
odd_sum += array[2]; // hit
even_sum += array[512]; // miss -> set 0, way 1
odd_sum += array[514]; // hit
even_sum += array[1]; // hit
odd_sum += array[3]; // hit
even_sum += array[511]; // miss
odd_sum += array[513]; // hit
```

- observation: `array[0]`, `array[256]`, `array[512]`, `array[768]` are in the same set
- how many data cache misses on a 2KB 2-way set associative cache with 16B blocks?

```C
int array[1024];
...
int even_sum = 0, odd_sum = 0;
even_sum += array[0]; // miss -> set 0, way 0
odd_sum += array[256]; // miss -> set 0, way 1
even_sum += array[512]; // miss -> replace set 0, way 0
odd_sum += array[768]; // miss -> replace set 0, way 1
even_sum += array[1]; // miss -> ...
odd_sum += array[257]; // miss
even_sum += array[513]; // miss
odd_sum += array[769]; // miss
```

- observation: `array[0]`, `array[256]`, `array[512]`, `array[768]` are in the same set
- how many data cache misses on a 2KB 2-way set associative cache with 16B blocks?

## Simulated Misses
**BST Lookups**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.00.15 AM.png' | relative_url}}" alt="Screenshot">
</div>

**Matrix Multiplies**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.00.43 AM.png' | relative_url}}" alt="Screenshot">
</div>

## Handling Writes
two decision points:
1. if the value is not in the cache, do we add it?
	- yes: need to load rest of block (**write-allocate**)
	- no: missing out on locality? (**write-no-allocate**)
2. if the value is in the cache, when do we update next level?
	- immediately: extra writing (**write-through**)
	- later: need to remember to do so (**write-back**)

## Allocate on Write
- processor writes less than whole cache block
- block not yet in cache, 2 options:
	1. **write-allocate**: fetch rest of cache block, replace written part (then follow write-through or write-back policy)
	2. **write-no-allocate**: don’t use cache at all, send write to memory instead
- block in cache, 2 options:
	1. **write-through**: write value to cache then to memory
	2. **write-back**: write value to cache, then write to memory when a conflict occurs
*write-allocate*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.38.48 AM.png' | relative_url}}" alt="Screenshot">
</div>

*write-no-allocate*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.39.14 AM.png' | relative_url}}" alt="Screenshot">
</div>

*write-through*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.39.54 AM.png' | relative_url}}" alt="Screenshot">
</div>

*write-back*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.42.29 AM.png' | relative_url}}" alt="Screenshot">
</div>
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.43.56 AM.png' | relative_url}}" alt="Screenshot">
</div>

*example: write-allocate + write-back*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.47.00 AM.png' | relative_url}}" alt="Screenshot">
</div>

*example: write-no-allocate + write-back*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.47.39 AM.png' | relative_url}}" alt="Screenshot">
</div>

*exercise*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.56.15 AM.png' | relative_url}}" alt="Screenshot">
</div>

## Fast Writes
- write appears to complete immediately when placed in buffer
- memory can be much slower
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-15 at 12.59.43 AM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

## Cache Tradeoffs
- larger caches → slower hits
- higher associativity → slower hits
- lots of tradeoffs
	- more cache hits v. slower cache hits?
	- faster cache hits v. fewer cache hits?
	- more cache hits v. slower cache misses?
- details depend on programs run
	- how often is the same block used again?
	- how often is the same index bit used?

## Side Notes: Caches
- most common processors use physical memory for caches

- cache lookup with virtual addresses → aliasing among processes
- indexing using PA must wait for TLB
- solution: index using VA bits (index bits in the page offset)
- do TLB lookup in parallel
- tag check using PA bits

## Page Table Entry Cache
- called a **TLB** (translation lookaside buffer)
- (usually very small) cache of page table entries
- TLB output can be used directly to form address
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-21 at 1.57.47 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

*VPN, PTE*
- only caches the page table lookup itself
- (generally) just entries from the **last-level page tables**
- VPN is divided into index + tag
*one page table entry per block*
- not much spatial locality between page table entries (they’re used for KBs of data already)
- 0 offset bits
*usually tens of entries*
- few active page table entries at a time enables highly associative cache designs

## TLB and Two-level Lookup
**TLB Hit**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-21 at 2.16.19 PM.png' | relative_url}}" alt="Screenshot">
</div>

**TLB Miss**
- at the end, send the PTE to the TLB to store
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-21 at 2.16.44 PM.png' | relative_url}}" alt="Screenshot">
</div>

## TLB Organization (2 way set associative)
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-21 at 2.25.43 PM.png' | relative_url}}" alt="Screenshot">
</div>

*exercise - TLB access pattern setup*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-21 at 2.39.45 PM.png' | relative_url}}" alt="Screenshot">
</div>

*example - TLB access pattern*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-10-21 at 3.05.08 PM.png' | relative_url}}" alt="Screenshot">
</div>
