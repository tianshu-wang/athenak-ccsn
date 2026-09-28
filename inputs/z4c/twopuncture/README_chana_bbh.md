# Binary puncture matched to chana

`z4c_bbh_chana.athinput` evolves the equal-mass quasicircular Bowen-York
binary of chana's `binary_puncture` run (Hannam et al. 2010 data) to t = 37 M,
on the same grid, so the two codes' puncture tracks can be compared.  The
header of the input file lists what is matched and what cannot be.

## Build

TwoPunctures is a submodule and must be built before AthenaK; it needs GSL
(`gsl-config` on the PATH, e.g. `module load gsl`).

```sh
git clone --recursive git@github.com:tianshu-wang/athenak-ccsn.git
cd athenak-ccsn
# or, in an existing clone: git submodule update --init --recursive

(cd twopuncturesc && make)          # -> twopuncturesc/lib/libTwoPunctures.a

# GPU (A100 shown; set the Kokkos arch for the device)
cmake -S . -B build-bbh -DPROBLEM=z4c_two_puncture \
      -DKokkos_ENABLE_CUDA=ON -DKokkos_ARCH_AMPERE80=ON
cmake --build build-bbh -j
```

## Run

```sh
mkdir run && cd run
../build-bbh/src/athena -i ../inputs/z4c/twopuncture/z4c_bbh_chana.athinput
```

Time a short run first (`time/nlim=50` on the command line) and scale by the
~5500 cycles to `tlim = 37`.

Memory: AthenaK preallocates `<mesh_refinement>/max_nmb_per_rank` MeshBlocks
(16000 in the input).  The run starts at 12236 blocks of 8^3 with 4 ghost
layers; a reduced CPU test measured roughly 1-2 MB per allocated block plus a
fixed overhead, so expect ~20-30 GB.  Lower `max_nmb_per_rank` only as far as
the block count allows: the run aborts if AMR needs more blocks than it.

## Output

`bbh.co_0.txt` (starts at +x) and `bbh.co_1.txt` (starts at -x), columns
`iter t x y z vx vy vz` in M.  Convert them to chana's tracker layout for
`analyze_binary_puncture.py --reference-tracker`:

```sh
python3 ../inputs/z4c/twopuncture/co_to_chana_tracker.py \
    bbh.co_0.txt bbh.co_1.txt puncture_tracker_athenak.txt
```
