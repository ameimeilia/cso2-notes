##### URL/URIs
- Uniform Resource Locators (URL)
	- tells how to find “resource” on network
	- uniform: one syntax for identifying resources
- Uniform Resource Identifiers (URI)
	- superset of URLs

**URI Generally**
- `scheme://authority/path?query#fragment`

1. `scheme:`: what protocol
2. `//authority/`: user@host:port OR host:port OR user@host OR host
3. `path`: which resource
4. `?query`: key/value pairs
5. `#fragment`: place in resource (local, not part of request for service)

*examples*
- `https://kytos02.cs.virginia.edu:443/cs3130-spring2023/quizzes/quiz.php?qid=02#q2`
- `//www.cs.virginia.edu/~cr4bd/3130/S2023`: scheme implied from context
- `/~cr4bd/3130/S2023`: scheme/host implied from context
##### Auto-configuration
- often the local router machine runs a service to assign IP addresses to a machine
- the local router:
	- knows which IP addresses are available
	- sysadmin may configure in mapping from MAC addresses to IP addresses

**Dynamic Host Configuration Protocol (DHCP) High-level**
- protocol done over UDP, used to contact local router without using IP:
	1. use IP address `0.0.0.0` as source address and `255.255.255.255` as destination address
	2. contacts everyone on the local network
	3. local server is configured to reply to the request with an address + **time limit**
	4. later: can send messages to local server to renew/give up address
##### Network Address Translation
- IPv4 address are scarce → convert many private address to one public address
- outside POV: several machines share one public IP address
- inside POV: machines have different IP on private network

**Implementing NAT**
- use NAT translation table, managed by router
- add entries as connections are made and remove as connections are closed
![[Screenshot 2024-11-10 at 12.54.42 AM.png]]
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
![[Screenshot 2024-11-10 at 1.45.53 AM.png | center | 500]]
##### Asymmetric Encryption
- two functions:
	1. public encrypt: `PE(public_key, message) = ciphertext`
	2. public decrypt: `PE(private_key, ciphertext) = message`
- `(public_key, private_key)` = key pair
- should be hard to find the message knowing `PE`, `PD`, the public key, and the ciphertext
- should not be able to find the `private_key` knowing `PE`, `PD`, the public key, the ciphertext, and the message

**Key Pairs**
- `private_key`: kept secret, not shared with anyone
- `public_key`: safe to give to everyone

**Using**
1. 

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