# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

from __future__ import annotations

import os
import functools
import logging
import dataclasses

import numpy
import h5py
import fabio
from fabio.utils.cli import ProgressBar

from .edf_file_series import EdfFileSeries
from .current_reader import CurrentReader
from . import exceptions


LRU_CACHE_SIZE = 64

_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Config:
    """Contains the global configuration of the application"""

    root_directory: str | None
    """Root directory where the raw data is stored"""

    edf_directory: str
    """Root directory where to store output data"""

    report: bool
    """If true, a report is displayed but the data is not processed"""

    process_dark: bool
    """If true, darks are processed"""

    process_flat: bool
    """If true, darks are processed"""

    generate_yml: bool
    """If true, a yaml file is generated from the scan metadata"""

    generate_xml: bool
    """If true, a xmlfile is generated from the scan metadata"""

    dry_run: bool
    """If true, the processing is done without writing anything"""

    args: object
    """Raw parsed arguments from the command line"""

    current: CurrentReader | None
    """External resource to reach the current"""

    skip_active_scans: bool
    """If True, active scans are skipped, else it is considered as a failure"""


def make_angle_proj(scan: H5Handler, config: Config):
    with h5py.File(scan.h5_name, "r") as h5:
        srot = h5[scan.srot_path][()]
    outname = os.path.join(scan.dataset_output, "angle_proj.dat")
    if not config.dry_run:
        with open(outname, "w") as f:
            for value in srot:
                f.write(f"{value:.8}\n")


