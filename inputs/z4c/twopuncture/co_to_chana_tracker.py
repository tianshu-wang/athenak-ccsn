#!/usr/bin/env python3
"""Convert AthenaK's bbh.co_0.txt / bbh.co_1.txt (M units) into chana's
puncture_tracker.txt layout (seconds and cm at M = 3.0e5 cm), so
analyze_binary_puncture.py --reference-tracker can read it.

    python3 co_to_chana_tracker.py bbh.co_0.txt bbh.co_1.txt \
        puncture_tracker_athenak.txt
"""
import sys
import numpy as np

M_CM = 3.0e5
M_S = 1.00069228559445614e-05   # one M of coordinate time at M = 3.0e5 cm


def load(path):
    # columns: 1:iter 2:time 3:x 4:y 5:z 6:vx 7:vy 8:vz
    d = np.loadtxt(path, comments="#")
    return d[:, 1], d[:, 2:5]


def main():
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    t0, p0 = load(sys.argv[1])
    t1, p1 = load(sys.argv[2])
    n = min(len(t0), len(t1))
    if not np.allclose(t0[:n], t1[:n]):
        raise SystemExit("the two tracker files are not sampled at the same times")
    # co_0 starts at +x, which is chana's puncture 1.
    rows = np.column_stack([t0[:n] * M_S, p0[:n] * M_CM, p1[:n] * M_CM])
    header = ("puncture tracker -- AthenaK CompactObjectTracker output, converted\n"
              "from M units at M = 3.0e5 cm.\n"
              "npunctures = 2\n"
              "time_s x1_cm y1_cm z1_cm x2_cm y2_cm z2_cm")
    np.savetxt(sys.argv[3], rows, fmt="%.17e", header=header)
    print(f"wrote {n} samples to {sys.argv[3]} (t = {t0[0]:g} .. {t0[n - 1]:g} M)")


if __name__ == "__main__":
    main()
