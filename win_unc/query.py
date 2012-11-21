from win_unc.connecting import UncDirectoryConnection, UncDirectoryMount
from win_unc.internal.current_state import get_current_net_use_table


__all__ = ['get_current_connections', 'get_connection_for_unc_directory']


def get_current_connections():
    net_use = get_current_net_use_table()
    return [_get_connection_or_mount(row['remote'], row['local']) for row in net_use.rows]


def get_connection_for_unc_directory(unc):
    net_use = get_current_net_use_table()
    matching = net_use.get_matching_rows(remote=unc)
    return _get_connection_or_mount(matching[0]['remote'], matching[0]['local']) if matching else None


def _get_connection_or_mount(unc, disk_drive=None):
    return UncDirectoryMount(unc, disk_drive) if disk_drive else UncDirectoryConnection(unc)
