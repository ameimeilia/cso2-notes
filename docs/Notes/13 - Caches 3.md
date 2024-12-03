##### Exercises: C and Cache Misses
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

![[Screenshot 2024-10-14 at 9.25.26 PM.png]]

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

![[Screenshot 2024-10-14 at 9.28.14 PM.png]]
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

![[Screenshot 2024-10-14 at 9.34.06 PM.png]]

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
##### Misses with Skipping
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
##### Mapping of Sets to Memory (3-way)
![[Screenshot 2024-10-14 at 11.44.43 PM.png]]
##### Exercise: C and Cache Misses (Assoc.)
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
##### Simulated Misses
**BST Lookups**
![[Screenshot 2024-10-15 at 12.00.15 AM.png]]

**Matrix Multiplies**
![[Screenshot 2024-10-15 at 12.00.43 AM.png]]
##### Handling Writes
two decision points:
1. if the value is not in the cache, do we add it?
	- yes: need to load rest of block (**write-allocate**)
	- no: missing out on locality? (**write-no-allocate**)
2. if the value is in the cache, when do we update next level?
	- immediately: extra writing (**write-through**)
	- later: need to remember to do so (**write-back**)
##### Allocate on Write
- processor writes less than whole cache block
- block not yet in cache, 2 options:
	1. **write-allocate**: fetch rest of cache block, replace written part (then follow write-through or write-back policy)
	2. **write-no-allocate**: don’t use cache at all, send write to memory instead
- block in cache, 2 options:
	1. **write-through**: write value to cache then to memory
	2. **write-back**: write value to cache, then write to memory when a conflict occurs
*write-allocate*
![[Screenshot 2024-10-15 at 12.38.48 AM.png]]

*write-no-allocate*
![[Screenshot 2024-10-15 at 12.39.14 AM.png]]

*write-through*
![[Screenshot 2024-10-15 at 12.39.54 AM.png]]

*write-back*
![[Screenshot 2024-10-15 at 12.42.29 AM.png]]
![[Screenshot 2024-10-15 at 12.43.56 AM.png]]

*example: write-allocate + write-back*
![[Screenshot 2024-10-15 at 12.47.00 AM.png]]

*example: write-no-allocate + write-back*
![[Screenshot 2024-10-15 at 12.47.39 AM.png]]

*exercise*
![[Screenshot 2024-10-15 at 12.56.15 AM.png]]
##### Fast Writes
- write appears to complete immediately when placed in buffer
- memory can be much slower
![[Screenshot 2024-10-15 at 12.59.43 AM.png | center | 400]]
##### Cache Tradeoffs
- larger caches → slower hits
- higher associativity → slower hits
- lots of tradeoffs
	- more cache hits v. slower cache hits?
	- faster cache hits v. fewer cache hits?
	- more cache hits v. slower cache misses?
- details depend on programs run
	- how often is the same block used again?
	- how often is the same index bit used?