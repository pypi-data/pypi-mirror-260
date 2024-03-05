# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import h5py
from .converter import H5Handler
from .converter import Config


def make_info(scan: H5Handler, config: Config):
    with h5py.File(scan.h5_name, "r") as h5:
        ref_on = scan.tomo_n
        n_flat = h5[scan.group_scan + "/technique/scan/flat_n"][()]
        energy = h5[scan.group_scan + "/technique/scan/energy"][()]
        distance = h5[scan.group_scan + "/technique/scan/sample_detector_distance"][()]
        scan_range = h5[scan.group_scan + "/technique/scan/scan_range"][()]
        dark_n = h5[scan.group_scan + "/technique/scan/dark_n"][()]
        if len(scan.flat) > 0:
            y_step = h5[scan.flat[0] + "/technique/flat/displacement"][()]
        else:
            y_step = 0
        dim = h5[scan.group_scan + f"/technique/detector/{scan.detector}/size"][()]
        tomo_exptime = h5[scan.group_scan + "/technique/scan/exposure_time"][()]
        latency_time = h5[scan.group_scan + "/technique/scan/latency_time"][()]
        roi = h5[scan.group_scan + f"/technique/detector/{scan.detector}/roi"][()]
        try:
            acq_mode = h5[
                scan.proj_scan + f"/instrument/{scan.detector}/acq_parameters/acq_mode"
            ][()]
            max_expo = h5[
                scan.proj_scan
                + f"/instrument/{scan.detector}/ctrl_parameters/acc_max_expo_time"
            ][()]
            count_time = h5[
                scan.proj_scan
                + f"/instrument/{scan.detector}/acq_parameters/acq_expo_time"
            ][()]
            acq_frame = max(count_time / max_expo, 1)
        except Exception:
            acq_mode = ""
            acq_frame = ""
            max_expo = ""
        col_end = roi[0]
        col_beg = roi[1]
        row_end = roi[2]
        row_beg = roi[3]
        pixelsize = h5[scan.group_scan + "/technique/optic/sample_pixel_size"][()]
        date = str(h5[scan.group_scan + "/start_time"][()])
        srcurrent = h5[scan.group_scan + "/instrument/machine/current"][()]
        try:
            comment = str(h5[scan.group_scan + "/technique/scan/comment"][()])
        except Exception:
            comment = ""

        print("Creation of the .info file")
        infofile = os.path.join(scan.dataset_output, scan.dataset_name + "_.info")
        if os.path.isfile(infofile):
            h5 = open(infofile, "r")
            lines = [line.strip("\n") for line in h5.readlines()]
        else:
            lines = [""] * 40

        lines[1] = "Energy= " + str(energy)
        lines[2] = "Distance= " + str(distance)
        lines[3] = "Prefix= " + scan.dataset_name
        lines[4] = "Directory= " + scan.dataset_output
        lines[5] = "ScanRange= " + str(scan_range)
        lines[6] = "TOMO_N= " + str(ref_on)
        lines[7] = "REF_ON= " + str(ref_on)
        lines[8] = "REF_N= " + str(n_flat)
        lines[9] = "DARK_N= " + str(dark_n)
        lines[10] = "Y_STEP= " + str(y_step)
        lines[11] = "Dim_1= " + str(dim[0])
        lines[12] = "Dim_2= " + str(dim[1])
        lines[13] = "Count_time= " + str(tomo_exptime / 1000)
        lines[14] = "Latency_time (s)= " + str(latency_time / 1000)
        lines[16] = "Col_end= " + str(col_end)
        lines[17] = "Col_beg= " + str(col_beg)
        lines[18] = "Row_end= " + str(row_end)
        lines[19] = "Row_beg= " + str(row_beg)
        lines[21] = "PixelSize= " + str(pixelsize)
        lines[22] = "Optic_used= " + str(pixelsize)
        lines[23] = "Date= " + str(date[2:-1])
        lines[26] = "SrCurrent= " + str(f"{srcurrent:.3f}")
        lines[29] = "Acq_mode= " + str(acq_mode)
        lines[30] = "Acq_nb_frame= " + str("1")
        lines[31] = "Acq_orig= " + str(acq_frame)
        lines[32] = "Max_expo_time= " + str(max_expo)
        lines[38] = "Comment= " + str(comment[2:-1])

        if not config.dry_run:
            with open(infofile, "w") as fout:
                for line in lines:
                    fout.write(line + "\n")
