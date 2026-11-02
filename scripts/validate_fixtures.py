#!/usr/bin/env python3
"""Validate structure of the synthetic retry/idempotency fixture corpus."""
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED={"id","title","category","status","description","assumptions","events","expected","failure_modes","notes"}
def main():
    errors=[]; seen=set(); paths=sorted((ROOT/"fixtures").glob("*.json"))
    if not paths: errors.append("No fixture files found")
    for p in paths:
        try: data=json.loads(p.read_text(encoding="utf-8"))
        except Exception as e: errors.append(f"{p.name}: invalid JSON: {e}"); continue
        if not isinstance(data,dict): errors.append(f"{p.name}: root must be object"); continue
        missing=REQUIRED-data.keys()
        if missing: errors.append(f"{p.name}: missing {sorted(missing)}"); continue
        fid=data["id"]
        if not isinstance(fid,str) or not fid: errors.append(f"{p.name}: id must be nonempty string")
        elif fid in seen: errors.append(f"{p.name}: duplicate id {fid}")
        else: seen.add(fid)
        if data["status"]!="draft": errors.append(f"{p.name}: status must be draft")
        if not isinstance(data["events"],list) or not data["events"]: errors.append(f"{p.name}: events must be nonempty list")
        if not isinstance(data["assumptions"],list): errors.append(f"{p.name}: assumptions must be list")
        if not isinstance(data["expected"],dict): errors.append(f"{p.name}: expected must be object")
        if not p.name.startswith(str(fid)): errors.append(f"{p.name}: filename should start with id {fid}")
    if errors:
        print("Validation failed:"); [print(" - "+e) for e in errors]; return 1
    print(f"Validated {len(paths)} draft fixtures ({len(seen)} unique IDs)."); return 0
if __name__=="__main__": sys.exit(main())
