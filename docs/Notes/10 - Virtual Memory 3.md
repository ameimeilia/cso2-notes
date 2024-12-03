*example - pagetable lookup*
![[Screenshot 2024-10-01 at 2.10.26 PM.png]]
##### `translate()`
![[Screenshot 2024-10-05 at 5.46.22 PM.png]]
##### `page_allocate()`
- allocates a page table with a valid entry for arg, then make all other entries invalid
- if the page table is already allocated, simply add the valid entry
##### `posix_memalign`
```C
void *result;
error_code = posix_memalign(&result, alingment, size);
```
- allocates `size` bytes
- chooses address that is multiple of `alignment`
- `error_code` indicates if out-of-memory, etc.
- fills in `result`

##### Two-level Page Tables
- lookup implemented in hardware → must be simple → split up address bits
- should not involve many memory accesses → tree with many children from each node

##### Two-level Page Table Lookup
![[Screenshot 2024-10-01 at 3.56.36 PM.png]]

*another view*![[Screenshot 2024-10-01 at 3.56.51 PM.png | center | 500]]
##### Multi-level Page Tables
- VPN split into pieces for each level of page table
- top levels: page table entries point to next page table
- bottom level: page table entry points to destination page
- validity checks at *each level*
##### 2-level Splitting
![[Screenshot 2024-10-01 at 3.49.28 PM.png | center | 500]]

*example - 2 level page table lookups*
![[Screenshot 2024-10-01 at 3.08.58 PM.png]]

![[Screenshot 2024-10-01 at 3.42.38 PM.png]]

![[Screenshot 2024-10-03 at 2.17.04 PM.png]]