class H5Handler:
    def __init__(self, h5_path: str, dataset_output: str, config: Config):
        self._config = config
        self._scan_current: CurrentReader | None = None

        self.h5_name = os.path.abspath(h5_path)
        self.dataset_output = dataset_output
        dataset_dir = os.path.dirname(h5_path)
        self.dataset_name = dataset_dir.split("/")[-1]

        self.acq_frame: int = -1
        """Number of accumulated frames, 1 means there is no accumulation"""

        self.acc_output_sum: bool = True
        """If true the detector output is provided as accumulated sum.

        Else it's a statisitc on a signle sub frame.
        """

        self.flat: list[str] = []
        self.dark: list[str] = []
        self.static: list[str] = []
        self.group_scan: str | None = None
        self.proj_scan: str | None = None
        self.current_scan: str | None = None
        self.sx_path: str | None = None
        self.sy_path: str | None = None
        self.yrot_path: str | None = None
        self.sz_path: str | None = None

        self.detector: str | None = None
        self.cameratype: str | None = None

        with h5py.File(self.h5_name, "r") as h5:
            self._read(h5)

    def get_axis_path(self, h5: h5py.File, role: str):
        role_path = f"{self.group_scan}/technique/tomoconfig/{role}"
        if role_path in h5:
            names = h5[role_path].asstr()[()]
            for name in names:
                measurement_path = f"{self.proj_scan}/measurement/{name}"
                if measurement_path in h5:
                    return measurement_path
                positioner_path = f"{self.proj_scan}/instrument/positioners/{name}"
                if positioner_path in h5:
                    return positioner_path

        _logger.warning("Axis role '%s' was not found", role)

        def get_path(path1: str, path2: str | None = None):
            if path1 in h5:
                return path1
            if path2 is not None and path2 in h5:
                return path2
            return None

        if role == "sample_u":
            return get_path(f"{self.proj_scan}/instrument/positioners/sx")
        elif role == "sample_v":
            return get_path(f"{self.proj_scan}/instrument/positioners/sy")
        elif role == "translation_y":
            return get_path(f"{self.proj_scan}/instrument/positioners/yrot")
        elif role == "translation_z":
            return get_path(
                f"{self.proj_scan}/instrument/positioners/sz",
                f"{self.proj_scan}/measurement/sz",
            )
        raise ValueError(f"Unknown role {role}")

    def _read(self, h5: h5py.File):
        # make sure everything is done

        if "Bliss" not in h5.attrs.get("creator"):
            raise exceptions.FileNotProducedByBliss

        for name in h5:
            if "end_time" not in h5[name]:
                raise exceptions.ScanNotTerminated(self.h5_name, name)

        for name in h5:
            if "writer" in h5[name]:
                if "status" in h5[name]["writer"]:
                    status = h5[name]["writer/status"].asstr()[()]
                    if status != "SUCCEEDED":
                        raise exceptions.ScanNotSuccessed(self.h5_name, name, status)

        # categories scans
        for name in h5:
            # FIXME: Use image_key
            scan = h5[name]
            title = scan["title"].asstr()[()]
            if "tomo" in title:
                self.group_scan = name
            elif "dark" in title:
                self.dark.append(name)
            elif "flat" in title:
                self.flat.append(name)
            elif "projections" in title:
                if name.endswith(".1"):
                    self.proj_scan = name
                if "measurement/current" in scan:
                    self.current_scan = name
            elif "static images" in title:
                self.static.append(name)

        self.sample_name = h5[self.group_scan + "/sample/name"].asstr()[()]

        if self._config.current is None and self.current_scan is None:
            raise ValueError("Missing slow chain for machine current")

        self._read_detector_info(h5)

        try:
            group = h5[self.group_scan]
            self.end_time = group["end_time"][()]

            if self.current_scan is not None:
                self._scan_current = CurrentReader()
                self._scan_current.read_from_h5(h5[self.current_scan])

            proj_group = h5[self.proj_scan]
            if "measurement/timer_trig" in proj_group:
                self.scan_time = proj_group["measurement/timer_trig"][()]
                self.scan_epoch = proj_group["measurement/epoch_trig"][()]
            else:
                self.scan_time = proj_group["measurement/elapsed_time"][()]
                self.scan_epoch = proj_group["measurement/epoch"][()]

            self.tomo_n = group["technique/scan/tomo_n"][()]
            self.digits = len(str(self.tomo_n))
            if self.digits < 4:
                self.digits = 4

            self.sx_path = self.get_axis_path(h5, role="sample_u")
            self.sy_path = self.get_axis_path(h5, role="sample_v")
            self.sz_path = self.get_axis_path(h5, role="translation_z")
            self.yrot_path = self.get_axis_path(h5, role="translation_y")
            self.srot_path = self.get_axis_path(h5, role="rotation")

            try:
                self.ref_on = group["technique/scan/tomo_n"][()]
            except Exception:
                pass

            print("Accu= ", self.acq_frame, "sum?", self.acc_output_sum)
        except AttributeError:
            _logger.debug("Error while reading acquisition info", exc_info=True)

    def _read_detector_info(self, h5: h5py.File):
        group = h5[self.group_scan]
        self.detector = list(group["technique/detector"])[0]

        detector_group = group[f"technique/detector/{self.detector}"]
        cameratype = self.detector
        try:
            cameratype = detector_group["name"].asstr()[()]
        except Exception:
            try:
                cameratype = detector_group["type"].asstr()[()]
            except Exception:
                pass
        finally:
            if "IRIS" in cameratype:
                for i in group["technique/detector"]:
                    cameratype = i
        self.cameratype = cameratype

        proj_group = h5[self.proj_scan]
        detector_group2 = proj_group[f"instrument/{self.detector}"]
        try:
            self.acq_mode = detector_group2["acq_parameters/acq_mode"].asstr()[()]
            acc_max_expo_time = detector_group2["ctrl_parameters/acc_max_expo_time"][()]
            # acc_max_expo_time is not the real accumulation used by lima
            acq_expo_time = detector_group2["acq_parameters/acq_expo_time"][()]
            d, m = divmod(acq_expo_time, acc_max_expo_time)
            acq_frame = d + int(m > 0.00001)
            self.acq_frame = acq_frame
            if "acq_parameters/acc_operation" in detector_group2:
                acc_operation = detector_group2["acq_parameters/acc_operation"][()]
                self.acc_output_sum = acc_operation == "ACC_SUM"
            else:
                self.acc_output_sum = True
        except Exception:
            _logger.debug("Error while reading acquisition info", exc_info=True)
            _logger.error("Fall back with no acq_mode/acq_frame/max_expo")
            self.acq_mode = ""
            self.acq_frame = 0
            self.acc_output_sum = True

    @property
    def current(self) -> CurrentReader:
        """
        Return the current to use.
        """
        if self._config.current is not None:
            return self._config.current
        if self._scan_current is None:
            raise RuntimeError("No current available")
        return self._scan_current

    def create_directory(self):
        if not os.path.isdir(self._config.edf_directory):
            if not self._config.dry_run:
                os.makedirs(self._config.edf_directory)

        if not os.path.isdir(self.dataset_output):
            if not self._config.dry_run:
                os.makedirs(self.dataset_output)

    def dump_files(self, data):
        print("Dumping files into", self.dataset_output)
        for filename in data.filename_list:
            outname = os.path.join(self.dataset_output, filename)
            if not self._config.dry_run:
                with open(outname, "wb") as fout:
                    fout.write(data[filename])

    def run_projection(self):
        """Creation of projections"""
        dataset = self.proj_scan + "/measurement/" + self.detector
        ram_dump = False
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="proj",
            scan_time=self.scan_time,
            scan_epoch=self.scan_epoch,
            current=self.current,
            acq_frame=self.acq_frame,
            acc_output_sum=self.acc_output_sum,
            sx=self.sx_path,
            sy=self.sy_path,
            sz=self.sz_path,
            yrot=self.yrot_path,
            filename_pattern=f"{self.dataset_name}_{{index:0{self.digits}d}}.edf",
            dump=ram_dump,
        )
        if ram_dump:
            data.dump_data("proj")
            try:
                self.dump_files(data)
            finally:
                data.close()
        else:
            series = EdfFileSeries(
                output_directory=self.dataset_output,
                filename_pattern=f"{self.dataset_name}_{{index:0{self.digits}d}}.edf",
            )
            progress = ProgressBar("Convert projections", self.tomo_n, 40)
            try:
                with series:
                    for i, _f, frame in data.iter_frames("proj"):
                        header = data.header(i)
                        series.append(frame, header)
                        progress.update(i)
            finally:
                progress.clear()
                data.close()

        try:
            last_frame = os.path.join(self.dataset_output, data.name(self.tomo_n - 1))
            very_last_frame = os.path.join(self.dataset_output, data.name(self.tomo_n))
            cmd = f"cp {last_frame} {very_last_frame}"
            print(cmd)
            if not self._config.dry_run:
                os.system(cmd)
        except Exception as e:
            _logger.debug("Error while duplicating the last proj", exc_info=True)
            print(e)

        print("Conversion of projections done")

    def run_dark(self):
        if len(self.dark) == 0:
            _logger.debug("No dark found")
            return
        dark = self.dark[0]
        if len(self.dark) > 1:
            _logger.warning(
                "More than one dark found. Only the first one was processed"
            )
        dataset = dark + "/measurement/" + self.detector
        print("Conversion of darks in progress...")
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="dark",
            acq_frame=self.acq_frame,
            acc_output_sum=self.acc_output_sum,
            filename_pattern="dark.edf",
        )
        try:
            self.dump_files(data)
        finally:
            data.close()

        print("Conversion of darks done")

    def run_static(self):
        if len(self.static) == 0:
            _logger.debug("No static found")
            return
        if len(self.static) > 1:
            _logger.warning(
                "More than one static found. Only the first one was processed"
            )
        dataset = self.static[0] + "/measurement/" + self.detector
        print("Conversion of end images in progress...")

        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="static",
            acq_frame=self.acq_frame,
            acc_output_sum=self.acc_output_sum,
            filename_pattern=f"{self.dataset_name}_{{index:0{self.digits}d}}.edf",
            first_index=self.ref_on + 1,
        )

        try:
            self.dump_files(data)
        finally:
            data.close()

        # cmd = "mv " + self.dataset_output + "/static" + "0" * self.digits + ".edf " + self.dataset_output + "/static.edf"
        if not self._config.dry_run:
            # os.system(cmd)
            pass
        print("Conversion of end images done")

    def run_flat(self):
        if len(self.flat) == 0:
            _logger.debug("No flat found")
            return
        dataset = self.flat[0] + "/measurement/" + self.detector
        print("Conversion of flats in progress...")
        data = EdfFrom3d(
            self.h5_name,
            dataset,
            kind="flat",
            acq_frame=self.acq_frame,
            acc_output_sum=self.acc_output_sum,
            filename_pattern=f"refHST{0:0{self.digits}d}.edf",
        )
        try:
            self.dump_files(data)
        finally:
            data.close()

        if len(self.flat) > 1:
            dataset = self.flat[1] + "/measurement/" + self.detector
            print("Conversion of flats in progress...")
            data = EdfFrom3d(
                self.h5_name,
                dataset,
                kind="flat",
                acq_frame=self.acq_frame,
                acc_output_sum=self.acc_output_sum,
                filename_pattern=f"refHST{self.ref_on:0{self.digits}d}.edf",
            )
            try:
                self.dump_files(data)
            finally:
                data.close()
        else:
            try:
                cmd = (
                    f"cp {self.dataset_output}/refHST"
                    + "0" * self.digits
                    + f".edf {self.dataset_output}/refHST{self.ref_on:0{self.digits}d}.edf"
                )
                print(cmd)
                if not self._config.dry_run:
                    os.system(cmd)
            except Exception as e:
                _logger.debug("Error while copying refHST data", exc_info=True)
                print(
                    f"You might need to create {self.dataset_output}/{self.dataset}_{self.ref_on}.edf and {self.dataset_output}/refHST{self.ref_on:0{self.digits}d}.edf"
                )
                print(e)
        print("Conversion of flats done")

    def finish(self):
        cmd = f"chmod -R 777 {self.dataset_output}"
        if not self._config.dry_run:
            os.system(cmd)

    def execute(self):
        self.create_directory()
        self.run_projection()
        make_angle_proj(self, self._config)
        self.run_static()
        if self._config.process_dark:
            self.run_dark()
        else:
            _logger.debug("Dark was skipped by configuration")

        if self._config.process_flat:
            self.run_flat()
        else:
            _logger.debug("Flat was skipped by configuration")

        from .info_output import make_info

        try:
            make_info(self, self._config)
        except Exception:
            _logger.debug("Error while generating XML file", exc_info=True)
            print("info creation failed")

        if self._config.generate_xml:
            from .xml_output import make_xml

            try:
                make_xml(self, self._config)
            except Exception:
                _logger.debug("Error while generating XML file", exc_info=True)
                print("xml creation failed")

        if self._config.generate_yml:
            from .yaml_output import make_yaml

            try:
                make_yaml(self, self._config)
            except Exception:
                _logger.debug("Error while generating YAML file", exc_info=True)
                print("yaml creation failed")
        self.finish()

        print("Conversion over")


