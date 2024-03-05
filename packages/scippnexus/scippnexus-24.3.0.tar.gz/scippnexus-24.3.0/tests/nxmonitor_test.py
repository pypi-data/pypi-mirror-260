import h5py
import pytest
import scipp as sc
from scipp.testing import assert_identical

import scippnexus as snx


@pytest.fixture()
def h5root():
    """Yield h5py root group (file)"""
    with h5py.File('dummy.nxs', mode='w', driver="core", backing_store=False) as f:
        yield f


def make_group(group: h5py.Group) -> snx.Group:
    return snx.Group(group, definitions=snx.base_definitions())


@pytest.fixture()
def group():
    """Yield NXroot containing a single NXentry named 'entry'"""
    with h5py.File('dummy.nxs', mode='w', driver="core", backing_store=False) as f:
        yield snx.Group(f, definitions=snx.base_definitions())


def test_dense_monitor(h5root):
    monitor = snx.create_class(h5root, 'monitor', snx.NXmonitor)
    da = sc.DataArray(
        sc.array(dims=['time_of_flight'], values=[1.0]),
        coords={'time_of_flight': sc.array(dims=['time_of_flight'], values=[1.0])},
    )
    data = snx.create_field(monitor, 'data', da.data)
    data.attrs['axes'] = 'time_of_flight'
    snx.create_field(monitor, 'time_of_flight', da.coords['time_of_flight'])
    monitor = make_group(monitor)
    assert sc.identical(monitor[...]['data'], da)


def create_event_data_no_ids(group):
    group.create_field(
        'event_time_offset',
        sc.array(dims=[''], unit='s', values=[456, 7, 3, 345, 632, 23]),
    )
    group.create_field(
        'event_time_zero', sc.array(dims=[''], unit='s', values=[1, 2, 3, 4])
    )
    group.create_field(
        'event_index', sc.array(dims=[''], unit=None, values=[0, 3, 3, 5])
    )


def test_loads_event_data_in_current_group_as_data_array(group):
    monitor = group.create_class('monitor1', snx.NXmonitor)
    create_event_data_no_ids(monitor)
    assert monitor.dims == ('event_time_zero',)
    assert monitor.shape == (4,)
    loaded = monitor[...]['events']
    assert_identical(
        loaded.bins.size().data,
        sc.array(
            dims=['event_time_zero'], unit=None, dtype='int64', values=[3, 0, 2, 1]
        ),
    )


def test_loads_event_data_in_child_group_as_data_array(group):
    monitor = group.create_class('monitor1', snx.NXmonitor)
    create_event_data_no_ids(monitor.create_class('events', snx.NXevent_data))
    assert monitor.dims == ('event_time_zero',)
    assert monitor.shape == (4,)
    loaded = monitor[...]
    assert isinstance(loaded, sc.DataGroup)
    assert isinstance(loaded['events'], sc.DataArray)
    assert sc.identical(
        loaded['events'].bins.size().data,
        sc.array(
            dims=['event_time_zero'], unit=None, dtype='int64', values=[3, 0, 2, 1]
        ),
    )
