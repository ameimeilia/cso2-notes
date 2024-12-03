##### Privilege Levels
- vulnerable code runs with higher privileges
- there are other common cases of higher privilege besides kernel mode
	- ex. scripts in web browsers
##### JavaScript
- scripts in webpages
- not supposed to be able to read arbitrary memory, but:
	- can access arrays to examine caches
	- could take advantage of some browser function being vulnerable
	- **could supply vulnerable code itself**
##### Just-in-time Compilation
- for performance, compiled to machine code, run in browser
- not supposed to access arbitrary browser memory