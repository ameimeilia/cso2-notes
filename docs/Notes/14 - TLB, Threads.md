##### Side Notes: Caches
- most common processors use physical memory for caches

- cache lookup with virtual addresses → aliasing among processes
- indexing using PA must wait for TLB
- solution: index using VA bits (index bits in the page offset)
- do TLB lookup in parallel
- tag check using PA bits
##### Page Table Entry Cache
- called a **TLB** (translation lookaside buffer)
- (usually very small) cache of page table entries
- TLB output can be used directly to form address
![[Screenshot 2024-10-21 at 1.57.47 PM.png | center | 500]]
*VPN, PTE*
- only caches the page table lookup itself
- (generally) just entries from the **last-level page tables**
- VPN is divided into index + tag
*one page table entry per block*
- not much spatial locality between page table entries (they’re used for KBs of data already)
- 0 offset bits
*usually tens of entries*
- few active page table entries at a time enables highly associative cache designs
##### TLB and Two-level Lookup
**TLB Hit**
![[Screenshot 2024-10-21 at 2.16.19 PM.png]]

**TLB Miss**
- at the end, send the PTE to the TLB to store
![[Screenshot 2024-10-21 at 2.16.44 PM.png]]
##### TLB Organization (2 way set associative)
![[Screenshot 2024-10-21 at 2.25.43 PM.png]]

*exercise - TLB access pattern setup*
![[Screenshot 2024-10-21 at 2.39.45 PM.png]]

*example - TLB access pattern*
![[Screenshot 2024-10-21 at 3.05.08 PM.png]]
##### Why Threads?
1. **concurrency**: one thread for each different thing happening at the same time
2. **parallelism**: do same thing with more resources
##### Single and Multithread Processes
![[Screenshot 2024-10-21 at 3.09.54 PM.png]]
##### `pthread_create`
```C
void *ComputerPi(void *argument) { ... }
void *PrintClassList(void *argument) { ... }
int main() {
	pthread_t pi_thread, list_thread;
	/* pthread_create arguments:
	 * 1. thread identifier (&pi_thread, &list_thread)
	 * 2. function to run, thread starts here (ComputePi, PrintClassList)
	 * 3. thread attributes (extra settings) / function argument (NULLs)
	*/
	if (0 != pthread_create(&pi_thread, NULL, ComputePi, NULL))
		handle_error();
	if (0 != pthread_create(&list_thread, NULL, PrintClassList, NULL))
		handle_error();
	... /* more code */
}
```

![[Screenshot 2024-10-21 at 11.15.42 PM.png | center | 500]]
##### A Threading Race
- non-deterministic behavior when working with threads → race conditions
*example - output `in the thread` ~ 4% of the time*
```C
#include <pthread.h>
#include <stdio.h>
void *print_message(void *ignored_argument) {
	printf("In the thread\n");
	return NULL;
}
int main() {
	printf("About to start thread\n");
	pthread_t the_thread;
	/* assume does not fail */
	pthread_create(&the_thread, NULL, print_message, NULL);
	printf("Done starting thread\n");
	return 0; // returning from main exists the entire process, including threads
}
// race: main's return 0 or print_message's prinf first?
```

**Solutions**
```C
printf("Done starting thread\n");
pthread_join(the_thread, NULL); // wait for thread
return 0;
```
- `R = pthread_join(X, &P)`: wait for thread `X`, copies return values into `P`
- like `waitpid`, but for a thread
- thread return value is pointer to anything
- `R = 0` if successful, error code otherwise

```C
printf("Done starting thread\n");
pthread_exit(NULL);
```
- exit current thread, returning a value
- like `exit` or returning from main, but for a single thread
- same effect as returning from function passed to `pthread_create`

**Error Checking `pthread_create`**
```C
int error = pthread_create(...);
if (error != 0) {
	/* print some error message */
}
```
##### Thread Example
*example - sum, only globals*
![[Screenshot 2024-10-21 at 10.02.27 PM.png]]

**Memory Layout**
![[Screenshot 2024-10-21 at 10.02.40 PM.png]]

*example - sum, to global, with thread IDs*
![[Screenshot 2024-10-21 at 10.07.53 PM.png]]