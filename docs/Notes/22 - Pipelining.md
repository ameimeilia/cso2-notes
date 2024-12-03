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