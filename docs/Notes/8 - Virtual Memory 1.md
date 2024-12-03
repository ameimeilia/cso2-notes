##### Address Translation
![[Screenshot 2024-09-24 at 3.00.13 PM.png | center | 600]]
##### Toy Program Memory
![[Screenshot 2024-09-24 at 2.37.07 PM.png | center | 500]]![[Screenshot 2024-09-24 at 2.41.58 PM.png | center | 500]]
##### Toy Page Table Lookup
![[Screenshot 2024-09-24 at 2.47.04 PM.png | center | 500]]
##### Virtual Address Sizes
- virtual address sizes are not always the size of pointers, sometimes part of the pointer is not used
- virtual address size is amount actually used for mapping
##### Address Space Size
- amount that can be addressed, based on number of unique addresses
- eg. 32-bit virtual address = $2^{32}$ byte virtual address space
- eg. 20-bit physical address = $2^{20}$ byte physical address space

*exercise - page table size*
![[Screenshot 2024-09-29 at 11.27.33 PM.png | center | 400]]

*exercise - page table lookup*![[Screenshot 2024-09-24 at 3.29.25 PM.png]]
##### Permission Bits
- additional bits in page table entry that define:
	- user mode access
	- read, write, execute permissions
- checked by hardware, like the valid bit

