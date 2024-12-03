##### Using Symmetric Encryption
- symmetric encryption is much faster and better at supporting larger messages
- real protocols use both asymmetric and symmetric encryption
	- use asymmetric as little as possible
	- use symmetric for everything else
- **hybrid encryption**: use asymmetric encryption to setup symmetric encryption
##### Key Agreement
- A has B’s public encryption key, want to choose shared secret

1. both sides generate random values (similar to private key)
2. derive “key shares” from values (similar to public key)
3. use math to combine “key shares”

**DIffie-Hellman Key Agreement**
1. A chooses random value Y
2. A sends public value derived from Y (“key share”)
3. B chooses random value Z
4. B send public value derived from Z (“key share”)
5. A combines Y with public value from B to get number
6. B combines Z with public value from A to get number
##### Typical TLS Handshake
![[Screenshot 2024-11-16 at 4.36.42 PM.png]]

**After Handshake**
- use symmetric encryption
- use key share results to get **several** keys
	- take hash(something + shared secret) to derive each key
- separate keys for each direction (server → client, client → server), encryption, and MAC
- messages use encryption + MAC + nonces

**TLS Provides:**
- confidentiality/authenticity
	- only client/server can read
	- client knows they are talking to a specific server based on certificate
	- server knows client doesn’t change during connection
- forward secrecy
	- can’t decrypt old conversations (data for KeyShares is temporary)
- speed
	- most communication done with efficient symmetric ciphers
	- 1 sets of messages back and forth to set up connection
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