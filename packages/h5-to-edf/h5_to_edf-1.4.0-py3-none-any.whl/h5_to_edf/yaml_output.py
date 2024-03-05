# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import h5py
import numpy as np
from .converter import H5Handler
from .converter import Config

try:
    import yaml
except ImportError:
    yaml = None


def make_yaml(scan: H5Handler, config: Config):
    """
    Create a YAML file from an HDF5 file.

    Parameters:
        scan: Description of the scan
        config: Global configuration
    """
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")

    if not scan.h5_name.endswith(".h5"):
        raise ValueError("The input file is not a .h5 file")

    print("Creation of the .yml file")

    with h5py.File(scan.h5_name, "r") as h5:
        # Get acquisition parameters
        detector = scan.detector
        count_time = _safe_hdf5_read(
            h5, scan.proj_scan + f"/instrument/{detector}/acq_parameters/acq_expo_time"
        )
        max_expo = _safe_hdf5_read(
            h5,
            scan.proj_scan
            + f"/instrument/{detector}/ctrl_parameters/acc_max_expo_time",
        )

        # Create the YAML data structure
        data = {
            "tomo": {
                "acquisition": {
                    "scanName": _safe_hdf5_read(h5, scan.group_scan + "/sample/name"),
                    "date": _safe_hdf5_read(h5, scan.group_scan + "/end_time"),
                    "beamline": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/saving/beamline"
                    ),
                    "machineMode": _safe_hdf5_read(
                        h5, scan.group_scan + "/instrument/machine/filling_mode"
                    ),
                    "machineCurrentStart": _safe_hdf5_read(
                        h5, scan.group_scan + "/instrument/machine/current"
                    ),
                    "machineCurrentStop": float(scan.current.get(scan.scan_epoch[-1])),
                    "distance": str(
                        round(
                            float(
                                _safe_hdf5_read(
                                    h5,
                                    scan.group_scan
                                    + "/technique/scan/sample_detector_distance",
                                )
                            ),
                            2,
                        )
                    ),
                    "sourceSampleDistance": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/source_sample_distance"
                    ),
                    "energy": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/energy"
                    ),
                    "tomo_N": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/tomo_n"
                    ),
                    "ref_On": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/flat_on"
                    ),
                    "ref_N": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/flat_n"
                    ),
                    "dark_N": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/dark_n"
                    ),
                    "scanRange": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/scan_range"
                    ),
                    "scanType": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/scan_type"
                    ),
                    "half_acquisition": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/half_acquisition"
                    ),
                    "comment": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/comment"
                    ),
                    "nb_scans": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/nb_scans"
                    ),
                    "delta_z": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/scan/delta_pos"
                    ),
                    "opticsName": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/optic/name"
                    ),
                    "scintillator": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/optic/scintillator"
                    ),
                    "magnification": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/optic/magnification"
                    ),
                    "cameraType": _safe_hdf5_read(
                        h5, scan.group_scan + f"/technique/detector/{detector}/type"
                    ),
                    "cameraBinning": _safe_hdf5_read(
                        h5, scan.group_scan + f"/technique/detector/{detector}/binning"
                    ),
                    "pixelSize": _safe_hdf5_read(
                        h5, scan.group_scan + "/technique/optic/sample_pixel_size"
                    ),
                    "roi_size": _safe_hdf5_read(
                        h5, scan.group_scan + f"/technique/detector/{detector}/size"
                    ),
                    "acq_mode": _safe_hdf5_read(
                        h5,
                        scan.proj_scan
                        + f"/instrument/{detector}/acq_parameters/acq_mode",
                    ),
                    "expo_time": count_time,
                    "subframe": max_expo,
                    "latency_time": _safe_hdf5_read(
                        h5, scan.proj_scan + "/technique/proj/latency_time"
                    ),
                    "accumulation": float(max(count_time / max_expo, 1)),
                    "scan_time": float(scan.scan_time[-1]),
                }
            }
        }

        # Create a dictionary of motors
        motors = {}
        for name in h5[scan.group_scan + "/instrument/positioners/"].keys():
            motors[name] = _safe_hdf5_read(
                h5, scan.group_scan + f"/instrument/positioners/{name}"
            )
        data["tomo"]["acquisition"]["motors"] = motors

        # Save the YAML file
        outname = os.path.join(scan.dataset_output, f"{scan.sample_name}_.yml")
        if not config.dry_run:
            with open(outname, "w") as yamlfile:
                yaml.safe_dump(
                    data, yamlfile, default_flow_style=False, sort_keys=False
                )


def _safe_hdf5_read(hdf_file, key, default=None):
    """
    Read a value from an HDF5 file and return a safe representation of the value.

    Parameters:
    hdf_file (h5py.File): The HDF5 file object.
    key (str): The key to read from the HDF5 file.
    default (any): The default value to return if the key is not found.

    Returns:
    The value associated with the key, or the default value if the key is not found.
    """
    try:
        value = hdf_file[key][()]
        if isinstance(value, bytes):
            return value.decode("utf-8")
        elif isinstance(value, (float, np.float64, np.float32, np.int64)):
            return float(value)
        else:
            return str(value)
    except KeyError:
        return default
