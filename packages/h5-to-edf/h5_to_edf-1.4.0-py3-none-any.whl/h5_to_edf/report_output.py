# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import h5py
import datetime
from .converter import H5Handler
from .converter import Config


def make_report(scan: H5Handler, config: Config):
    report_list = []
    with h5py.File(scan.h5_name, "r") as h5:
        # name
        report_list.append(h5[scan.group_scan + "/technique/scan/name"][()])
        # date
        report_list.append(h5[scan.group_scan + "/end_time"][()])
        # pixel size
        report_list.append(
            h5[scan.group_scan + "/technique/optic/sample_pixel_size"][()]
        )
        # energy
        report_list.append(h5[scan.group_scan + "/technique/scan/energy"][()])
        # current
        report_list.append(h5[scan.group_scan + "/instrument/machine/current"][()])
        # proj number
        report_list.append(h5[scan.group_scan + "/technique/scan/tomo_n"][()])
        # duration
        end = h5[scan.group_scan + "/end_time"][()]
        start = h5[scan.group_scan + "/start_time"][()]
        end = datetime.datetime.fromisoformat(end.decode())
        start = datetime.datetime.fromisoformat(start.decode())
        duration = end - start
        duration_sec = duration.seconds
        report_list.append(duration_sec)
        report_list.append(duration_sec / 60)
        # xc
        xc = scan.group_scan + "/instrument/positioners/xc"
        report_list.append(xc)
        # sx
        sx = scan.group_scan + "/instrument/positioners/sx"
        report_list.append(sx)
        # sy
        sy = scan.group_scan + "/instrument/positioners/sy"
        report_list.append(sy)
        # sz
        sz = scan.group_scan + "/instrument/positioners/sz"
        report_list.append(sz)
        # yrot
        yrot = scan.group_scan + "/instrument/positioners/yrot"
        report_list.append(yrot)
        # HA
        # ???yrot/pixel_size
        # ct
        report_list.append(h5[scan.group_scan + "/technique/scan/exposure_time"][()])
        # range
        report_list.append(h5[scan.group_scan + "/technique/scan/scan_range"][()])
        # size proj
        size = h5[scan.group_scan + f"/technique/detector/{scan.detector}/size"][()]
        report_list.append(size[0])
        report_list.append(size[1])
        # camera name
        report_list.append(
            h5[scan.group_scan + f"/technique/detector/{scan.detector}/name"][()]
        )
        # acq mode
        report_list.append(
            h5[scan.proj_scan + f"/instrument/{scan.detector}/acq_parameters/acq_mode"][
                ()
            ]
        )
        # Accumulation
        # ??? exp_time/subframe
        # Scintillator
        report_list.append(h5[scan.group_scan + "/technique/optic/scintillator"][()])
        # comments
        report_list.append(h5[scan.group_scan + "/technique/scan/comment"][()])

    print(report_list)
    return report_list
