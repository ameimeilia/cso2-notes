---
layout: default
title: Threads
parent: Notes
nav_order: 8
---
# Threads
{: .highlight }
Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/threads.pdf
## Why Threads?
1. **concurrency**: one thread for each different thing happening at the same time
2. **parallelism**: do same thing with more resources
## Single and Multithread Processes
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-21 at 3.09.54 PM.png | relative_url }}" alt="Screenshot">
</div>

## `pthread_create`

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

<div style="text-align: center;">
  <img src="{{ Screenshot 2024-10-21 at 11.15.42 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

## A Threading Race
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

## Thread Example
*example - sum, only globals*
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-21 at 10.02.27 PM.png | relative_url }}" alt="Screenshot">
</div>

**Memory Layout**
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-21 at 10.02.40 PM.png | relative_url }}" alt="Screenshot">
</div>

*example - sum, to global, with thread IDs*
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-21 at 10.07.53 PM.png | relative_url }}" alt="Screenshot">
</div>

## Thread Example
*example - sum, info struct*
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-27 at 6.00.01 PM.png | relative_url }}" alt="Screenshot">
</div>
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-10-22 at 2.27.57 PM.png | relative_url }}" alt="Screenshot" width="400">
</div>

*example - sum, to main stack*
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-27 at 6.00.53 PM.png | relative_url }}" alt="Screenshot">
</div>
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-10-22 at 2.30.51 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

*example - sum, on heap*
<div style="text-align: center">
  <img src="{{ Screenshot 2024-10-27 at 6.08.11 PM.png | relative_url }}" alt="Screenshot">
</div>
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-10-22 at 2.31.11 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

## Returning from Threads

```C
/* omitted: headers */
void *create_string(void *ignored_argument) {
	char string[1024];
	ComputeString(string); 
	return string; // string is stored in the stack for THIS thread
}
int main() {
	pthread_t the_thread; 
	pthread_create(&the_thread, NULL, create_string, NULL); 
	char *string_ptr; // string_ptr is stored on the stack for the MAIN thread
	pthread_join(the_thread, (void**) &string_ptr); 
	printf("string is %s\n", string_ptr);
}
```

<div style="text-align: center;">
  <img src="{{ Screenshot 2024-10-22 at 2.35.34 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

## Thread Joining
- `pthread_join` allows collecting thread return value
- if you don’t join joinable thread → **memory leak**
- to avoid memory leak: always join, or “detach” thread to make it not joinable

**`pthread_detach`**
- detach = don’t care about return value, etc.
- system will deallocate when thread terminates

```C
void *show_progress(void * ...) { ... }
void spawn_show_progress_thread() {
	pthread_t show_progress_thread;
	pthread_create(&show_progress_thread, NULL, show_progress, NULL);
	
	/* instead of keeping pthread_t around to join thread later: */ 
	pthread_detach(show_progress_thread);
}

int main() {
	spawn_show_progress_thread();
	do_other_stuff();
	...
}
```

**Starting Threads Detached**

```C
void *show_progress(void * ...) { ... }
void spawn_show_progress_thread() {
	pthread_t show_progress_thread;
	pthread_attr_t attrs;
	pthread_attr_init(&attrs);
	pthread_attr_setdetachstate(&attrs, PTHREAD_CREATE_DETACHED);
	pthread_create(&show_progress_thread, attrs, show_progress, NULL); 
	pthread_attr_destroy(&attrs);
}
```

**Setting Stack Sizes**

```C
void *show_progress(void * ...) { ... }
void spawn_show_progress_thread() {
	pthread_t show_progress_thread;
	pthread_attr_t attrs; pthread_attr_init(&attrs); 
	// set stack size of thread
	pthread_attr_setstacksize(&attrs, 32 * 1024 /* bytes */); 
	pthread_create(&show_progress_thread, attrs, show_progress, NULL);
}
```
