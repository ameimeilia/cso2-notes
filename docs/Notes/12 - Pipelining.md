> [!note]
> Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/pipeline.pdf
##### Pipelining
- **latency**: time to complete one instruction
- **throughput**: rate to complete many instructions (time between finishes = time between starts)
![[Screenshot 2024-11-16 at 5.08.20 PM.png | center | 500]]

*exercise - latency/throughput*
![[Screenshot 2024-11-16 at 5.17.19 PM.png | center | 500]]![[Screenshot 2024-11-16 at 5.18.10 PM.png | center | 500]]
##### Diminishing Returns
- can’t infinitely increase stages to decrease cycle time

**Register Delays**
![[Screenshot 2024-11-16 at 5.26.42 PM.png | center | 500]]

**Uneven Split**
![[Screenshot 2024-11-16 at 5.27.00 PM.png | center | 500]]

##### Data Hazard
- pipeline reads **older value** instead of value that should have just been written
![[Screenshot 2024-11-16 at 5.31.27 PM.png]]

**Compiler Solution**
- change the ISA: all `addq`s take effect 3 instructions later
	- assume we can read the register value while it is being written back, else 4 instructions later
- problem: must recompile every time processor changes

*3 instructions later*
![[Screenshot 2024-11-16 at 5.50.17 PM.png | center | 500]]

*4 instructions later*
![[Screenshot 2024-11-16 at 5.50.54 PM.png | center | 500]]
##### Control Hazard
- pipeline needs to read value that **hasn’t been computed** yet

**Hardware Solution**
- **stalling**: hardware inserts `nop`s where necessary
![[Screenshot 2024-11-16 at 6.06.49 PM.png | center | 500]]

**Guessing Solution**
- speculate that `jne` **won’t** go to `LABEL`
- if right, 2 cycles faster
- if wrong: undo before too late

*speculating wrong*
![[Screenshot 2024-11-16 at 11.00.52 PM.png | center | 500]]
- to “undo” partially executed instructions, remove values from pipeline registers
- more complicated pipelines: replace written values in cache/registers/etc.
##### Forwarding/Bypassing
**Opportunity 1**
- better solution for data hazard
![[Screenshot 2024-11-16 at 11.07.33 PM.png | center | 500]]

- to exploit the opportunity, use a mux that compares the register #’s in machine code
![[Screenshot 2024-11-16 at 11.08.27 PM.png | center | 500]]

**Opportunity 2**
![[Screenshot 2024-11-16 at 11.11.31 PM.png | center | 500]]

- to exploit the opportunity, add a second wire to the mux
![[Screenshot 2024-11-16 at 11.12.27 PM.png | center | 500]]

*exercise - forwarding paths*
![[Screenshot 2024-11-16 at 11.26.09 PM.png | center | 500]]
##### Stalling + Forwarding
- combine stalling and forwarding when a memory read is followed by an operation on the read value
	- forwarding from memory directly to execute requires completing both stages in one clock cycle → invalid
![[Screenshot 2024-11-25 at 5.50.27 PM.png | center | 500]]
- assume hazard is detected in `subq`’s decode stage → decode stage is repeated
- note that the following doesn’t require stalling:
	- in `movq %rbx`, `%rbx` is only used at the start of the memory stage
![[Screenshot 2024-11-25 at 5.54.20 PM.png | center | 500]]
##### Hazard vs Dependencies
- **hazard**: two instructions interfere with same value
	- extra work is done prior to resolve hazards
- **dependency**: X needs result of instruction Y
	- has potential for being messed up by pipeline if part of X runs before Y finishes
![[Screenshot 2024-11-25 at 6.03.41 PM.png | center | 400]]
- more pipeline stages = more hazards

*exercise - different pipeline*
![[Screenshot 2024-11-25 at 6.50.15 PM.png]]
##### Beyond Pipelining
**Multiple Issue**
- start **more than one instruction/cycle**
- multiple parallel pipelines: many-input/output register file
![[Screenshot 2024-11-19 at 2.31.05 PM.png | center | 500]]

**Out-of-order Execution**
- find **later instructions to do** instead of stalling
- lists of available instructions in pipeline registers
	- take any instruction with available values
- provide illusion that work is still done in order
![[Screenshot 2024-11-19 at 2.31.40 PM.png | center | 550]]
##### Out-of-order and Hazards
- out-of-order execution makes hazards harder to handle
	- problems for forwarding, branch prediction, figuring out which instructions to dispatch

*example - read after write*
![[Screenshot 2024-11-25 at 7.00.51 PM.png | center | 600]]

**Register Version Tracking**
- since out-of-order execution may compute versions at different times, track different versions of registers
- strategy: preprocess instructions to annotate version info
- only forward the version that matches what is expected
![[Screenshot 2024-11-19 at 2.38.15 PM.png | center | 450]]

*example - write after write*
![[Screenshot 2024-11-25 at 7.09.38 PM.png]]

**Keeping Multiple Versions**
- for write-after-write problem: need to keep copies of multiple versions
- for read-after-write problem: need to distinguish different versions
- **solution**: have many registers and assign each version a new “real” register

**Register Renaming**
- rename architectural registers to physical registers
- different physical register for each version of architectural
- track which physical registers are ready
- compare physical register numbers to do forwarding
##### An OOO Pipeline
![[Screenshot 2024-11-25 at 7.13.49 PM.png]]

**An OOO Pipeline Diagram**
![[Screenshot 2024-11-25 at 7.19.17 PM.png | center | 500]]
##### Register Renaming State
*example 1*
![[Screenshot 2024-11-25 at 7.26.13 PM.png | center | 500]]

*example 2*
- note: `(%rax)` could be the same location as `8(%r11)`, creating a dependency, an issue not handled via register renaming
- processor handles by either running load+stores in order sore comparing load/store address
![[Screenshot 2024-11-25 at 8.59.13 PM.png | center | 500]]

*exercise*
![[Screenshot 2024-11-25 at 9.05.19 PM.png | center | 500]]