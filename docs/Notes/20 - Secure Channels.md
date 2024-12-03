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
![[Screenshot 2024-11-12 at 2.50.39 PM.png | center | 500]]

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