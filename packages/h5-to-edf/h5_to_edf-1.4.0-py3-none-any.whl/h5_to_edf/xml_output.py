# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import h5py
from xml.dom import minidom
import xml.etree.cElementTree as ET

from .converter import H5Handler
from .converter import Config


def make_xml(scan: H5Handler, config: Config):
    print("Creation of the .xml file")
    assert scan.current is not None
    with h5py.File(scan.h5_name, "r") as h5:
        tomo = ET.Element("tomo")

        acquisition = ET.SubElement(tomo, "acquisition")

        # beamline = ET.SubElement(acquisition, "beamline")
        # beamline.text = "BM18"

        # nameExp = ET.SubElement(acquisition, "nameExp")
        # nameExp.text = "tomo"

        scanName = ET.SubElement(acquisition, "scanName")
        scanName.text = scan.sample_name

        # disk = ET.SubElement(acquisition, "disk")
        # disk.text = "some vlaue2"

        date = ET.SubElement(acquisition, "date")
        date.text = h5[scan.group_scan + "/end_time"].asstr()[()]

        machineMode = ET.SubElement(acquisition, "machineMode")
        machineMode.text = h5[
            scan.group_scan + "/instrument/machine/filling_mode"
        ].asstr()[()]

        machineCurrentStart = ET.SubElement(acquisition, "machineCurrentStart")
        machineCurrentStart.text = str(
            h5[scan.group_scan + "/instrument/machine/current"][()]
        )

        machineCurrentStop = ET.SubElement(acquisition, "machineCurrentStop")
        machineCurrentStop.text = str(scan.current.get(scan.scan_epoch[-1]))

        # insertionDeviceName = ET.SubElement(acquisition, "insertionDeviceName")
        # insertionDeviceName.text = "some value1"

        # insertionDeviceGap = ET.SubElement(acquisition, "insertionDeviceGap")
        # insertionDeviceGap.text = "some vlaue2"

        # filter = ET.SubElement(acquisition, "filter")
        # filter.text = "some value1"

        # monochromatorName = ET.SubElement(acquisition, "monochromatorName")
        # monochromatorName.text = "some vlaue2"

        energy = ET.SubElement(acquisition, "energy")
        energy.text = str(h5[scan.group_scan + "/technique/scan/energy"][()])

        tomo_N = ET.SubElement(acquisition, "tomo_N")
        tomo_N.text = str(h5[scan.group_scan + "/technique/scan/tomo_n"][()])

        ref_On = ET.SubElement(acquisition, "ref_On")
        ref_On.text = str(h5[scan.group_scan + "/technique/scan/flat_on"][()])

        ref_N = ET.SubElement(acquisition, "ref_N")
        ref_N.text = str(h5[scan.group_scan + "/technique/scan/flat_n"][()])

        dark_N = ET.SubElement(acquisition, "dark_N")
        dark_N.text = str(h5[scan.group_scan + "/technique/scan/dark_n"][()])

        if len(scan.flat) > 0:
            y_Step = ET.SubElement(acquisition, "y_Step")
            y_Step.text = str(h5[scan.flat[0] + "/technique/flat/displacement"][()])

        # ccdtime = ET.SubElement(acquisition, "ccdtime")
        # ccdtime.text = "some vlaue2"

        # scanDuration = ET.SubElement(acquisition, "scanDuration")
        # scanDuration.text = "some value1"

        distance = ET.SubElement(acquisition, "distance")
        distance.text = str(
            h5[scan.group_scan + "/technique/scan/sample_detector_distance"][()]
        )

        sourceSampleDistance = ET.SubElement(acquisition, "sourceSampleDistance")
        sourceSampleDistance.text = str(
            h5[scan.group_scan + "/technique/scan/source_sample_distance"][()]
        )

        scanRange = ET.SubElement(acquisition, "scanRange")
        scanRange.text = str(h5[scan.group_scan + "/technique/scan/scan_range"][()])

        scanType = ET.SubElement(acquisition, "scanType")
        scanType.text = h5[scan.group_scan + "/technique/scan/scan_type"].asstr()[()]

        # realFinalAngles = ET.SubElement(acquisition, "realFinalAngles")
        # realFinalAngles.text = "some vlaue2"

        opticsName = ET.SubElement(acquisition, "opticsName")
        opticsName.text = h5[scan.group_scan + "/technique/optic/name"].asstr()[()]

        scintillator_path = scan.group_scan + "/technique/optic/scintillator"
        if scintillator_path in h5:
            scintillator = ET.SubElement(acquisition, "scintillator")
            scintillator.text = h5[scintillator_path].asstr()[()]

        cameraName = ET.SubElement(acquisition, "cameraName")
        cameraName.text = scan.cameratype

        cameraBinning = ET.SubElement(acquisition, "cameraBinning")
        cameraBinning.text = str(
            h5[scan.group_scan + f"/technique/detector/{scan.detector}/binning"][()]
        )

        # cameraFibers = ET.SubElement(acquisition, "cameraFibers")
        # cameraFibers.text = "some vlaue2"

        pixelSize = ET.SubElement(acquisition, "pixelSize")
        pixelSize.text = str(
            h5[scan.group_scan + f"/technique/detector/{scan.detector}/pixel_size"][()]
        )

        # ccdMode = ET.SubElement(acquisition, "ccdMode")
        # ccdMode.text = "some vlaue2"

        # projectionSize = ET.SubElement(acquisition, "projectionSize")
        # projectionSize.text = "some value1"

        listMotors = ET.SubElement(acquisition, "listMotors")
        listMotors.text = "motors"

        # ccdstatus = ET.SubElement(acquisition, "ccdstatus")
        # ccdstatus.text = "some value1"

        dom = minidom.parseString(ET.tostring(tomo))
        xml_str = dom.toprettyxml(indent="\t")
        outname = os.path.join(scan.dataset_output, f"{scan.sample_name}_.xml")
        if not config.dry_run:
            with open(outname, "w") as fout:
                fout.write(xml_str)
