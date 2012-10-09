---
layout: main
---

Why win_unc?
============

This library is for anyone who has tried to connect to or mount UNC paths in a Python
script on Windows. Understanding how to wield the `NET USE` command is a feat
in itself. Parsing its output programatically to know if your command worked is much
harder.

Fortunately, this library should make your life a lot easier.


Installation
============

To install:

    $ pip install win_unc

Getting pip on Windows
----------------------

Of course, installing `pip` packages on Windows is not always straightforward.
Here's how:

Download the [setuptools installer](http://pypi.python.org/pypi/setuptools) for your platform and
run it. **Note that for 64-bit Windows, you need to download the `ez_setup.py` script instead of
the `.exe` installer.

Once you've installed <code>setuptools</code>, you need to add some paths to your system's `Path`
environment variable. You'll probably want to add paths like these:
  * `C:\Python27`
  * `C:\Python27\Scripts`

Then, in Windows command-line (`cmd.exe`), you can run the following to get `pip`
installed:

    > easy_install pip


Basic Usage
===========

Below is a simple example:

{% highlight python %}
from win_unc import UncDirectoryMount, UncDirectory, DiskDrive

conn = UncDirectoryMount(UncDirectory(r'\\home\shared'), DiskDrive('Z:'))
conn.connect()
print 'Drive connected:', conn.is_connected()
conn.disconnect()
{% endhighlight %}

You can also provide credentials like this

{% highlight python %}
from win_unc import UncCredentials

unc = UncDirectory(r'\\home\shared', UncCredentials('user', 'pwd'))
conn = UncDirectoryMount(unc, DiskDrive('Z:'))</code></pre>
{% endhighlight %}


Documentation
=============

UncDirectoryConnection
----------------------

The `UncDirectoryConnection` class describes how a UNC directory relates to the current
Windows sesssion. Use this class when you want to connect or disconnect a UNC directory. You can
also use it to determine if a UNC directory is connected or not.


### __init__

{% highlight python %}
UncDirectoryConnection(
    unc_directory,
    disk_drive=None,
    persistent=False,
    logger=no_logging)
{% endhighlight %}


License
=======
This package is released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
