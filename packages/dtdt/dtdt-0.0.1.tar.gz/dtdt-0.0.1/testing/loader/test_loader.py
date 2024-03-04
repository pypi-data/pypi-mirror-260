import os

import numpy as np
import pytest
import tdt

from dtdt import DataFormatEnum, read_block


def get_block_names():
    if not os.path.exists("data/FiPho-180416"):
        tdt.download_demo_data()
    return [dir for dir in os.listdir("data") if os.path.isdir(f"data/{dir}")]


@pytest.fixture(params=get_block_names())
def loaded_data(request: pytest.FixtureRequest):
    block_name = request.param
    return tdt.read_block(f"data/{block_name}"), read_block(f"data/{block_name}")


def type_check(dtdt_prop, tdt_prop):
    if isinstance(dtdt_prop, str):
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif isinstance(dtdt_prop, list):
        t_arr = tdt_prop == dtdt_prop
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif isinstance(dtdt_prop, dict):
        assert all(
            dtdt_prop.items() == tdt_prop.items()
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif isinstance(dtdt_prop, np.ndarray):
        t_arr = tdt_prop == dtdt_prop
        t_arr = t_arr.flatten()
        assert all(
            t_arr
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif (
        isinstance(dtdt_prop, np.int64)
        or isinstance(dtdt_prop, np.int32)
        or isinstance(dtdt_prop, np.int16)
        or isinstance(dtdt_prop, np.int8)
    ):
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif isinstance(dtdt_prop, np.float64) or isinstance(dtdt_prop, np.float32):
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif (
        isinstance(dtdt_prop, np.uint64)
        or isinstance(dtdt_prop, np.uint32)
        or isinstance(dtdt_prop, np.uint16)
        or isinstance(dtdt_prop, np.uint8)
    ):
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif isinstance(dtdt_prop, np.bool_):
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    elif isinstance(dtdt_prop, DataFormatEnum):
        dtdt_prop = dtdt_prop.value
        assert (
            dtdt_prop == tdt_prop
        ), f"Failing Type: {type(dtdt_prop)}\ndtdt: {dtdt_prop}\nTDT: {tdt_prop}"
    else:
        raise NotImplementedError(f"Type {type(dtdt_prop)} not implemented")


def test_all_epocs(loaded_data):
    dtdt_data, tdt_data = loaded_data
    for epoc in dtdt_data.epocs:
        for header_prop in epoc.header.__dict__:
            if header_prop == "start_time":
                continue
            dtdt_prop = epoc.header.__dict__[header_prop]
            tdt_prop = getattr(tdt_data.epocs[epoc.header.name], header_prop)
            assert dtdt_prop == tdt_prop
        for prop in epoc.__dict__:
            if prop == "header":
                continue
            if prop == "ts":
                continue
            if prop == "code" or prop == "buddy" or prop == "notes":
                continue
            dtdt_prop = epoc.__dict__[prop]
            tdt_prop = getattr(tdt_data.epocs[epoc.header.name], prop)
            type_check(dtdt_prop, tdt_prop)


def test_all_streams(loaded_data):
    dtdt_data, tdt_data = loaded_data
    for stream in dtdt_data.streams:
        # get all header
        for header_prop in stream.header.__dict__:
            dtdt_prop = stream.header.__dict__[header_prop]
            tdt_prop = getattr(tdt_data.streams[stream.header.name], header_prop)
            assert dtdt_prop == tdt_prop
        for prop in stream.__dict__:
            if prop == "header":
                continue
            dtdt_prop = stream.__dict__[prop]
            try:
                if prop == "ts":
                    continue
                if prop == "chan":
                    tdt_prop = tdt_data.streams[stream.header.name].channel
                else:
                    tdt_prop = getattr(tdt_data.streams[stream.header.name], prop)
            except AttributeError:
                print(
                    f"AttributeError: {prop} not found in tdt data for stream {stream.header.name}"
                )
            type_check(dtdt_prop, tdt_prop)


def test_all_snips(loaded_data):
    dtdt_data, tdt_data = loaded_data
    for snip in dtdt_data.snips:
        for prop in snip.__dict__:
            dtdt_prop = snip.__dict__[prop]
            tdt_prop = getattr(tdt_data.snips[snip.header.name], prop)
            type_check(dtdt_prop, tdt_prop)


def test_all_scalars(loaded_data):
    dtdt_data, tdt_data = loaded_data
    for scalar in dtdt_data.scalars:
        for prop in scalar.__dict__:
            dtdt_prop = scalar.__dict__[prop]
            tdt_prop = getattr(tdt_data.scalars[scalar.header.name], prop)
            type_check(dtdt_prop, tdt_prop)
