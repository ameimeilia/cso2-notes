---
layout: default
title: Security
parent: readings
nav_order: 13
---
# Security
## 1 Four useful tools

### 1.1 Hashes
- **Hash function**: Converts any input into a fixed-size output. A change in input changes the output.
- **Cryptographically-secure hash function**: Hard to reverse; finding the input from the output requires random guessing.
### 1.2 Symmetric ciphers
- Pair of functions for encryption and decryption, both needing a secret key.
- Properties:
	- Produces ciphertext that conceals the original message.
	- Decryption undoes encryption with the correct key.
	- Without the key, decryption requires guessing.
- Vulnerable to **malleability** attacks, where bit flipping in ciphertext affects plaintext.
### 1.3 Message authentication codes and authenticated encryption
- Similar to a hash function but includes a secret key, producing a tag to verify the sender's identity.
- Ensures:
	- Tag generation from MAC function and key.
	- Hard to find another message with the same tag without the key.
- **Authenticated Encryption**: Combines symmetric encryption and MAC to prevent both unauthorized access and corruption.
### 1.4 Asymmetric ciphers
- Key pairs with one public key ($k_1$) for encryption and one private key ($k_2$) for decryption.
- Properties:
	- Only $k_2$ can decrypt messages encrypted with $k_1$.
	- Determining $k_2$ or the message from public key info is difficult.
- Should be randomized to prevent attackers from predicting encrypted outcomes of small message sets.
### 1.5 Digital Signatures
- Provides message verification with signing (s) and verifying (v) functions.
- Properties:
	- Signing creates a signature with the private key, verifiable by the public key.
	- Forging signatures without the private key is hard.
- Signature schemes and asymmetric encryption use **trapdoor functions** (easy to compute in one direction, difficult in the other without a private key).
### 1.6 Diffie-Hellman Key Exchange
- Allows two parties to agree on a shared secret without revealing it to eavesdroppers.
- Steps:
    - 1. Agree (in public) on an initial random number $g$
	1. Each (privately, without telling anyone at all) pick a second random number, their private key
	2. Each applies the operator to $g$ and their key, sharing the result (in public) with the others
	3. Each applies the operator to what they received and their key to attain their shared secret

| person A knows | shared publicly | person B knows |
| -------------- | --------------- | -------------- |
|                | $f,g$           |                |
| $a$            |                 | $b$            |
|                | $f(g,a),f(g,b)$ |                |
| $f(f(g,b),a)$  |                 | $f(f(g,a),b)$  |
### 1.7 Cryptographically-secure random numbers
- **Need for Secure Randomness**: Essential for security, ensuring unpredictability despite knowledge of generating code.
- **Pseudo-Random Generators**: Most software RNGs are deterministic and predictable if internal state is known.
- **Cryptographically-Secure Generators**:
	- Rely on **entropy harvesting** (e.g., timing of keystrokes, mouse movement).
	- **Entropy pools** managed by OS; may run low if demand is high.
## 2 Using the tools

### 2.1 Signatures
- **Task**: Verify a document's approval by an individual.
- **Solution**: Individual signs a document hash with their private key.
    - Verification: Check if digital signature verification function returns true.
### 2.2 Should I trust you?
- **Task**: Prove identity to someone unknown.
- **Solution**:
    1. A trusted third party signs a certificate containing your public key.
    2. Present the certificate.
    3. The verifier encrypts a random number with your public key; you decrypt and return it to confirm identity.
- **Application**: Certificate authorities (CAs) issue certificates; a two-part process includes certificate presentation and proof of private key possession.
### 2.3 Storing passwords
- **Task**: Store password securely, inaccessible even to the root account.
- **Solution**: Store only the password's hash.
    - **Rainbow Table Attack**: Prevent by **salting** passwords.
    - **Web Passwords**: Often less secure, transmitted as plaintext; browsers save raw passwords for autofill.
    - **Better Practice**: Use a password manager to encrypt and generate unique passwords.
### 2.4 Let’s talk privately
- **Task**: Establish private communication with a new contact in public.
- **Solution**: Use **Diffie-Hellman** for symmetric key exchange.
    - **Protocol**: Secure multi-step setup, commonly via TLS.
    - **TLS Flow**:
        1. Browser and server exchange Diffie-Hellman public keys, generating shared keys for encryption.
        2. Server sends a signed certificate to confirm identity.
        3. Server signs a hash of prior messages for verification.
        4. Browser validates the certificate, verifies integrity, and starts secure communication.
## 3 Pitfalls of cryptographic protocols
- Secure cryptographic functions can lead to flaws if not used carefully for encryption and authentication.
### 3.1 Symmetric encryption but not authentication
- **Issue**: Encrypted messages alone don’t prevent tampering.
    - Attackers can guess parts of the encrypted content and potentially modify it (e.g., changing an amount in a payment).
- **Solution**: Use message authentication codes (MACs) to verify integrity.
### 3.2 Public key encryption but not authentication
- **Issue**: Public-key encryption allows anyone to encrypt a message to a public key.
    - An attacker could impersonate a sender by encrypting a message to the recipient's public key, altering the content.
- **Solution**: Require digital signatures to confirm the sender's identity.
### 3.3 Replay attacks
- **Issue**: An attacker can resend signed and encrypted messages (e.g., a payment request), causing repeated actions.
- **Solution**: Use **nonces** (unique numbers) or sequence numbers to track and prevent message duplication.
### 3.4 Other attacks, prevention
- **Examples**:
    - **Asymmetric Decryption Vulnerability**: If A proves identity by decrypting B’s message, B could use A’s decryption for messages from others.
    - **Verification Skipping**: A system might skip verifying the other party in certain cases, leaving it open to attack.
- **Best Practice**: Use machine-checked proofs to validate protocol security properties, as manual verification is error-prone.