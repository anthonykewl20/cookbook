#!/usr/bin/env python3
"""Deterministic scorer for the Molecular Gastronomy self-proof battery.

Reads the fixed ground truth (groundtruth.json) and one or more cook output
files, matches each cook's TRUE/FALSE verdict to the planted label, and prints
per-cook and per-arm accuracy / sensitivity / specificity. No judgment: the
labels are fixed before any cook runs; this only string-matches verdicts.

Cook output format expected (one verdict line per claim):
    C1: TRUE -- <evidence...>
    C2: FALSE -- <evidence...>
The scorer reads only "C<n>: TRUE|FALSE" (case-insensitive); evidence is ignored.
"""
import json, re, sys, glob, os

HERE = os.path.dirname(os.path.abspath(__file__))
GT = json.load(open(os.path.join(HERE, "groundtruth.json")))
LABELS = {c["id"]: c["truth"] for c in GT["claims"]}
N = len(LABELS)
VERDICT_RE = re.compile(r'(C\d)\s*[:\-]\s*(TRUE|FALSE)', re.IGNORECASE)

def parse(path):
    found = {}
    for line in open(path):
        m = VERDICT_RE.search(line)
        if m:
            cid, v = m.group(1).upper(), m.group(2).upper()
            if cid in LABELS and cid not in found:
                found[cid] = (v == "TRUE")
    return found

def score(found):
    correct = sum(1 for cid, pred in found.items() if pred == LABELS[cid])
    answered = len(found)
    tp = sum(1 for cid, pred in found.items() if LABELS[cid] and pred)       # true, said true
    fn = sum(1 for cid, pred in found.items() if LABELS[cid] and not pred)    # true, said false
    tn = sum(1 for cid, pred in found.items() if not LABELS[cid] and not pred) # false, said false
    fp = sum(1 for cid, pred in found.items() if not LABELS[cid] and pred)     # false, said true
    n_true = sum(1 for t in LABELS.values() if t)
    n_false = N - n_true
    return dict(answered=answered, correct=correct, accuracy=correct/N,
                sensitivity=(tp/n_true) if n_true else None,
                specificity=(tn/n_false) if n_false else False_claim_reject_rate(tn, n_false))

def False_claim_reject_rate(tn, n_false):
    return tn/n_false if n_false else None

def main():
    paths = sys.argv[1:]
    if not paths:
        paths = sorted(glob.glob(os.path.join(HERE, "runs", "*.txt")))
    rows = []
    for p in paths:
        f = parse(p)
        s = score(f)
        s["cook"] = os.path.basename(p)
        s["missing"] = sorted(set(LABELS) - set(f))
        rows.append(s)
    # print per cook
    print(f"{'cook':28} {'acc':>6} {'sens':>6} {'spec':>6} {'miss':>5}")
    for r in rows:
        sens = f"{r['sensitivity']:.2f}" if r['sensitivity'] is not None else "  na"
        spec = f"{r['specificity']:.2f}" if r['specificity'] is not None else "  na"
        print(f"{r['cook']:28} {r['accuracy']:.2f}   {sens}   {spec}   {len(r['missing'])}")
    # per-arm aggregate by filename prefix (process_* / baseline_*)
    for arm in ("process", "baseline"):
        arm_rows = [r for r in rows if r["cook"].startswith(arm)]
        if arm_rows:
            acc = sum(r["accuracy"] for r in arm_rows)/len(arm_rows)
            print(f"  {arm:10} mean accuracy = {acc:.2f} (n={len(arm_rows)})")
    if any(r for r in rows if r["cook"].startswith("process")) and any(r for r in rows if r["cook"].startswith("baseline")):
        p = sum(r["accuracy"] for r in rows if r["cook"].startswith("process"))/max(1, sum(1 for r in rows if r["cook"].startswith("process")))
        b = sum(r["accuracy"] for r in rows if r["cook"].startswith("baseline"))/max(1, sum(1 for r in rows if r["cook"].startswith("baseline")))
        print(f"  LIFT (process - baseline) = {p-b:+.2f}")

if __name__ == "__main__":
    main()
