---
layout: default
title: Caches
parent: readings
nav_order: 9
---
# Caches
### 1 A thought experiment
- Single-level caching either remembers memory or does not
- Multi-level caching can partially remember and assist in faster recovery
- **Tags** store where the data is found (e.g., book, page, word), while **blocks** store the data itself.
- **Cache line**: tag + block.

### 2 Locality
- **Locality** refers to how data is accessed in memory:
    - **Spatial locality**:
        - Small numerical differences between addresses.
        - Programs tend to access addresses close to previous ones.
    - **Temporal locality**:
        - Repeated access to the same address within a short time period.
- Caches are optimized for spatial and temporal locality.
#### 2.1 Cache line
- When caching memory, data from nearby addresses is also cached, based on spatial locality.
- Example:
    - Accessing `0x12345678` loads a block containing addresses from `0x12345640` to `0x1234567F`.
    - The **tag** for the block is based on the high-order bits (`0x48d159`), and the low-order bits represent the **block offset**.

**Comparison to Virtual Memory**
- Both cache lines and virtual memory pages use low-order bits as offsets into memory.
- **Virtual memory**:
    - Translates an address; if translation fails, a fault occurs.
- **Caching**:
    - Accelerates access; if data is not in the cache, RAM is accessed without failure.
- Virtual memory adds new system capabilities, while caching only increases speed.

### 3 Three types of caches
- A cache is a finite-size memory storing a subset of recent results.
- Caching applies to various contexts, with memory access being the most common.
- Cache designs vary based on how they replace old cache lines to make room for new ones.
#### 3.1 Fully-associative
- Stores cache lines in an unordered set, allowing maximum flexibility in line replacement.
- Requires checking every cache line's tag for every access.
- **Least-recently used (LRU)** rule is commonly used for deciding which line to replace.
- **Capacity miss**: occurs when all lines have been replaced since the last access, and the line is no longer in the cache.
##### 3.1.1 Capacity miss
- When a cache is accessed but the line desired is not located in it
- **cold miss** (**compulsory miss**): inevitable, happen when the address is accessed for the very first time
- **capacity miss**: occurs when every line in the cache has been replaced since the last access to the line being requested.
#### 3.2 Direct-mapped
- Stores cache lines in an array, with an index derived from the address.
- The index is based on spatial locality to maximize efficiency.
##### 3.2.1 Conflict miss
- **Conflict miss**: occurs when a different line with the same index replaces the desired line in the cache.
    - Example of memory accesses in order leading to a conflict miss:
        1. `0xbf1234` – cold miss
        2. `0xbf1238` – hit
        3. `0xbf9230` – cold miss
        4. `0xbf1234` – conflict miss
#### 3.3 Set-associative
- Compromise between fully-associative and direct-mapped caches.
- Array of sets of cache lines, each identified by a **set index**.
- Example: A 2-way set associative cache uses a least-recently used policy for replacing blocks.
	1. address `0xbf1234` – cold miss
	    - afterwards: set with index `0x23`: `0xbf1230` through `0xbf123f`
	2. address `0xbf1238` – hit
	    - afterwards: set with index `0x23`: `0xbf1230` through `0xbf123f`
	3. address `0xbf9230` – cold miss
	    - afterwards: set with index `0x23`: `0xbf1230` through `0xbf123f`; `0xbf9230` through `0bf923f`
	4. address `0xbfaa32` – cold miss
	    - since set only has 2 lines in it, the least recently used `0xbf1230` through `0xbf123f` is replaced
	    - afterwards: set with index `0x23`: `0xbfaa30` through `0xbfaa3f`; `0xbf9230` through `0bf923f`
	5. address `0xbf1234` – conflict miss
	    - since set only has 2 lines in it, the least recently used `0xbf9230` through `0xb9123f` is replaced
	    - afterwards: set with index `0x23`: `0xbfaa30` through `0xbfaa3f`; `0xbf1230` through `0bf123f`

### 4 Hierarchies of memory caches

![A block diagram of a cache hierarchy featuring two cores with: each core connected to an L1 instruction cache and an L1 data cache. The L1 caches for each core are in turn connected to an L2 cache labeled as 'unified' for the core. The two L2 caches are then connected to a shared L3 cache. The L3 cache is, in turn, connected to main mmeory.](https://www.cs.virginia.edu/~cr4bd/3130/F2024/readings/cache-hierarchy.svg)

- Modern systems typically have several levels of memory caches arranged in a hierarchy.
- **L1 Cache**:
    - Smallest and fastest.
    - Usually on the processor chip itself, often designed to complete at least one access per cycle.
    - Typically split into separate caches for instructions and data.
- **L2 Cache and higher**:
    - Larger than L1, resulting in slower access but fewer misses.
    - Often shared between multiple L1 caches and cores.
    - Most common setup (2023): L2 cache per core, shared L3 cache across cores.
- Caches work in levels, with higher levels accessed if data is not found in lower levels (e.g., L1 asks L2, and so on).
### 5 Page table caches (TLBs)
**TLBs (Translation Lookaside Buffers)**:
- Cache for page table entries.
- Usually a small set-associative cache storing the final page table entry (PTE) in address translation.
- Typically read-only, flushed when page tables are modified.
- Common setup (2023): similar hierarchy to memory caches with separate L1 data and instruction TLBs, and L2 TLBs.
### 6 Handling writes

#### 6.1 Write-through versus write-back
- **Write-back**:
    - Writes are stored in the cache and only written to the next level when the cache line is evicted.
    - Uses a "dirty bit" to track which lines have been modified.
    - Efficient for multiple edits to the same cache line before eviction.
- **Write-through**:
    - Writes are immediately sent to the next cache level.
    - Has a finite-size write queue; if full, it writes at the speed of the slower cache.
    - Efficient for lines that are rarely edited before eviction.
- Different cache levels can use different write policies (e.g., L1 can be write-back while L2 is write-through).
#### 6.2 Write-allocate versus write-no-allocate
- **Write-allocate**:
    - When writing to a new value, it is added to the cache, improving locality but sometimes requiring additional reads (e.g., loading the rest of a cache block).
- **Write-no-allocate**:
    - Written values that are not yet in the cache are forwarded directly to the next cache level without being added to the current cache.
### 7 Cache-efficient code
- Efficient code practices for caches:
    - Access memory regions together (temporal locality).
    - Use memory efficiently (spatial locality).
    - Align addresses to avoid spanning cache lines.
    - Access different regions with different set indexes to avoid conflicts.
- Cache-efficient code can lead to performance improvements but may be less readable and harder to maintain.