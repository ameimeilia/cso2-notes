---
layout: default
title: Out-of-Order
parent: Notes
nav_order: 13
---
# Out-of-Order
{: .highlight }
Slides: [ooo](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/ooo.pdf), [bpred](https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/bpred.pdf)
## Instruction Queue and Dispatch
- iterate through instruction queue each cycle and determine which instructions can be run
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 9.19.18 PM.png' | relative_url}}" alt="Screenshot">
</div>

- more common to have specialized execution units
- issue stage matches instructions to execution units that can run them
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 9.30.38 PM.png' | relative_url}}" alt="Screenshot">
</div>
## Execution Units/Functional Units
- where actual work of instruction is done, e.g. the actual ALU, or data cache
- sometimes pipelined:
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-21 at 2.17.11 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>

*exercise*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-21 at 2.24.21 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>

- sometimes unpipelined:
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-21 at 2.24.48 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## Instruction Queue and Dispatch (multicycle)
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 9.53.30 PM.png' | relative_url}}" alt="Screenshot">
</div>
## Register Renaming: Missing Pieces
- deal with “hidden” inputs such as `%rsp`, condition codes?
- solution: translate to instructions with additional register parameters
	- making `%rsp` explicit parameter
	- turning hidden condition codes into operands
- can also translate complex instructions to simpler ones
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-21 at 2.32.41 PM.png' | relative_url}}" alt="Screenshot">
</div>
## OOO Limitations
- can’t always find instructions to run
- need to track all uncommitted instructions
- branch misprediction has a big cost (relative to pipelined)
## Importance of Prediction
- predicting a jump is always not taken/stalling both result in 2 wasted cycles for each jump taken
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.03.02 PM.png' | relative_url}}" alt="Screenshot" width="400">
</div>
- additionally, stalling also results in 2 wasted cycles for each jump not taken
- correct branch prediction has a very big impact on performance
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 11.10.42 PM.png' | relative_url}}" alt="Screenshot" width="500">
</div>
## Static Branch Prediction
- forward not taken, backward taken
- if the target of the jump is greater than the PC, assume the jump is not taken
- if the target of the jump is less than the PC, assume the jump is taken
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.13.07 PM.png' | relative_url}}" alt="Screenshot" width="300">
</div>

*example - predict same as last*
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.27.33 PM.png' | relative_url}}" alt="Screenshot">
</div>
## Collisions
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
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.44.21 PM.png' | relative_url}}" alt="Screenshot">
</div>

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.49.30 PM.png' | relative_url}}" alt="Screenshot">
</div>

<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.50.59 PM.png' | relative_url}}" alt="Screenshot">
</div>
## 2-bit Saturating Counter
- track 2 bits to distinguish between cases:
	1. jump is usually taken, but not taken last time
	2. jump not taken the last several times
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 10.53.41 PM.png' | relative_url}}" alt="Screenshot">
</div>
## Branch Target Buffer
- cache for branch targets
- necessary since branch predicting happens before decoding the instruction
- used to:
	1. look up instruction and identify target address for next instruction
	2. branch predict without checking for jump based on previously stored info
<div style="text-align: center;">
  <img src="{{ '/images/Screenshot 2024-11-25 at 11.01.03 PM.png' | relative_url}}" alt="Screenshot">
</div>