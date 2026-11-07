import argparse
import json
from collections import Counter

from arsenal.aparare.parse_auth import citeste_esecuri


def suspecti(counts, prag=10):
    """Intoarce lista de (ip, n) cu n >= prag, sortata descrescator dupa n."""
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return sorted(
        ((ip, n) for ip, n in counts.items() if n >= prag),
        key=lambda pereche: pereche[1],
        reverse=True,
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = Counter(e["ip"] for e in esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts.most_common()),
            "suspecti": [{"ip": ip, "incercari": n} for ip, n in sus],
        }
        print(json.dumps(raport, indent=2))
    else:
        print("Esecuri de autentificare:", len(esecuri))
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip}  ({n} incercari)  BRUTE FORCE")


if __name__ == "__main__":
    main()
