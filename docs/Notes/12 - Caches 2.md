##### Direct-mapped Caches
*example - access pattern*
![[Screenshot 2024-10-13 at 9.36.59 PM.png]]![[Screenshot 2024-10-13 at 9.37.14 PM.png]]

**Mapping of sets to memory**
![[Screenshot 2024-10-13 at 9.40.47 PM.png]]
##### Misses
**Simulated Misses: BST Lookups**
*simulated 16KB direct-mapped data cache; excluding BST setup*
![[Screenshot 2024-10-13 at 9.43.22 PM.png]]

**Actual Misses: BST Lookups**
*actual 32KB more complex data cache - using set-associative cache*
![[Screenshot 2024-10-13 at 9.46.30 PM.png]]

**Simulated Misses: Matrix Multiplies**
*simulated 16KB direct-mapped cache; excluding initial load*
![[Screenshot 2024-10-13 at 10.02.41 PM.png]]

**Actual Misses: Matrix Multiplies**
*actual 32KB more complex data cache; excluding matrix initial load*
![[Screenshot 2024-10-13 at 10.03.25 PM.png]]
##### Associativity
- multiple places to put values with the same index
- avoid misses from two active values using same set (**conflict misses**)

*cache operation*
![[Screenshot 2024-10-14 at 8.27.43 PM.png | center | 400]]

**Associative Lookup Possibilites**
1. none of the blocks for the index are valid
2. none of the valid blocks for the index match the tag
3. one of the blocks for the index is valid and matches the tag

- the least recently used (**LRU**) bit tracks which way was read least recently and is updated on every access
- once both ways are full, use the LRU bit to determine which way to replace to ensure temporal locality
![[Screenshot 2024-10-14 at 8.32.05 PM.png]]

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
![[Screenshot 2024-10-14 at 8.47.43 PM.png | center | 400]]
##### Cache Accesses and C Code
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
![[Screenshot 2024-10-14 at 9.02.48 PM.png]]
##### Exercise: C and Cache Misses
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
![[Screenshot 2024-10-14 at 9.16.11 PM.png | center | 500]]![[Screenshot 2024-10-14 at 9.16.29 PM.png | center | 500]]![[Screenshot 2024-10-14 at 9.16.39 PM.png | center | 500]]
**Aside: Alignment**
- compilers and malloc/new implementations usually try to **align** values
- align = make address be multiple of something
- most important reason: don’t cross cache block boundaries