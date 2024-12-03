##### Memory Hierarchy Assumptions
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
##### Split Caches; Multiple Cores
- typically separate data and instruction caches for L1
- (almost) never going to read instructions as data or vice-versa
- can optimize instruction cache for different access pattern
- easier to build fast caches that handle less accesses at a time
![[Screenshot 2024-10-03 at 2.40.57 PM.png | center | 500]]
##### One-block Cache
![[Screenshot 2024-10-03 at 2.51.27 PM.png | center | 450]]
##### Direct-mapped Cache
![[Screenshot 2024-10-03 at 3.36.06 PM.png | center | 500]]
##### Tag-Index-Offset (TIO)
- depends on cache design
![[Screenshot 2024-10-03 at 3.27.41 PM.png | center | 500]]

**TIO Formulas (direct-mapped)**
![[Screenshot 2024-10-03 at 2.59.25 PM.png | center | 400]]
- **cache size**: amount of *data* in cache, not including metadata (tags, valid bits, etc.)

*exercise - TIO*
![[Screenshot 2024-10-03 at 3.16.44 PM.png | center | 550]]