class EdfFrom3d:
    """Maps a 3D array in a hdf5 file to stack of 2D image files"""

    def __init__(
        self,
        h5filename,
        dataset,
        /,
        kind,
        acq_frame,
        acc_output_sum,
        scan_time=None,
        scan_epoch=None,
        current=None,
        first_index=0,
        filename_pattern="{index:04d}.edf",
        sx=None,
        sy=None,
        sz=None,
        yrot=None,
        dump=True,
    ):
        """
        Arguments:
            h5filename: h5file to get the data from
            dataset: 3d array to map
            stem: output name stem
        """
        # FIXME: This is not properly handled
        self.h5o = h5py.File(h5filename, "r")
        self.dataset = self.h5o[dataset]
        assert len(self.dataset.shape) == 3, "We need a 3D array please!"

        self._current = current
        self.scan_time = scan_time
        self.scan_epoch = scan_epoch
        self.filename_pattern = filename_pattern
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.yrot = yrot
        self.first_index = first_index
        self.acq_frame: int = acq_frame
        self.acc_output_sum: bool = acc_output_sum
        self._file_size = None
        if dump:
            self.dump_data(kind)

    def dump_data(self, kind):
        self.filename_list = []
        self.filename_lut = {}
        self.data = []
        for i, f, d in self.iter_frames(kind):
            self.filename_list.append(f)
            self.filename_lut[f] = i
            self.data.append(d)

    def _normalize_to_uint16_single_frame(self, data: numpy.ndarray) -> numpy.ndarray:
        """Get a frame this the actual accumulation and returns it as single frame uint16"""
        if self.acq_frame > 1 and self.acc_output_sum:
            data = data / self.acq_frame
        if data.dtype == numpy.uint16:
            return data
        if data.max() > numpy.iinfo(numpy.uint16).max:
            _logger.warning("The convertion to uint16 will overflow")
        return data.astype(numpy.uint16)

    def iter_frames(self, kind):
        if kind == "dark":
            filename_list = [self.name(0)]
            data = [numpy.mean(self.dataset, axis=0)]

        elif kind == "flat":
            filename_list = [self.name(0)]
            data = [numpy.median(self.dataset, axis=0)]

        elif kind == "static":
            filename_list = [self.name(i) for i in range(len(self))]
            data = self.dataset

        elif kind == "proj":
            # Decide on which frame has which filename:
            filename_list = [self.name(i) for i in range(len(self))]
            data = self.dataset

        else:
            assert False

        _logger.debug("Iter %s nb %s", len(filename_list), kind)
        for i, filename in enumerate(filename_list):
            yield i, filename, self._normalize_to_uint16_single_frame(data[i])

    def close(self):
        self.dataset = None
        self.h5o.close()

    def name(self, i):
        """Generate some filename pattern"""
        index = int(self.first_index) + i
        return self.filename_pattern.format(index=index)

    def num(self, name):
        """Get the frame index from the filenane"""
        return self.filename_lut[name]

    def header(self, index):
        sx = self.sx
        sy = self.sy
        sz = self.sz
        yrot = self.yrot

        result = {}
        if self._current is not None:
            epoch = self.scan_epoch[index]
            result["SRCUR"] = str(self._current.get(epoch))

        if sx is not None and sy is not None and sz is not None and yrot is not None:
            motor_mne = []
            motor_pos = []
            if sx in self.h5o:
                motor_mne.append("sx")
                motor_pos.append(str(self.h5o[sx][()]))
            if sy in self.h5o:
                motor_mne.append("sy")
                motor_pos.append(str(self.h5o[sy][()]))
            if sz in self.h5o:
                motor_mne.append("sz")
                if "positioners" in sz:
                    motor_pos.append(str(self.h5o[sz][()]))
                else:
                    motor_pos.append(str(self.h5o[sz][()][index]))
            if yrot in self.h5o:
                motor_mne.append("yrot")
                motor_pos.append(str(self.h5o[yrot][()]))
            result["motor_mne"] = " ".join(motor_mne)
            result["motor_pos"] = " ".join(motor_pos)
        return result

    def toBlob(self, i):
        """Convert the numpy array to a file"""
        out = self._normalize_to_uint16_single_frame(self.data[i])
        header = self.header(i)
        edf = fabio.edfimage.edfimage(out, header=header)
        try:
            # FIXME: strange that we need to do this?
            edf._frames[0]._index = 0
            blob = bytearray(edf._frames[0].get_edf_block())
        except Exception as e:
            _logger.debug("Error while creating EDF output", exc_info=True)
            print(e)
        finally:
            edf.close()
        return blob

    def filesize(self, arg=0):
        """Size of the files"""
        if self._file_size is None:
            blob = self[arg]
            self._file_size = len(blob)
        return self._file_size

    # The rest is hopefully common to most 3D data arrays
    #  ... changes if you piece together scans in a h5 etc
    def __len__(self):
        """Number of frames"""
        return self.dataset.shape[0]

    @functools.lru_cache(maxsize=LRU_CACHE_SIZE)
    def __getitem__(self, arg):
        """
        Given a filename : return a Blob
        """
        if isinstance(arg, int):
            i = arg
        else:
            i = self.num(arg)  # raises KeyError if missing
        if i < 0 or i >= len(self):
            raise KeyError("Not found %s" % (arg))
        return self.toBlob(i)
