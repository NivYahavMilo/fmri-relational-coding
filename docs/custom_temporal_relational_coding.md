# Custom Temporal Relational Coding (Moving Windows)

Detailed reference for the moving-window relational coding experiment that probes how short temporal segments of task-related activity align with nearby rest windows. This method generalizes the whole-brain relational coding flow by explicitly averaging over configurable task and rest windows before computing the correlation-distance metric.

---

> **Architecture note.** This write-up predates the "flatten-flows" refactor. The
> algorithm is unchanged, but the class hierarchy under
> `relational_coding/custom_temporal_relational_coding/` dispatched through
> `FlowManager` has been replaced by plain functions: shared algorithms (including
> `custom_temporal_relational_coding` and `correlate_current_timepoint`) live in
> `rc_core.py`, data loaders in `data_access.py`, and the per-analysis orchestration
> in `flows/custom_temporal.py`, `flows/snr.py`, and `flows/concat.py` (each a
> top-level `run(...)`). Paths come from `settings.py`. References below to
> `FlowManager`, `CustomTemporalRelationalCoding(Utils)`, `RelationalCodingBase`, or
> `config` map onto these.

## Code Map

- Driver helpers (looping over ROIs, window grids, filtering combos): `main.py`
  - `custom_temporal_relational_coding_for_specific_roi`
  - `custom_temporal_relational_coding`
  - `moving_window_custom_temporal_relational_coding`
  - `moving_window_custom_temporal_relational_coding_with_signal_processing`
  - or the CLI: `python -m cli custom-temporal ...` / `moving-window ...` / `moving-window-sp ...`
- Analysis module: `flows/custom_temporal.py::run` (subject vs. averaged flow)
- Core algorithm + window logic: `rc_core.py` (`custom_temporal_relational_coding`, `get_task_window_slides_vectors`, `get_rest_window_slides_vectors`, `correlate_current_timepoint`)
- Data loaders: `data_access.py`

Representative snippets:

```60:69:flows/custom_temporal.py
def run(roi, **kwargs):
    init_window_task = kwargs.pop('init_window_task')
    ws_task = kwargs.pop('task_window_size')
    ws_rest = kwargs.pop('rest_window_size')
    avg_data = kwargs.pop('average_data', False)
    if avg_data:
        _avg_flow(roi=roi, init_window_task=init_window_task, ws_task=ws_task, ws_rest=ws_rest, **kwargs)
        return
    _subject_flow(roi=roi, init_window_task=init_window_task, ws_task=ws_task, ws_rest=ws_rest, **kwargs)
```

```rc_core.py
def custom_temporal_relational_coding(*, data_task, data_rest, window_size_rest,
                                      init_window_task, window_size_task, **kwargs):
    ...
    rc_distance, _ = correlate_current_timepoint(data=custom_temporal_window_vec, **kwargs)
    ...
```

---

## Inputs and Data Shapes

| Component | Format / Dimensions | Notes |
| --- | --- | --- |
| ROI tabular data per subject | DataFrame with columns `feat_0 … feat_{n}`, plus `timepoint`, `y`, optional `Subject`. Each row represents one TR. | Same preprocessed tables used by the standard relational coding flow; stored under `Schaefer2018_SUBNET_{mode}_DF`. |
| Average ROI data | Loaded from `Schaefer2018_SUBNET_AVG_{mode}` when `average_data=True`. | Typically group-averaged across selected subjects (group suffix `_GROUPi`). |
| Window parameters | `rest_window_size=(start_tr, end_tr)`, `task_window_size=int`, `init_window_task` ∈ {`'start'`, `'end'`, `'middle'`, `'dynamic'`, `'moving_window_from_end'`, `'shuffle'`} | Provided by helper functions or CLI kwargs. |
| Optional controls | `shuffle_rest`, `filtering`, `decomposition`, `movie_distances`, `window_moving_size`, `window_range`, `group_subjects`, `group_index`, `skip_correlation`, etc. | Passed through `FlowManager` into the core algorithm and down to `correlate_current_timepoint`. |

Typical dimensionalities:

