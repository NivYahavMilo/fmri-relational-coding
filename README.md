# fMRI Relational Coding

Statistical analysis of fMRI brain signals from the Human Connectome Project (HCP)
7T movie-watching and resting-state data. The code quantifies **relational coding** —
how similarly a region's voxel-activity pattern responds to narrative movie clips
versus nearby resting-state segments — at the voxel, ROI, and network level using the
Schaefer-2018 300-ROI / 7-network atlas.

> This repository accompanies ongoing, unpublished research. It describes the
> algorithms and how to run them; it intentionally contains no findings or citations.

## What it computes

Each analysis reduces a region's task and rest responses to per-clip pattern vectors,
correlates them, and summarizes the task-vs-rest relationship as a scalar **relational
distance**. The analyses differ in how the task/rest windows are selected and aggregated:

| Analysis | CLI command | Idea |
| --- | --- | --- |
| Whole-brain relational coding | `relational-coding` | Task end-TR vs rest, swept across each rest TR, per subject or group average. |
| Singular relational coding | `singular` | Task end-TR vs the per-clip averaged rest vector. |
| Custom-temporal relational coding | `custom-temporal` | Sliding task/rest windows of configurable size. |
| Moving-window sweep | `moving-window` | Custom-temporal swept over a range of rest windows. |
| Moving-window + signal processing | `moving-window-sp` | Same, with optional low-pass filtering or PCA. |
| ISFC relational coding | `isfc` | Inter-subject functional correlation (leave-one-out rest average). |
| Activation patterns | `activations` | Per-clip activation-pattern correlations. |
| SNR / movie distances | `snr` | Relational distances across subject-group sizes. |

Algorithm write-ups live in [`docs/`](docs/):
- [`docs/whole_brain_fmri_relational_coding.md`](docs/whole_brain_fmri_relational_coding.md)
- [`docs/custom_temporal_relational_coding.md`](docs/custom_temporal_relational_coding.md)

## Layout

```
rc_core.py            # relational-coding algorithms as plain functions
data_access.py        # ROI / averaged / group data loaders
flows/                # one module per analysis, each exposing run(...)
main.py               # launcher functions (library API) + CLI entry point
cli.py                # argparse command-line interface over the launchers
settings.py           # paths + RC_* environment/.env overrides
flow_manager.py       # raw-data preprocessing pipeline dispatcher
arithmetic_operations/# correlation, standardization, distances, signal processing
data_normalizer/      # raw -> voxel -> ROI -> network preprocessing
visualizations/       # plotting helpers (opt-in, require seaborn/matplotlib)
tests/                # pytest suite (algorithms + config + CLI)
```

The analyses compose `rc_core` + `data_access` directly — there is no base class or
runtime dispatcher for them; call `flows.<analysis>.run(...)` (or use the CLI).

## Setup

Dependencies are managed with [uv](https://docs.astral.sh/uv/). Version pins mirror the
validated study environment (Python 3.9); results depend on them, so avoid bumping.

```bash
uv sync                 # create the environment from pyproject.toml + uv.lock
uv run pytest           # run the test suite
```

## Configuration

Input tables and results live outside the repo. `settings.py` reads three overrides
(from the environment or a local `.env`); copy the template and edit it:

```bash
cp .env.example .env
```

| Variable | Default | Meaning |
| --- | --- | --- |
| `RC_DRIVE` | `/Volumes/My_Book` | Root of the external data drive. |
| `RC_DATA_DIR` | `<RC_DRIVE>/parcelled_data_niv` | Preprocessed input tables. |
| `RC_RESULTS_DIR` | `<RC_DRIVE>/fmri-relational-coding-results` | Where results are written. |

A full analysis run expects the preprocessed HCP tables (produced by the
`data_normalizer` pipeline) to already exist under those paths.

## Running an analysis

```bash
# one ROI, group-averaged, with plots
uv run python -m cli relational-coding --roi RH_Vis_18 --avg --plot

# a sliding-window analysis over all ROIs
uv run python -m cli custom-temporal --rest-start 6 --rest-end 16 --task-ws 10

# inter-subject functional correlation
uv run python -m cli isfc --plot
```

Omitting `--roi` runs the analysis over every ROI in `StaticData.ROI_NAMES`.
`python -m cli --help` (or `<command> --help`) lists all options. The same
functions are importable from `main.py` for use in notebooks/scripts.

## Testing

```bash
uv run pytest
```

The suite covers the core algorithms (analytic checks plus golden snapshots on
synthetic data), the settings/env overrides, and the CLI wiring. It uses only
synthetic fixtures, so it runs without the HCP data on disk.
