---
layout: default
title: Side Channels, Spectre
parent: Notes
nav_order: 14
---
# Side Channels, Spectre

{: .note }
> Slides: [spectre](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/spectre.pdf)

## Side Channels
- unintended communication channel which leaks information

**Naive Password Checking**
- number of iterations = number of matching characters
- leaks information about length of loop

```C
int check_passphrase(const char *versus) { 
	int i = 0; 
	while (passphrase[i] == versus[i] && passphrase[i]) { 
		i += 1; 
	} 
	return (passphrase[i] == versus[i]); }
```

- to exploit: run multiple guesses and measure time
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-27 at 12.42.35 AM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

## Timing and Cryptography
- lots of asymmetric cryptography uses big-integer math
	- ex. multiplying 500+ bit numbers together

**Big Integer Multiplication**
- suppose we have two 64-bit integers, $x, y$ that we want to multiple into a 128-bit product
- multiply only does 64-bit products
- solution:
	1. divide $x, y$ into 32-bit parts: $x=x_1 \cdot 2^{32} + x_0$ and $y=y_1 \cdot 2^{32} + y_0$
	2. $xy = x_1y_12^{64} + x_1y_0 \cdot 2^{32} + x_0y_1 \cdot 2^{32} + x_0y_0$

**Big Integers and Cryptography**
- native multiplication idea: number of steps depends on size of numbers
- problem: sometimes the value of the number is a secret (e.g. part of the private key)
- size of number is revealed through timing

## Browsers and Website Leakage
- web browsers run code from untrusted webpages
- goal: can’t tell what other webpages you visit
- leakage examples:
	1. browser marks visited links → scripts can query current color of something
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 1.20.10 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>
	2. script in webpage times loop that writes to a big array → variation in timing depends on **other things running on machine** → create distinct “signatures”
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 1.23.38 PM.png' | relative_url}}" alt="Screenshot" width="300">
</div>

## Inferring Cache Accesses
- can figure out if a value is in a cache or not depending on timing of cache accesses
- can figure out if a value was evicted depending on timing of accesses before/after evictions

*exercise*
- psuedocode:

```C
char array[CACHE_SIZE]; 
AccessAllOf(array); 
*other_address += 1; 
TimeAccessingArray();
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 1.34.06 PM.png' | relative_url}}" alt="Screenshot">
</div>
- B: evict from same row
- D: if tag and index are the same, the `*other_address` is part of the array

**Some Complications**
1. caches often use physical, not virtual addresses
2. storing/processing timings evicts things in the cache
3. processor “pre-fetching” may load things into cache before access is timed
4. some L3 caches use a simple hash function to select index instead

*exercise - inferring cache accesses 1*

```C
char *array; 
array = AllocateAlignedPhysicalMemory(CACHE_SIZE); 
LoadIntoCache(array, CACHE_SIZE); 
if (mystery) { 
	*pointer += 1; 
} 
if (TimeAccessTo(&array[index]) > THRESHOLD) { 
	/* pointer accessed */ 
}
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 1.50.41 PM.png' | relative_url}}" alt="Screenshot">
</div>

- aside: this detects when the pointer is accessed but not necessarily if `mystery` is true since branch prediction may haves started the cache access

*exercise - inferring cache accesses 2*

```C
char *other_array = ...; 
char *array; 
array = AllocateAlignedPhysicalMemory(CACHE_SIZE); 
LoadIntoCache(array, CACHE_SIZE); 
other_array[mystery] += 1; 
for (int i = 0; i < CACHE_SIZE; i += BLOCK_SIZE) { 
	if (TimeAccessTo(&array[i]) > THRESHOLD) { 
		/* found something interesting */ 
	}
}
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 1.59.35 PM.png' | relative_url}}" alt="Screenshot">
</div>

*exercise - inferring cache accesses 3*

```C
char *array; 
posix_memalign(&array, CACHE_SIZE, CACHE_SIZE); 
LoadIntoCache(array, CACHE_SIZE); 
if (mystery) { 
	*pointer = 1; 
} 
if (TimeAccessTo(&array[index1]) > THRESHOLD || 
	TimeAccessTo(&array[index2]) > THRESHOLD) { 
	/* pointer accessed */ 
}
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.02.30 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Prime + Probe
- coined in attacks on AES encryption
- one way to measure how cache is used
- procedure:
	1. **Prime**: fill cache (or part of it) with values
	2. do something that uses the cache
	3. **Probe**: access values again and see where it’s slow
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.05.01 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