- **Rest window**: sliding range on `[0, 29]` TR indices (default loops 5-TR width inside `[0, 30)`).
- **Task window size**: fixed at 10 TRs in provided scripts; can be changed per call.
- **Feature count**: ROI-dependent (number of voxels mapped to that ROI).
- **Group sampling** (SNR variant): `group_subjects` subjects averaged per group; group indices iterate `1..6`.

---

## Processing Stages

### 1. Entry Points / Scheduling

1. `main.py` helper selects ROIs (single or all), sets default windows (`task_ws=10`, rest windows sweeping), and repeats across init-window modes (commonly `'end'`).
2. For each ROI+window configuration, `FlowManager.execute(..., flow_type=FlowType.CUSTOM_TEMPORAL_RELATIONAL_CODING)` is invoked, forwarding kwargs like `average_data`, `shuffle`, `filtering`, `decomposition`, or signal-processing hyperparameters (cut-off, order).

### 2. Subject vs. Average Flow

- **Subject-specific** (`CustomTemporalRelationalCoding.__subject_flow`):
  - Loads per-subject task and rest tables via `load_roi_data`.
  - Builds output directory names encoding task/rest windows (e.g., `task_end_10_tr_rest_0-5_tr`).
  - Optional variants:
    - Shuffle rest flag toggles `'end'` → `'shuffle'` in path.
    - Filtering runs are stored under `custom_temporal_relational_coding_filtering`.
    - PCA runs use `custom_temporal_relational_coding_pca`.
  - Skips processing if a pickle already exists for the ROI+window combo.
  - Iterates over `StaticData.SUBJECTS`, computing a single RC distance per subject (because rest windows are fixed rather than per-TR loops). Saves `{subject_id: distance}`.

- **Average flow** (`__avg_flow`):
  - Loads ROI-level average task/rest data (`Mode.CLIPS` / `Mode.REST`) potentially keyed by group suffix.
  - Stores results under `custom_temporal_relational_coding_avg/task_<...>/roi.pkl`.
  - Saves `{'avg': distance}` for the ROI; caching logic avoids recomputation.

### 3. Windowed Vector Construction

Implemented in `CustomTemporalRelationalCodingUtils.custom_temporal_relational_coding`:

1. Initialize dict `custom_temporal_window_vec`.
2. For each clip index `1..14`:
   - `get_task_window_slides_vectors` selects TRs according to `init_window_task`:
     - `'start'`: first `window_size_task` TRs.
     - `'end'`: last `window_size_task` TRs (default used in scripts).
     - `'middle'`: symmetric window around midpoint.
     - `'dynamic'`: exact `(s, e)` tuple from `window_range`.
     - `'moving_window_from_end'`: sliding endpoint determined by `window_moving_size`.
     - `'shuffle'`: alias of `'end'` but typically paired with rest shuffling downstream.
   - Columns removed: `y`, `timepoint`, optional `Subject`.
   - Compute the mean across the selected TR bin, returning a feature vector (length = number of ROI voxels).
   - `get_rest_window_slides_vectors` slices the rest dataframe between `(start, end)` (exclusive of `end`), dropping metadata columns, and averages across TRs. If the rest recording for the clip ends before `end`, `_add_tr_from_next_clip` supplements with TRs from the next clip to keep window size consistent.
   - Vectors are stored under `<clip_name>_task` and `<clip_name>_rest`.

3. After looping through all clips:
   - If `skip_correlation=True`, return `(None, raw_dataframe)`; used by pipelines that only need the concatenated feature matrix (e.g., downstream SNR or distance analyses).
   - Otherwise, pass the dictionary into `RelationalCodingBase.correlate_current_timepoint`, forwarding kwargs such as `shuffle_rest`, `filtering`, `decomposition`, `movie_distances`, or `skip_correlation`.

### 4. Correlation Distance Computation

Identical core logic as the whole-brain experiment, described in `docs/whole_brain_fmri_relational_coding.md`:

1. Convert dictionary → DataFrame, reorder columns to `StaticData.CLIPS_ORDER + StaticData.REST_ORDER`.
2. Optional preprocessing:
   - `SignalProcessing.low_pass_filtering` (when `filtering=True`; order and cut-off from kwargs).
   - `Decomposition.reduce_dimensions` (PCA when `decomposition=True`).
   - `distances_utils.create_distances_movies_vector` (when `movie_distances=True`).
   - Rest shuffling ensures permutation controls.
