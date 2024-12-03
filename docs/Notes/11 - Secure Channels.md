---
layout: default
title: Secure Channels
parent: Notes
nav_order: 11
---
# Secure Channels
> [!note]
> Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/secure.pdf
##### Secure Communication Context
- communication on a network between **principals** (people/servers/programs)

**Running Example: A to B**
- A talking with B and sometimes also with C
- attacker E: eavesdropper, passive, reads all messages over network
- attacker M: machine in the middle, active, gets to read/replace/add messages on the network
	- assume A and B have a *shared secret* they both know that M does not know

**Possible Security Properties**
1. *confidentiality*: information shared only with those who should have it
2. *authenticity*: message genuinely comes from the right principal without manipulation
3. repudiation: if A sends message to B, B can’t prove to C it came from A
4. forward-secrecy: if A gets compromised, E can’t use that to decode past conversations with B
5. anonymity: A can talk to B without knowing who it is
##### Symmetric Encryption
- two functions:
	1. encrypt: `E(key, message) = ciphertext`
	2. decrypt: `D(key, ciphertext) = message`
- key = shared secret
- should be **hard to learn anything about the message** without the key
- also want to **resist any recovery** of information about the message/key

**Usage**
1. A and B share encryption key in advance
2. A computes `E(key, message) = ciphertext`
3. A sends `[sequence_of_bytes]` to B on the network
4. B computes `D(key, ciphertext) = message`

