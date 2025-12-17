"""
Brownian motion trajectory processing utilities.

This module loads trajectory data from .mat or .dat files (four columns: frame, x, y, z),
computes step statistics, mean squared displacement (MSD), and estimates the diffusion
coefficient from the MSD slope.

Example usage:
    python brownian_analysis.py --input data/traj.mat --dt 0.033 --max-lag 50

The script prints key statistics and optionally writes CSV outputs for MSD and steps.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Tuple

import numpy as np

try:
    import scipy.io as sio
except ImportError:  # pragma: no cover - dependency availability varies
    sio = None


@dataclass
class TrajectoryStatistics:
    """Container for trajectory analysis results."""

    time_lags: np.ndarray
    msd: np.ndarray
    diffusion_coefficient: float
    mean_step: float
    step_std: float


def _load_mat(path: Path) -> np.ndarray:
    if sio is None:
        raise ImportError("scipy is required to load .mat files; install scipy and retry.")

    data = sio.loadmat(path)
    candidates = [value for value in data.values() if isinstance(value, np.ndarray)]
    matrices = [c for c in candidates if c.ndim == 2 and c.shape[1] >= 4]
    if not matrices:
        raise ValueError(
            f"No suitable 2D array with at least four columns found in {path}."
        )
    if len(matrices) > 1:
        matrices.sort(key=lambda m: m.shape[0], reverse=True)
    return matrices[0]


def _load_dat(path: Path) -> np.ndarray:
    try:
        return np.loadtxt(path)
    except Exception as exc:  # pragma: no cover - I/O errors depend on environment
        raise ValueError(f"Failed to read {path}: {exc}") from exc


def load_trajectory(path: Path) -> Tuple[np.ndarray, np.ndarray]:
    """Load trajectory data from a .mat or .dat file.

    Returns a tuple of (frames, positions) where frames are integers and positions is
    an (N, 3) array for x/y/z coordinates.
    """

    suffix = path.suffix.lower()
    if suffix == ".mat":
        raw = _load_mat(path)
    elif suffix == ".dat":
        raw = _load_dat(path)
    else:
        raise ValueError("Unsupported file type. Use a .mat or .dat file.")

    if raw.ndim != 2 or raw.shape[1] < 4:
        raise ValueError("Input must be a 2D array with four columns: frame, x, y, z.")

    frames = np.asarray(raw[:, 0], dtype=int)
    positions = np.asarray(raw[:, 1:4], dtype=float)
    return frames, positions


def compute_displacements(positions: np.ndarray) -> np.ndarray:
    """Return step vectors between successive positions."""

    if positions.shape[0] < 2:
        return np.empty((0, positions.shape[1]))
    return positions[1:] - positions[:-1]


def compute_msd(positions: np.ndarray, max_lag: int) -> Tuple[np.ndarray, np.ndarray]:
    """Compute mean squared displacement for lags from 1..max_lag."""

    n = positions.shape[0]
    if n < 2:
        raise ValueError("Need at least two points to compute MSD.")

    max_lag = min(max_lag, n - 1)
    msd = np.empty(max_lag)
    time_lags = np.arange(1, max_lag + 1)

    for lag in time_lags:
        diffs = positions[lag:] - positions[:-lag]
        msd[lag - 1] = np.mean(np.sum(diffs ** 2, axis=1))
    return time_lags, msd


def estimate_diffusion_coefficient(time_lags: np.ndarray, msd: np.ndarray, dims: int) -> float:
    """Estimate diffusion coefficient using MSD slope: MSD ≈ 2*d*D*Δt."""

    if time_lags.size < 2:
        raise ValueError("Need at least two MSD points to estimate diffusion coefficient.")

    slope, _ = np.polyfit(time_lags, msd, 1)
    return slope / (2 * dims)


def summarize_trajectory(
    positions: np.ndarray, dt: float, max_lag: int, fit_points: int | None = None
) -> TrajectoryStatistics:
    """Compute MSD and diffusion coefficient for a trajectory."""

    dims = positions.shape[1]
    displacements = compute_displacements(positions)
    step_lengths = np.linalg.norm(displacements, axis=1)
    mean_step = float(np.mean(step_lengths)) if step_lengths.size else 0.0
    step_std = float(np.std(step_lengths)) if step_lengths.size else 0.0

    lags, msd = compute_msd(positions, max_lag)
    time_lags = lags * dt

    if fit_points is None or fit_points <= 1 or fit_points > len(time_lags):
        fit_slice = slice(None)
    else:
        fit_slice = slice(0, fit_points)

    diffusion_coefficient = estimate_diffusion_coefficient(
        time_lags[fit_slice], msd[fit_slice], dims
    )

    return TrajectoryStatistics(
        time_lags=time_lags,
        msd=msd,
        diffusion_coefficient=float(diffusion_coefficient),
        mean_step=mean_step,
        step_std=step_std,
    )


def _write_csv(path: Path, headers: Iterable[str], rows: np.ndarray) -> None:
    header_line = ",".join(headers)
    np.savetxt(path, rows, delimiter=",", header=header_line, comments="")


def run_cli(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Path to .mat or .dat file")
    parser.add_argument("--dt", type=float, default=1.0, help="Time spacing between frames")
    parser.add_argument(
        "--max-lag",
        type=int,
        default=50,
        help="Maximum lag (in frames) for MSD computation",
    )
    parser.add_argument(
        "--fit-points",
        type=int,
        default=10,
        help="Number of initial points to fit for diffusion coefficient (<= max-lag)",
    )
    parser.add_argument(
        "--msd-csv", type=Path, default=None, help="Optional path to write MSD values (CSV)"
    )
    parser.add_argument(
        "--steps-csv",
        type=Path,
        default=None,
        help="Optional path to write step lengths (CSV)",
    )

    args = parser.parse_args(list(argv))

    frames, positions = load_trajectory(args.input)
    stats = summarize_trajectory(positions, dt=args.dt, max_lag=args.max_lag, fit_points=args.fit_points)

    print(f"Loaded {positions.shape[0]} points from {args.input}")
    print(f"Frame range: {frames.min()}–{frames.max()}" if frames.size else "Frame range: n/a")
    print(f"Mean step length: {stats.mean_step:.6f}")
    print(f"Step length std: {stats.step_std:.6f}")
    print("Estimated diffusion coefficient (D): {:.6f}".format(stats.diffusion_coefficient))

    if args.msd_csv is not None:
        msd_rows = np.column_stack((stats.time_lags, stats.msd))
        _write_csv(args.msd_csv, headers=["delta_t", "msd"], rows=msd_rows)
        print(f"MSD values written to {args.msd_csv}")

    if args.steps_csv is not None:
        displacements = compute_displacements(positions)
        step_lengths = np.linalg.norm(displacements, axis=1)
        step_rows = step_lengths.reshape(-1, 1)
        _write_csv(args.steps_csv, headers=["step_length"], rows=step_rows)
        print(f"Step lengths written to {args.steps_csv}")

    return 0


def main() -> None:
    try:
        exit_code = run_cli(sys.argv[1:])
    except Exception as exc:  # pragma: no cover - defensive CLI entry point
        print(f"Error: {exc}", file=sys.stderr)
        exit_code = 1
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
