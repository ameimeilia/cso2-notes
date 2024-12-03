##### Thread Example
*example - sum, info struct*
![[Screenshot 2024-10-27 at 6.00.01 PM.png]]
![[Screenshot 2024-10-22 at 2.27.57 PM.png | center | 400]]

*example - sum, to main stack*
![[Screenshot 2024-10-27 at 6.00.53 PM.png]]
![[Screenshot 2024-10-22 at 2.30.51 PM.png | center | 500]]

*example - sum, on heap*
![[Screenshot 2024-10-27 at 6.08.11 PM.png]]
![[Screenshot 2024-10-22 at 2.31.11 PM.png | center | 500]]
##### Returning from Threads
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

![[Screenshot 2024-10-22 at 2.35.34 PM.png | center | 500]]
##### Thread Joining
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
##### Atomic Operation
- operation that runs to completion or not at all
- most machines: loading/storing (aligned) values is atomic:
	- ex. can’t get x = 3 from x ← 1 and x ← 2 running in parallel
	- aligned = address of word is multiple of word size
- some instructions are not atomic, ex:
	- x86: integer `add` constant to memory location
	- many CPUs: loading/storing values that cross cache blocks

**What is actually atomic?**
- assume load/stores of ‘words’
- processor designer will specify what is atomic
- if not specified, not assume atomic
##### Thinking about Race Conditions
![[Screenshot 2024-10-27 at 6.28.46 PM.png | center | 500]]

**Lost `add`**
![[Screenshot 2024-10-27 at 6.36.55 PM.png | center | 500]]![[Screenshot 2024-10-27 at 6.38.24 PM.png | center | 500]]
- occurs on multiple cores since `add` is implemented with multiple steps (load, add, store internally)
- can be interleaved with what other cores do