**Encryption is not Enough**
- symmetric encryption provides confidentiality but **not authenticity**
- an active attacker M can *selectively* manipulate the encrypted message
- attacker can flip bits to change messages, shorten messages, corrupt selected parts messages
##### Message Authentication Codes (MACs)
- goal: use shared secret *key* to verify message origin
- `MAC(key, message) = tag
- knowing `MAC`, the message, and the tag, it should be hard to:
	1. find the value of `MAC(key, other_message)` → “forge” the tag
	2. find the key

**MAC vs Checksum**
- checksum can be recomputed without any key
- checksum is meant to protect against accidents, not malicious attacks
- checksum can be faster to compute + shorter

**Using MAC Without Encryption**
1. choose + share MAC key in advance
2. A computes the message, and also `MAC(MAC key, message) = ciphertext`
3. A sends the message and the `ciphertext` to B
4. B recomputes `MAC(MAC key, message) = ciphertext` and rejects if the `ciphertext` doesn’t match

**Using MAC With Encryption, “Authenticated Encryption”**
1. choose + share encryption key and MAC key in advance
2. A computes `E(key, message) = ciphertext1` and `MAC(MAC key, ciphertext1) = ciphertext2`
3. A sends `ciphertext1` and `ciphertext2` to B
4. B recomputes `MAC(MAC key, ciphertext1)` and rejects if it doesn’t match `ciphertext2` 
5. B computes `D(key, ciphertext1) = message`

*exercise*
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-11-10 at 1.45.53 AM.png | relative_url }}" alt="Screenshot" width="500">
</div>
##### Asymmetric Encryption
- two functions:
	1. public encrypt: `PE(public_key, message) = ciphertext`
	2. public decrypt: `PD(private_key, ciphertext) = message`
- `(public_key, private_key)` = key pair
- should be hard to find the message knowing `PE`, `PD`, the public key, and the ciphertext
- should not be able to find the `private_key` knowing `PE`, `PD`, the public key, the ciphertext, and the message

**Key Pairs**
- `private_key`: kept secret, not shared with anyone
- `public_key`: safe to give to everyone

**Using**
1. B generates `private_key` + `public_key`
2. B sends`public_key` to A securely
3. A computes `PE(public_key, message) = ciphertext`
4. A sends `ciphertext` to B on the network
5. B computes `PD(private_key, ciphertext) = message`

**Asymmetric vs Symmetric Encryption**
*both*:
- use secret data to generate key(s)

*asymmetric (public-key) encryption*
- one key pair per recipient
- private key kept by recipient
- public key sent to all potential senders
- encryption is one-way without private key

*symmetric encryption*
- one key per (recipient + sender)
- secret key kept by recipient + sender
- if you can encrypt, you can decrypt
##### Digital Signatures
- pair of functions:
	1. sign: `S(private_key, message = signature`
	2. verify: `V(public_key, signature, message) = 1`
- `(public_key, private_key)` = key pair, similar to asymmetric encryption
- knowing `S`, `V`, `public_key`, `message`, `signature` will be hard to find new messages/signatures

**Using**
1. A generates a `private_key` + `public_key` in advance
2. A send `public_key` to B securely
3. A computes `S(private_key, message) = signature`
4. A sends the `message` and the `signature` to B
5. B computes `V(public_key, message, signature) = 1`
##### Replay Attacks
- attacker can copy/paste an earlier message with the same signature
- solution: add context with **nonces** (number used once)
- generate random/unique number where each subsequent message uses the number from the previous message → protects against changing numbers
- also include context about **who is sending**, either:
	- include who is sending + other context so message can’t be reused
	- use unique set of keys for each principal
##### Other Attacks
**TLS State Machine Attack**
- protocol
	1. verify server identity
	2. receive messages from server
- attack:
	- if server sends “here’s your next message” instead of “here’s my identity” then a broken client ignores verifying the server’s identity

**Matrix vulnerabilities**
- protocol + goals
	1. each device has public keys
	2. to talk to a device, verify one of the public keys
	3. to add devices, client can forward other devices’ public keys
- bugs
	- when receiving new keys, clients did not check who they were forwarded from
##### Certificates
1. A has B’s public key
2. C wants B’s public key and knows A’s
3. A can generate a certificate for B
	- “B’s public key is *** ”
	- Sign(A’s private key, “B’s public key is *** ”)
4. B sends a copy of their certificate to C
5. if C trusts A, C now has B’s public key
	- if C does not trust A, can’t trust B’s public key

**Certificate Authorities**
- websites go to certificate authorities (CA) with their public key
- CA sign messages called certificates
- send certificates to browsers to verify identity
	- websites can forward certificate instead of browser contacting CA directly

**Certificate Hierarchy**
<div style="text-align: center;">
  <img src="{{ Screenshot 2024-11-12 at 2.50.39 PM.png | relative_url }}" alt="Screenshot" width="500">
</div>

**Public-key infrastructure**
- ecosystem with CA and certificates for everyone
- certificates for:
	- verifying identity of websites
	- verifying origin of domain name records
	- verifying origin of applications in some OSes/app stores/etc. 
	- …

**CA/Browser Forum**
- made up of CA + everyone who ships code with list of valid CA
- organization that sets rules for how website certificates verify identity
- CA chooses a random value and either:
	1. sends it to domain contact (with domain registrar) and receive response with it
	2. observes it placed in DNS or website or send from server in other specific way
- public CAs are also required to:
	- keep private keys in tamper-resistant hardware
	- maintain publicly-accessible database of revoked certificates
	- maintain certificate transparency: must keep public logs of every certificate issued
##### Cryptographic Hash Functions
- `hash(M) = X`
- given `X`: hard to find message other than by guessing
- given `X`, `M`: hard to find second message `M2` so that `hash(M2) = X`
- example uses:
	- substitute for original message in digital signature (especially for signing very large messages)
	- building MACs

**Password Hashing**
- cryptographic hash functions need guessing to “reverse”
- idea: store cryptographic hash of password instead of password
	- attacker who gets hash doesn’t get password
	- can still check if entered password is correct
- use slow/resource-intensive cryptographic hash functions to slow down guessing
##### “Secure” Random Numbers
- properties:
	- attack cannot guess number better than chance
	- knowing prior “random” numbers shouldn’t help predict next “random” numbers
	- compromised machine shouldn’t reveal older random numbers

**/dev/urandom**
- Linux kernel RNG
- collects “entropy” form hard-to-predict events
	- e.g. exact timing of I/O interrupts
	- e.g. some processor’s built-in random number circuit
- turned into as many random bytes as needed

**Turning “Entropy” into Random bytes**
- example idea:
	- interval variable state
	- to add “entropy”: state ← SecureHash(state + entropy)
	- to extract value:
		- random bytes ← SecureHash(1 + state), give bytes that can’t be reversed to compute state
		- state ← SecureHash(2 + state), change state so can’t return to old state if compromised
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