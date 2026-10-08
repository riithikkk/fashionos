import email, os, sys
from email import policy

path = sys.argv[1]
out = "mht_output"
os.makedirs(out, exist_ok=True)

with open(path, "rb") as f:
    msg = email.message_from_binary_file(f, policy=policy.default)

for i, part in enumerate(msg.walk()):
    if part.is_multipart():
        continue
    ctype = part.get_content_type()
    ext = {
        "text/html": ".html",
        "text/css": ".css",
        "application/javascript": ".js",
        "text/javascript": ".js",
        "application/x-javascript": ".js",
    }.get(ctype)
    if not ext:
        # keep images/fonts etc. too
        ext = "." + ctype.split("/")[-1].split("+")[0]
    data = part.get_payload(decode=True)
    if data:
        with open(os.path.join(out, f"file_{i}{ext}"), "wb") as f:
            f.write(data)
        print("saved", f"file_{i}{ext}", ctype)