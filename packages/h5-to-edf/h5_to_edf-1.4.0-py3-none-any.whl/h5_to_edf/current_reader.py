# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import h5py
import numpy
import datetime
import pathlib


class CurrentReader:
    """
    Access to the current information from epoch time.
    """

    def __init__(self):
        self._time = []
        self._current = []

    def set_values(self, time, current):
        time = numpy.array(time)
        current = numpy.array(current)
        assert len(time) == len(current)
        assert numpy.all(time[:-1] <= time[1:])
        self._time = time
        self._current = current

    def read_from_h5(self, scan_root: h5py.Group):
        self._current = scan_root["measurement/current"][()]
        self._time = scan_root["measurement/epoch"][()]

    def read_esrf_current_file(self, filename: str | pathlib.Path):
        filename = str(filename)
        timestamp = []
        current = []
        with open(filename, "rt") as f:
            line = next(f)
            if line.strip() != "# File generated from hdbviewer application":
                raise IOError(f"Wrong header file: {line}")
            line = next(f)
            if line.strip() != "#":
                raise IOError(f"Wrong header file: {line}")
            line = next(f)
            if (
                line.strip()
                != "HDB Date\tHDB Time\tsrdiag/beam-current/total/current (mA)"
            ):
                raise IOError(f"Wrong header file: {line}")
            for line in f:
                if line.startswith("#"):
                    continue
                line = line.strip()
                t, c = line.rsplit("\t", 1)
                t2 = datetime.datetime.strptime(t, "%d/%m/%Y\t%H:%M:%S")
                t2 = t2.replace(tzinfo=datetime.timezone.utc)
                timestamp.append(t2.timestamp())
                current.append(float(c))
        self.set_values(timestamp, current)

    def get(self, epoch: float) -> float:
        """
        Get a current value from an epoch time.
        """
        i = numpy.searchsorted(self._time, epoch)
        if i == 0:
            return self._current[0]
        if i >= len(self._current):
            return self._current[-1]
        if abs(self._time[i - 1] - epoch) < abs(self._time[i] - epoch):
            return self._current[i - 1]
        return self._current[i]
