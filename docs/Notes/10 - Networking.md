
> [!note]
> Slides: https://www.cs.virginia.edu/~cr4bd/3130/F2024/slides/network.pdf
##### Networks Review
**Mailbox Abstraction**
- send/receive messages
![[Screenshot 2024-11-06 at 3.18.56 PM.png | center | 500]]
- essentially how the “raw” Internet is implemented
- sockets are implemented on top of this

**Sockets/Connections**
- set up explicit connection then information can be sent on the connection
![[Screenshot 2024-11-06 at 5.38.59 PM.png | center | 500]]
##### Layers
![[Screenshot 2024-11-06 at 5.42.28 PM.png | center | 500]]
- application layer is built atop the transport layer which is built atop the network layer…
##### Network Limitations/Failures
- messages can be:
	- lost
	- delayed/reordered
	- limited in size
	- corrupted

**Handling Lost Message**
- Machine B sends an acknowledgement message to Machine A when the message is received
- Machine A picks a limit to the amount of time it is willing to wait for the acknowledgement
- if Machine A reaches the limit, it “times out” and attempts to send the message again
![[Screenshot 2024-11-06 at 6.01.12 PM.png | center | 500]]
- if Machine B’s acknowledgement message gets lost:
	- Machine A should resend the message (which follow the original protocol)
	- Machine B will need to be able to handle receiving multiple messages
![[Screenshot 2024-11-06 at 6.01.44 PM.png | center | 500]]

**Handling Delayed Messages**
- Machine A times out before the message reaches Machine B, so the message is resent
- OR Machine A times out before receiving the acknowledgement 
- Machine A needs to be able to handle possibly receiving multiple acknowledgements

*delayed message*
![[Screenshot 2024-11-06 at 6.06.12 PM.png | center | 500]]

*delayed acknowledgement*
![[Screenshot 2024-11-06 at 6.03.42 PM.png | center | 500]]

**Handling Message Size Limitations**
- solution: split up message
- Machine B must be able to identify the correct parts of the message
- Machine A must be able to identify the correct acknowledgements
![[Screenshot 2024-11-06 at 6.21.46 PM.png | center | 500]]

**Handling Message Corruption**
- send message + hashed message
- when receiving, recompute hash and check if match
- no match = message lost
- hashes are commonly called **checksums**
##### 4+ Layers
- often there are more layers above the “application” layer in inconsistent way
- eg.
	- HTTPS on TLS on TCP…
	- DNS on HTTPS on TLS on TCP…
	- SFTP on SSH on TCP…
##### Names and Addresses
- used to specify machine
![[Screenshot 2024-11-09 at 8.48.13 PM.png]]

*example - an Ethernet frame*
![[Screenshot 2024-11-09 at 8.57.41 PM.png]]
##### The Network Layer
- Internet Protocol (IP) v4 or v6 in common use today

**IPv4**
- 32-bit numbers
- *example*: `128.143.67.11`
	- four 8-bit decimal values separated by `.`
	- same as: $128 \cdot 256^3 + 142 \cdot 256^2 + 67 \cdot 256 + 11 = 2 156 782 459$
- organizations get blocks of IPs
	- eg. UVA has `128.143.0.0 - 128.143.255.255`

**IPv6**
- 128-bit numbers
- written in hex, 16-bit parts, separated by colons
- strings of 0s represented by double-colons
- typically given in blocks of $2^{80}$ or $2^{64}$ addresses
##### IPv4 Addresses and Routing Tables
![[Screenshot 2024-11-09 at 9.15.08 PM.png | center | 450]]

**Selected Special IPv4 addresses**
- `127.0.0.0 - 127.255.255.255`: local host/loopback
	- typically only `127.0.0.1` is used
- `192.168.0.0 - 192.168.255.255`, `10.0.0.0 - 10.255.255.255`, `176.16.0.0 - 172.32.255.255`
	- “private IP addresses”
	- not used on the Internet
	- commonly connected to Internet with **network address translation**
- `169.254.0.0 - 169.254.255.255`
	- link-local addresses
	- never forwarded by routers
##### Port Numbers in the Transport Layer
- used to identify individual programs/connections
- 16-bit port numbers
- `0 - 49151`: typically assigned for particular services
	- `80` = HTTP, `443` = HTTPS, `22` = SSH
- `49152 - 65535`: allocated on demand
	- default “return address” for client connecting to server
##### User Datagram Protocol (UDP) vs Transmission Control Protocol (TCP)
**TCP**: reliability/streams to other program
- **reliable** transmission of **as much data as you want**
- “connecting” fails if server not responding
- `write(fd, "a", 1); write(fd, "b", 1)` equal to `write(fd, "ab", 2)`
- one socket per remote program being talked to

**UDP**: messages sent to program, not no reliability/streams
- **unreliable** transmission of **short messages**
- “connecting” just sets default destination
- `write(fd, "a", 1); write(fd, "b", 1)` not equal to `write(fd, "ab", 2)`
- can send/receive multiple programs with one socket
##### Connections
**Connections in TCP/IP**
- connection identified by 5-tuple:
	- protocol=TCP/UDP, local IP address, local port, remote IP address, remote port
	- used by OS to lookup socket from table

![[Screenshot 2024-11-09 at 9.48.15 PM.png]]

**Non-connection Sockets**
- TCP servers waiting for connections
- UDP sockets with no articular remote host
- Linux: OS keeps 5-tuple with “wildcard” remote address
![[Screenshot 2024-11-09 at 9.52.00 PM.png]]
##### DNS: Distributed Database
- domain name system
- links addresses with names
![[Screenshot 2024-11-09 at 10.04.42 PM.png | center | 500]]
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