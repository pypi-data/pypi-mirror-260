# -*- coding: utf-8 -*-
#
# This file is part of the EBS-tomo project
#
# Copyright (c) 2019-2023 Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

import sys
import argparse
import os
import logging
from glob import glob

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

from h5_to_edf.converter import Config
from h5_to_edf.converter import H5Handler
from h5_to_edf.current_reader import CurrentReader
from h5_to_edf import exceptions


APP_NAME = "h5-to-edf"

LRU_CACHE_SIZE = 64


logging.basicConfig()
_logger = logging.getLogger(APP_NAME)


def create_argument_parser():
    from .. import __version__ as version

    parser = argparse.ArgumentParser()
    parser.add_argument("h5_names")
    parser.add_argument(
        "-o",
        dest="edf_directory",
        default=None,
        help="Output directory for EDF files",
    )
    # parser.add_argument('--start_nb', dest="start_nb", default=1)
    parser.add_argument(
        "--report",
        help="Display report without data processing",
        dest="report",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="Display debug information",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        help="Process the data without writing it",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"{APP_NAME} {version}"
    )
    parser.add_argument(
        "--no-dark",
        dest="process_dark",
        default=True,
        help="If the h5 does not contains darks, will skip dark creation",
        action="store_false",
    )
    parser.add_argument(
        "--no-flat",
        dest="process_flat",
        default=True,
        help="If the h5 does not contains flats, will skip flat creation",
        action="store_false",
    )
    parser.add_argument(
        "--yml",
        dest="generate_yml",
        default=False,
        help="Create a .yml file containing all the metadata from the h5 file",
        action="store_true",
    )
    parser.add_argument(
        "--no-xml",
        dest="generate_xml",
        default=True,
        help="Do not generate a .xml file containing few metadata from the h5 file",
        action="store_false",
    )
    parser.add_argument(
        "--current",
        dest="current",
        default=None,
        help="Use a current text file containing the machine current",
    )
    parser.add_argument(
        "--skip-active-scans",
        default=False,
        action="store_true",
        help="If specified, scans which are not terminated are skipped, "
        "else it is considered as a failure",
    )
    parser.add_argument(
        "--raw-data-root",
        default=False,
        action="store_true",
        help="The input source is the ESRF RAW_DATA root, "
        "using the ESRF data policy",
    )
    return parser


def convert_h5_file_to_edf(h5_filename: str, config: Config):
    """Convert a specific HDF5 file into a EDF file structure"""
    print(f"Process {h5_filename}")
    if config.root_directory is None:
        h5_path = h5_filename
        directory = os.path.dirname(h5_filename)
        dataset = directory.split("/")[-1]
    else:
        h5_path = os.path.join(config.root_directory, h5_filename)
        dataset = os.path.dirname(h5_filename)

    dataset_output = os.path.join(config.edf_directory, dataset + "_")

    if os.path.exists(dataset_output):
        # FIXME: Check if correct number of files
        # FIXME: Check if right size of files
        _logger.error("EDF directory '%s' already exists: File skipped", dataset_output)
        return

    try:
        scan = H5Handler(h5_path=h5_path, dataset_output=dataset_output, config=config)
    except ValueError as e:
        _logger.debug("Error while creating H5Handler", exc_info=True)
        _logger.error("%s: File skipped", e.args[0])
        return

    if "fast_acq" not in dir(scan) and "end_time" not in dir(scan):
        _logger.error("No fast_acq and no end_time in the file: File skipped")
        return

    if config.report:
        from h5_to_edf.report_output import make_report

        make_report(scan, config)
        return

    scan.execute()


def search_from_raw_data(root: str):
    h5_names = []
    for i in glob("*/*.h5", root_dir=root):
        if "tomwer" in i or "nabu" in i:
            # Skip post processing
            continue
        if '/blc' in i:
            # Skip collection root file
            continue
        h5_names.append(i)
    for i in glob("*/*/*.h5", root_dir=root):
        if "tomwer" in i or "nabu" in i:
            # Skip post processing
            continue
        h5_names.append(i)
    return h5_names


def search_default(root: str):
    if "*" not in root:
        if root.endswith(".h5"):
            h5_names = [root]
        else:
            if root[-1] == "/":
                root = root[:-1]
            root += "*"
    else:
        h5_names = [root]

    if "*" in root:
        h5_names = []
        for i in glob(root):
            for j in glob(i + "/*.h5"):
                if "tomwer" not in j and "nabu" not in j:
                    h5_names.append(j)
        h5_names.sort()
    return h5_names


def main() -> int:
    parser = create_argument_parser()
    args = parser.parse_args()

    if args.debug:
        logging.getLogger("h5_to_edf").setLevel(logging.DEBUG)

    try:
        import resource
    except ImportError:
        _logger.debug("No resource module available")
    else:
        if hasattr(resource, "RLIMIT_NOFILE"):
            try:
                hard_nofile = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
                resource.setrlimit(resource.RLIMIT_NOFILE, (hard_nofile, hard_nofile))
            except (ValueError, OSError):
                _logger.warning("Failed to retrieve and set the max opened files limit")
            else:
                _logger.debug("Set max opened files to %d", hard_nofile)

    if args.raw_data_root:
        root_directory = args.h5_names
        h5_names = search_from_raw_data(args.h5_names)
    else:
        root_directory = None
        h5_names = search_default(args.h5_names)

    if h5_names == []:
        _logger.error("No HDF5 file found")
        return -1

    edf_directory = args.edf_directory
    if edf_directory is None:
        edf_directory = os.path.join(h5_names[0].split("RAW_DATA")[0], "NOBACKUP")

    if args.current is not None:
        _logger.debug(f"Read current file %s", args.current)
        current = CurrentReader()
        current.read_esrf_current_file(args.current)
    else:
        current = None

    config = Config(
        root_directory=root_directory,
        edf_directory=edf_directory,
        process_dark=args.process_dark,
        process_flat=args.process_flat,
        generate_yml=args.generate_yml,
        generate_xml=args.generate_xml,
        skip_active_scans=args.skip_active_scans,
        report=args.report,
        dry_run=args.dry_run,
        args=args,
        current=current,
    )

    # start_nb = args.start_nb
    if not os.path.exists(edf_directory):
        if not config.report and not config.dry_run:
            os.makedirs(edf_directory, exist_ok=True)

    _logger.debug("Found %s", h5_names)

    if not args.report:
        if not os.access(edf_directory, os.W_OK):
            _logger.error(
                "EDF directory '%s' not writtable: Processing cancelled", edf_directory
            )
            return -1

    for h5_name in h5_names:
        try:
            convert_h5_file_to_edf(h5_name, config)
        except exceptions.FileNotProducedByBliss:
            _logger.warning(f"File {h5_name} was not produced by BLISS. Skipped")
        except (exceptions.ScanNotTerminated, exceptions.ScanNotSuccessed) as e:
            if config.skip_active_scans:
                _logger.warning(e.args[0])
            else:
                raise

    return 0


if __name__ == "__main__":
    res = main()
    sys.exit(res)