*exercise - reading a value*

```C
char *array; 
posix_memalign(&array, CACHE_SIZE, CACHE_SIZE); 
AccessAllOf(array); 
other_array[mystery * BLOCK_SIZE] += 1; 
for (int i = 0; i < CACHE_SIZE; i += BLOCK_SIZE) { 
	if (CheckIfSlowToAccess(&array[i])) {
		... 
	} 
}
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.17.37 PM.png' | relative_url}}" alt="Screenshot">
</div>

## Revisiting an Earlier Example
- *exercise - inferring cache accesses 1*: what is mystery is false but branch mispredicted?
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.19.36 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
- pointer access and eviction is run

**Reading a Value Without Really Reading It**

```C
char *array; 
posix_memalign(&array, CACHE_SIZE, CACHE_SIZE); 
AccessAllOf(array); 
if (something false) { 
	other_array[mystery * BLOCK_SIZE] += 1; 
} 
for (int i = 0; i < CACHE_SIZE; i += BLOCK_SIZE) { 
	if (CheckIfSlowToAccess(&array[i])) { 
		... 
	} 
}
```

- check `mystery * BLOCK_SIZE = i +/- K * # sets`
- detect code that never runs and read the value it has

## Seeing Past a `segfault`
```C
Prime(); 
if (something false) { 
	triggerSegfault(); 
	Use(*pointer); 
} 
Probe();
```

- cache accesses for `*pointer` could still happen if both:
	1. branch for if statement mispredicted
	2. `*pointer` starts before `segfault` detected
- fix:
	1. hardware: permissions check done with/before physical address lookup
	2. software: separate page tables for kernel and user space

## Contrived(?) Vulnerable Code
- suppose code is run with extra privileges
- assume x chosen by attacker

```C
if (x < array1_size)    // sometimes gets mispredicted, goes out of bounds
	y = array2[array1[x] * 4096;    // leaks the lower bits of array1[x]
```

*exercise*

```C
char array1[...]; 
...
int secret; 
... 
y = array2[array1[x] * 4096];
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.43.39 PM.png' | relative_url}}" alt="Screenshot">
</div>

*exercise*

```C
unsigned char array1[...]; 
... 
int secret; 
... 
y = array2[array1[x] * 4096];
```

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.48.26 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

**Exploit with Contrived Code**

```C
/* in kernel: */ 
int systemCallHandler(int x) { 
	if (x < array1_size) 
		y = array2[array1[x] * 4096]; 
	return y; 
} 

/* exploiting code */ 
/* step 1: mistrain branch predictor */ 
for (a lot) { 
	systemCallHandler(0 /* less than array1_size */); 
} 
/* step 2: evict from cache using misprediction */ 
Prime(); 
systemCallHandler(targetAddress − array1Address); 
int evictedSet = ProbeAndFindEviction(); 
int targetValue = (evictedSet − array2StartSet) / setsPer4K;
```

**Really Contrived?**

```C
char *array1; char *array2; 
if (x < array1_size) 
	y = array2[array1[x] * 4096];
```
- times 4096 shifts so we can get lower bits of target value

```C
int *array1; int *array2; 
if (x < array1_size) 
	y = array2[array1[x]];
```

- will still get upper bits of `array1[x]`
- can still read arbitrary memory

**Bounds Check in Kernel**
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-12-02 at 2.56.41 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

## Privilege Levels
- vulnerable code runs with higher privileges
- there are other common cases of higher privilege besides kernel mode
	- ex. scripts in web browsers

## JavaScript
- scripts in webpages
- not supposed to be able to read arbitrary memory, but:
	- can access arrays to examine caches
	- could take advantage of some browser function being vulnerable
	- **could supply vulnerable code itself**

## Just-in-time Compilation
- for performance, compiled to machine code, run in browser
- not supposed to access arbitrary browser memory