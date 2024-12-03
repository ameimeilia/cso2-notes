> [!note]
> Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/ooo.pdf, https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/bpred.pdf
##### Instruction Queue and Dispatch
- iterate through instruction queue each cycle and determine which instructions can be run
![[Screenshot 2024-11-25 at 9.19.18 PM.png]]

- more common to have specialized execution units
- issue stage matches instructions to execution units that can run them
![[Screenshot 2024-11-25 at 9.30.38 PM.png]]
##### Execution Units/Functional Units
- where actual work of instruction is done, e.g. the actual ALU, or data cache
- sometimes pipelined:
![[Screenshot 2024-11-21 at 2.17.11 PM.png | center | 500]]

*exercise*
![[Screenshot 2024-11-21 at 2.24.21 PM.png | center | 400]]

- sometimes unpipelined:
![[Screenshot 2024-11-21 at 2.24.48 PM.png | center | 500]]
##### Instruction Queue and Dispatch (multicycle)
![[Screenshot 2024-11-25 at 9.53.30 PM.png]]
##### Register Renaming: Missing Pieces
- deal with “hidden” inputs such as `%rsp`, condition codes?
- solution: translate to instructions with additional register parameters
	- making `%rsp` explicit parameter
	- turning hidden condition codes into operands
- can also translate complex instructions to simpler ones
![[Screenshot 2024-11-21 at 2.32.41 PM.png]]
##### OOO Limitations
- can’t always find instructions to run
- need to track all uncommitted instructions
- branch misprediction has a big cost (relative to pipelined)
##### Importance of Prediction
- predicting a jump is always not taken/stalling both result in 2 wasted cycles for each jump taken
![[Screenshot 2024-11-25 at 10.03.02 PM.png | center | 400]]
- additionally, stalling also results in 2 wasted cycles for each jump not taken
- correct branch prediction has a very big impact on performance
![[Screenshot 2024-11-25 at 11.10.42 PM.png | center | 500]]
##### Static Branch Prediction
- forward not taken, backward taken
- if the target of the jump is greater than the PC, assume the jump is not taken
- if the target of the jump is less than the PC, assume the jump is taken
![[Screenshot 2024-11-25 at 10.13.07 PM.png | center | 300]]

*example - predict same as last*
![[Screenshot 2024-11-25 at 10.27.33 PM.png]]
##### Collisions
- 2 branches could have same hashed PC
- possible results:
	1. both branches usually taken
		- no actual conflict, prediction is better
	2. both branches usually not take
		- no actual conflict, prediction is better
	3. one branch taken, one not taken
		- performance probably worse
- not worth it to track collisions

*exercise*
![[Screenshot 2024-11-25 at 10.44.21 PM.png]]

![[Screenshot 2024-11-25 at 10.49.30 PM.png]]

![[Screenshot 2024-11-25 at 10.50.59 PM.png]]
##### 2-bit Saturating Counter
- track 2 bits to distinguish between cases:
	1. jump is usually taken, but not taken last time
	2. jump not taken the last several times
![[Screenshot 2024-11-25 at 10.53.41 PM.png]]
##### Branch Target Buffer
- cache for branch targets
- necessary since branch predicting happens before decoding the instruction
- used to:
	1. look up instruction and identify target address for next instruction
	2. branch predict without checking for jump based on previously stored info
![[Screenshot 2024-11-25 at 11.01.03 PM.png]]