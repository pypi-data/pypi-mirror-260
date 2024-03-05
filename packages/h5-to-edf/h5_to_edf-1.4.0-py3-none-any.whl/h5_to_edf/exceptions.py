# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations


class ScanNotTerminated(Exception):
    """Raised when a processed scan is not yet closed

    Basically there is no `end_time`
    """

    def __init__(self, filename, group_name=None):
        self.filename = filename
        super(ScanNotTerminated, self).__init__(f"Scan {filename} group {group_name} not over")


class ScanNotSuccessed(Exception):
    """Raised when a processed scan was not properly terminated

    For example the writer have a FAILED status
    """

    def __init__(self, filename, group_name, status):
        self.filename = filename
        super(ScanNotSuccessed, self).__init__(f"Scan {filename} group {group_name} not successed ({status})")


class FileNotProducedByBliss(Exception):
    """Raised when a processed file was not created by BLISS
    """
