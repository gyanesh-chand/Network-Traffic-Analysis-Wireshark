from binascii import unhexlify
import base64
import gzip
import zlib
import json

payload = "2730223b1f2c50272f285532503b2a57303b5654565219"
data = unhexlify(payload)

flags = ("flag{", "ctf{", "thm{", "htb{", "picoctf{")

print("[*] Testing all XOR keys...\n")

for key in range(256):
    decoded = bytes(b ^ key for b in data)

    try:
        text = decoded.decode("utf-8")
    except UnicodeDecodeError:
        continue

    # Only show mostly printable text
    if sum(32 <= ord(c) <= 126 for c in text) < len(text) * 0.8:
        continue

    print("=" * 50)
    print(f"Key : {key}")
    print("Text:", repr(text))

    # Flag detection
    if any(f in text.lower() for f in flags):
        print("[+] Possible FLAG found!")

    # JSON detection
    try:
        print("[+] Valid JSON")
        print(json.loads(text))
    except:
        pass

    # Base64 detection
    try:
        print("[+] Looks like Base64")
        print(base64.b64decode(text, validate=True))
    except:
        pass

    # Gzip detection
    try:
        print("[+] GZIP")
        print(gzip.decompress(decoded))
    except:
        pass

    # Zlib detection
    try:
        print("[+] ZLIB")
        print(zlib.decompress(decoded))
    except:
        pass