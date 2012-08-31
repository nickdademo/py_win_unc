class UncMountingError(object):
    pass


class UncMountFailedError(UncMountingError):
    """
    Error for the case when the `UncDirectory` is not able to be mounted.
    """
    def __init__(self, unc_path, drive_letter):
        """
        Returns a `MountingError` object. `unc_path` is the UNC path that could not be mounted.
        `drive_letter` is the Windows drive letter that was attempting to be mapped.
        """
        self.unc_path = unc_path
        self.drive_letter = drive_letter

    def __str__(self):
        return 'Failed to mount UNC directory at "{path}" to the {drive}: drive.'.format(
            path=self.unc_path,
            drive=self.drive_letter)


class NoDrivesAvailableError(UncMountingError):
    """
    Error for the case when Windows has no drive letters available to be mapped.
    """

    def __str__(self):
        """
        Returns a description of the error.
        """
        return 'The system has no drive letters available.'
