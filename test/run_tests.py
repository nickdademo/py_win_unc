import platform
from unittest import main

from test_net_use_table import *
from test_sanitize import *
from test_utils import *
from test_unc_directory import *


if platform.system() == 'Windows':
	print 'Including Windows-specific tests'
else:
	print 'WARNING: Excluding Windows-specific tests because host is not Windows'


if __name__ == '__main__':
    main()
