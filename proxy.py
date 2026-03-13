import sys, io, os, json, base64, hashlib
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

if len(sys.argv) != 3:
    print("Use: proxy.py <SUPABASE_URL> <ANON_KEY>", file=sys.stderr)
    sys.exit(4)

SUPABASE_URL = sys.argv[1].rstrip("/")
ANON_KEY = sys.argv[2]

def sha256sum(path):
    try:
        with open(path, "rb") as f:
            h = hashlib.sha256()
            while chunk := f.read(8192):
                h.update(chunk)
            return h.hexdigest()
    except Exception as e:
        print(f"ERR: hash failed for {path}: {e}", file=sys.stderr)
        return None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
proxy_path = os.path.join(BASE_DIR, "proxy.py")
eden_path = os.path.join(BASE_DIR, "edenQuests.pl")

hash_proxy = sha256sum(proxy_path) or "missing"
hash_eden = sha256sum(eden_path) or "missing"

CLIENT_TAG = "hwid_disabled"

def call_rpc_get_macro(supabase_url, anon_key, hwid, hash_proxy, hash_eden):
    url = supabase_url.rstrip("/") + "/rest/v1/rpc/get_macro_for_client"
    headers = {
        "apikey": anon_key,
        "Authorization": "Bearer " + anon_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"p_hwid": hwid, "p_proxy_hash": hash_proxy, "p_eden_hash": hash_eden}
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=20) as resp:
            body = resp.read().decode('utf-8')
            j = json.loads(body)
            return j
    except HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            print("HTTPError RPC:", e.code, body, file=sys.stderr)
        except:
            print("HTTPError RPC:", e.code, file=sys.stderr)
        return {"error": f"http_{e.code}"}
    except URLError as e:
        print("URLError RPC:", e, file=sys.stderr)
        return {"error": "url_err"}
    except Exception as e:
        print("ERR RPC:", e, file=sys.stderr)
        return {"error": "err"}

res = call_rpc_get_macro(SUPABASE_URL, ANON_KEY, CLIENT_TAG, hash_proxy, hash_eden)
if not res:
    print("ERR: empty rpc response", file=sys.stderr)
    sys.exit(5)

if res.get("error"):
    print("ERR from rpc:", res["error"], file=sys.stderr)
    sys.exit(3)

b64_text = res.get("content_base64")
if not b64_text:
    print("ERR: no content", file=sys.stderr)
    sys.exit(6)

try:
    decoded = base64.b64decode(b"".join(b64_text.encode('ascii', errors='ignore').split()))
    sys.stdout.buffer.write(decoded)
    sys.exit(0)
except Exception as e:
    print(f"ERR: failed decode or output: {e}", file=sys.stderr)
    sys.exit(6)