3. Compute pairwise correlational structure, flatten task/rest quadrants, correlate flattened vectors to produce a single scalar distance.

Because each subject produces one vector per clip (already averaged across windows), there is one scalar output per subject per ROI per window combo.

### 5. Persistence and Artifacts

- Outputs live under directories configured in `settings.py`:
  - `FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS`
  - `FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_FILTERING`
  - `FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_PCA`
  - `FMRI_CUSTOM_TEMPORAL_RELATION_CODING_RESULTS_AVG`
- Filenames encode ROI names; directory names encode `task_<init>_<size>_tr_rest_<start>-<end>_tr`.
- Files are pickled dicts mapping a subject identifier (or `'avg'`) to the scalar relational coding distance. Additional metadata (e.g., raw window matrices) can be obtained by re-running with `skip_correlation=True`.

---

## Specialized Variants

| Variant | Additional Steps / Parameters | Files |
| --- | --- | --- |
| **Filtering** | Pass `filtering=True`, `filter_order`, `filter_cut_off`; default example in `moving_window_custom_temporal_relational_coding_with_signal_processing`. | Results stored under `custom_temporal_relational_coding_filtering/...`. |
| **PCA Reduction** | Set `decomposition=True`; optionally adjust `n_components` fraction in `Decomposition.reduce_dimensions`. | Saved under `custom_temporal_relational_coding_pca/...`. |
| **SNR Measurements** | Uses group-averaged data via `load_group_subjects`, sets `skip_correlation=False` but records intermediate features for distance analyses. See `flows/snr.py`. | Results under `MOVIE_DISTANCES_CORRELATION_ANALYSIS/...`. |
| **Concatenated Task Clips** | `flows/concat.py` reuses the same `rc_core` functions but concatenates multiple clips before averaging. | Stored under the concat-specific result directories in `settings`. |

---

## Execution Examples

### Single ROI, Default Windows

```python
import flows.custom_temporal as custom_temporal

custom_temporal.run(
    'RH_Vis_18',
    rest_window_size=(8, 13),   # TR 8–12
    init_window_task='end',
    task_window_size=10,
    average_data=False,
    shuffle_rest=False,
)
```
Equivalently from the CLI:
```bash
python -m cli custom-temporal --roi RH_Vis_18 --rest-start 8 --rest-end 13 --task-ws 10
```

### Moving Window Sweep with Filtering

```python
from main import moving_window_custom_temporal_relational_coding_with_signal_processing

moving_window_custom_temporal_relational_coding_with_signal_processing(
    roi='RH_Default_Temp_6',
    average_data=False,
    shuffle=False,
    filtering=True,
    decomposition=False,
    with_plot=True
)
```

This iterates the rest window in one-TR increments while keeping `task_ws=10`. Each iteration saves a new pickle, enabling temporal profiling of rest-task couplings.

---

## Practical Considerations

- **Caching**: Every ROI/window pair short-circuits if the destination pickle already exists. Delete older outputs when re-running with different parameters.
- **Data Continuity**: When rest recordings do not cover the requested window (common near clip boundaries), `_add_tr_from_next_clip` supplements with subsequent clip TRs. This maintains consistent vector lengths but can slightly blur clip identities near the seams.
- **Normalization Hooks**: The code includes commented-out z-scoring lines (`z_score(rest_window_avg, axis=0)`). Activating them would require verifying that `z_score` handles 1D inputs as expected.
- **Signal Processing Flags**: Filtering/PCA require additional kwargs; ensure `filter_order` and `filter_cut_off` are set when `filtering=True`, or `correlate_current_timepoint` will raise.
- **Parallelization**: The current helpers loop sequentially over ROIs and windows; for large runs, consider distributing by ROI or rest window.

---

## Output Interpretation

- Each stored scalar indicates how well the averaged task correlation structure aligns with the averaged rest structure within the specified window pairing. Higher correlations imply greater similarity (less differentiation) between rest and task within that temporal neighborhood.
- Aggregating across rest windows (by reading multiple pickles) can reveal when rest segments best predict nearby task activity, enabling temporal-localized relational analyses.


