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


Contents
========

* This list will contain the toc (it doesn't matter what you write here)
{:toc}


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

Once you've installed `setuptools`, you need to add some paths to your system's `Path`
environment variable. You'll probably want to add paths like these:

*   `C:\Python27`
*   `C:\Python27\Scripts`

Then, in Windows command-line (`cmd.exe`), you can run the following to get `pip`
installed:

    > easy_install pip


Basic Usage
===========

Below is a simple example:

{% highlight python %}
from win_unc import DiskDrive, UncDirectory, UncDirectoryConnection, UncDirectoryMount

# Connect a shared directory without authorization.
unc = UncDirectory(r'\\home\shared')
conn = UncDirectoryConnection(unc, persistent=True)

conn.connect()
print 'Connected?', conn.is_connected()
conn.disconnect()


# Mount another directory with authorization to the Z: drive.
creds = UncCredentials('user', 'pwd')
authz_unc = UncDirectory(r'\\remote\shared', creds)

mnt = UncDirectoryMount(authz_unc, DiskDrive('Z:'))

mnt.mount()
print 'Mounted?', mnt.is_mounted()
mnt.unmount()


# Mount a directory to any available local drive.
mnt2 = UncDirectoryMount(UncDirectory(r'\\neighbor\shared'))
mnt2.mount()
print 'Mounted at:', mnt2.disk_drive
mnt2.unmount()
{% endhighlight %}


Documentation
=============

UncDirectoryConnection {#UncDirectoryConnection}
----------------------

The [UncDirectoryConnection][] class describes how a UNC directory relates to the current
Windows sesssion. Use this class when you want to connect or disconnect a UNC directory. You can
also use it to determine if a UNC directory is connected or not.


### \_\_init\_\_ {#UncDirectoryConnection_init}

{% highlight python %}
UncDirectoryConnection(
    unc_directory,
    disk_drive=None,
    persistent=False,
    logger=no_logging)
{% endhighlight %}

Constructs a new [UncDirectoryConnection][] object.

`unc_directory` must be a [UncDirectory][] object which provides a UNC path and any credentials
necessary to authorize the connection.

`disk_drive` must be `None` or a [DiskDrive][] object.

* If `None`, connecting this UNC directory will not create a local mount point.
* If a `DiskDrive`, connecting this UNC directory will create a local mount point at the drive
  letter specified by `disk_drive`.

`persistent` must be `True` if you want the UNC directory connection to persist across multiple
Windows sessions. Otherwise, set this to `False` (the default).

`logger` must be a function that takes a single string argument. The function will be called
whenever the object does something worthy of being logged.

For example, `logger` could look like this:

    def my_logger(message):
        print message


### connect {#UncDirectoryConnection_connect}

{% highlight python %}
connect()
{% endhighlight %}

Connects the UNC directory. This will make at most three connection attempts with different
credential configurations in case the credentials provided are not necessary (which is likely
when the credentials are saved by Windows from a previous connection). If the command fails, a
[ShellCommandError][] will be raised.

### disconnect {#UncDirectoryConnection_disconnect}

{% highlight python %}
disconnect()
{% endhighlight %}

Disconnects the UNC path. If the command fails, a [ShellCommandError][] will be raised.


### is_connected {#UncDirectoryConnection_is_connected}

{% highlight python %}
is_connected()
{% endhighlight %}

Returns `True` if the system registers this [UncDirectoryConnection][] as connected or `False`
otherwise. A UNC path is considered connected when the system reports its status as either `OK` or
`Disconnected`.

**Note: This method does not rely on any internal state management of the object. It is entirely
possible to construct a new [UncDirectoryConnection][] that is *already* connected by the system.
In this case, the result of [is_connected](#UncDirectoryConnection_is_connected) will be `True` even
if no calls to [connect](#UncDirectoryConnection_connect) have yet been made.**


#### Why "Disconnected" Is Considered Connected {#why_disconnected_is_connected}

In the context of the system, a status of `Disconnected` means that the UNC path's connection has
been authorized and established but it is temporarily disconnected (probably because it has been
idle for some period of time).

To refresh the connection of a `Disconnected` UNC path, you can usually just perform some trivial
task with the directory. For example, you could query its contents like this:

    > dir \\unc\path

This commonly refreshes the UNC connection and restores its status to `OK`.

However, these steps are not usually necessary since merely accessing the UNC path in any way will
cause the system to reconnect it.


### get_path {#UncDirectoryConnection_get_path}

{% highlight python %}
get_path()
{% endhighlight %}

Returns the UNC path being used by this [UncDirectoryConnection][].

(This is a pass-through method for the underlying [UncDirectory][].
See [UncDirectory's `get_path` method](#UncDirectory_get_path).)


### get_username {#UncDirectoryConnection_get_username}

{% highlight python %}
get_username()
{% endhighlight %}

Returns the username of the credentials being used by this [UncDirectoryConnection][] or `None` if
no username was provided.

(This is a pass-through method for the underlying [UncDirectory][].
See [UncDirectory's `get_username` method](#UncDirectory_get_username).)


### get_password {#UncDirectoryConnection_get_password}

{% highlight python %}
get_password()
{% endhighlight %}

Returns the password of the credentials being used by this [UncDirectoryConnection][] or `None` if
no password was provided.

(This is a pass-through method for the underlying [UncDirectory][].
See [UncDirectory's `get_password` method](#UncDirectory_get_password).)


### unc (member) {#UncDirectoryConnection_unc}

The [UncDirectory][] for this [UncDirectoryConnection][].


### disk_drive (member) {#UncDirectoryConnection_disk_drive}

The [DiskDrive][] of the mount point for this [UncDirectoryConnection][] or `None` if no mount point
is provided.


### persistent (member) {#UncDirectoryConnection_persistent}

`True` if the Windows system should remember this connection for future sessions of the current
user or `False` otherwise.


### logger (member) {#UncDirectoryConnection_logger}

The logging function to use for logging purposes. This must point to a function that takes exactly
one string argument containing the message of a log.


UncDirectoryMount {#UncDirectoryMount}
-----------------

The [UncDirectoryMount][] class is a [UncDirectoryConnection][] that specifically represents a
connection with a mount point. Unless noted here, this class is identical to
[UncDirectoryConnection][].


### \_\_init\_\_ {#UncDirectoryMount_init}

{% highlight python %}
UncDirectoryConnection(
    unc_directory,
    disk_drive=None,
    persistent=False,
    logger=no_logging)
{% endhighlight %}

Constructs a new [UncDirectoryMount][].

For `unc_directory`, `persistent`, and `logger` see
[UncDirectoryConnection's constructor][#UncDirectoryConnection_init].

`disk_drive` must be `None` or a `DiskDrive`.

* If `None`, an available disk drive will be chosen automatically and used as the mount point for
  this [UncDirectoryMount][]. If no drives are available a [NoAvailableDrivesError][] will be
  raised.
* If a `DiskDrive`, mounting this UNC directory will create a local mount point at the drive
  letter specified by `disk_drive`.


### mount {#UncDirectoryMount_mount}

An alias for [UncDirectoryConnection's `connect` method](UncDirectoryConnection_connect).


### mount {#UncDirectoryMount_unmount}

An alias for [UncDirectoryConnection's `disconnect` method](UncDirectoryConnection_disconnect).


### is_mounted {#UncDirectoryMount_is_mounted}

An alias for [UncDirectoryConnection's `is_connected` method](UncDirectoryConnection_is_connected).



UncDirectory {#UncDirectory}
------------

The [UncDirectory][] class describes the path to a UNC directory and (optionally) any credentials
that are needed to authorize a connection to the path.

### \_\_init\_\_ {#UncDirectory_init}

{% highlight python %}
UncDirectory(
    path,
    unc_credentials=None)
{% endhighlight %}

Constructs a new [UncDirectory][] object.

`path` must be a string representing a UNC path. If `path` cannot be construed as a valid UNC
path, an [InvalidUncPathError][] will be raised.

`unc_credentials` may be either `None` or a [UncCredentials][] object.

* If `None`, the [UncDirectory][] object will not specify any credentials to use for authorizing a
  connection.
* If a [UncCredentials][] object, the [UncDirectory][] will attempt to use `unc_credentials` for
  authorizing a connection.

-----

{% highlight python %}
UncDirectory(
    unc_directory)
{% endhighlight %}

Constructs a new [UncDirectory][] object as a clone of `unc_directory`. The clone will be a
"shallow" copy, so the underlying [UncCredentials][] object used by the clone will have the same
`id` as the original.

`unc_directory` must be a [UncDirectory][] object to clone.


### get_path {#UncDirectory_get_path}

{% highlight python %}
get_path()
{% endhighlight %}

Returns the UNC path for this [UncDirectory][]. The UNC path may differ slightly from the one
provided at the construction of the object since the constructor does some cleaning of the path
before it is used.


### get_normalized_path {#UncDirectory_get_normalized_path}

{% highlight python %}
get_normalized_path()
{% endhighlight %}

Returns the normalized path for this [UncDirectory][]. Differing UNC paths that all point to the
same network location will have the same normalized path.

For example, the following UNC paths all have a normalized path of `\\remote`:

* `\\REMOTE`
* `\\remote\`
* `\\remote\IPC$`


### get_username {#UncDirectory_get_username}

{% highlight python %}
get_username()
{% endhighlight %}

Returns the username of the credentials being used by this [UncDirectory][] or `None` if
no username was provided.

(This is a pass-through method for the underlying [UncCredentials][] object.
See [UncCredentials' `get_username` method](#UncDirectory_get_username).)


### get_password {#UncDirectory_get_password}

{% highlight python %}
get_password()
{% endhighlight %}

Returns the password of the credentials being used by this [UncDirectory][] or `None` if
no password was provided.

(This is a pass-through method for the underlying [UncCredentials][] object.
See [UncCredentials' `get_password` method](#UncDirectory_get_password).)


### get_auth_string {#UncDirectory_get_auth_string}

{% highlight python %}
get_auth_string()
{% endhighlight %}

Returns the authorization string associated with the credentials of this [UncDirectory][].

(This is a pass-through method for the underlying [UncCredentials][] object.
See [UncCredentials' `get_auth_string` method](#UncDirectory_get_auth_string).)


### get_auth_path {#UncDirectory_get_auth_path}

{% highlight python %}
get_auth_path()
{% endhighlight %}

Returns the path of this [UncDirectory][] with the authorization string prepended
(see [get_auth_string](#UncDirectory_get_auth_string)). If this
[UncDirectory][] has no associated credentials, the returned path will be the same as
[get_path](#UncDirectory_get_path).

The result of this method can be parsed by
[get_unc_directory_from_string](#get_unc_directory_from_string) to get a new [UncDirectory][].


UncCredentials {#UncCredentials}
--------------

The [UncCredentials][] class represents a set of credentials (username and password) to be used with
a UNC connection.


### \_\_init\_\_ {#UncCredentials_init}

{% highlight python %}
UncCredentials(
    username=None,
    password=None)
{% endhighlight %}

Constructs a new [UncCredentials][] object.

`username` must be `None` or a string representing a Windows username (logon).

* If `None`, then this object will not specify a username when being used for a UNC connection. This
  means that Windows will use the username of the current Windows session when authorization is
  required.
* If a Windows username, then `username` will be used if authorization is required for the
  accompanying UNC connection.

Usernames may include a domain prefix (i.e. "domain\username"), but if `username` cannot be
construed as a valid Windows username, then an [InvalidUsernameError][] will be raised. Realize that
**providing `None` and `''` (the empty string) for `username` have very different meanings.
Windows usernames cannot be empty.**

`password` must be `None` or a string representing a password. Realize that **providing `None` (no
password) and `''` (the empty string) have very different meanings. The empty string is a
meaningful, legitimate password.**

-----

{% highlight python %}
UncCredentials(
    unc_credentials)
{% endhighlight %}

Constructs a new [UncCredentials][] object as a clone of `unc_credentials`.

`unc_credentials` must be a [UncCredentials][] object to clone.


### get_username {#UncCredentials_get_username}

{% highlight python %}
get_username()
{% endhighlight %}

Returns the username of this [UncCredentials][] object or `None` if no username was provided.


### get_password {#UncCredentials_get_password}

{% highlight python %}
get_password()
{% endhighlight %}

Returns the password of this [UncCredentials][] object or `None` if no password was provided.


### is_empty {#UncCredentials_is_empty}

{% highlight python %}
is_empty()
{% endhighlight %}

Returns `True` if this [UncCredentials][] object does not contain any meaningful credentials and
`False` otherwise.


### get_auth_string {#UncCredentials_get_auth_string}

{% highlight python %}
get_auth_string()
{% endhighlight %}

Returns a standard representation of this [UncCredentials][] object as a string that can be parsed
into a new [UncCredentials][] object by [get_creds_from_string][#get_creds_from_string].

The following table shows some examples of how this authorization string is formatted:

Username | Password | Authorization String
---------|----------|---------------------
`None`   | `None`   | `''`
`'user'` | `None`   | `'user'`
`'user'` | `'pwd'`  | `'user:pwd'`
`None`   | `'pwd'`  | `:pwd`
`'user'` | `''`     | `user:`



DiskDrive {#DiskDrive}
---------

The [DiskDrive][] class represents a Windows disk drive. Disk drives are always identified by a
single alphabet character. They may map to hardware devices, local directories, or remote
directories.


### \_\_init\_\_ {#DiskDrive_init}

{% highlight python %}
DiskDrive(
    drive_letter)
{% endhighlight %}

Constructs a new [DiskDrive][].

`drive_letter` must be a single letter from `A` to `Z` for representing a drive letter. There is
some leniency as to what strings are recognized.

The following are all interpreted as the drive letter `G`:

* `' G '`
* `'G:'`
* `'g'`
* `'g:'`

-----

{% highlight python %}
DiskDrive(
    disk_drive)
{% endhighlight %}

Constructs a new [DiskDrive][] as a clone of `disk_drive`.

`disk_drive` must be a [DiskDrive][] object to clone.


### get_drive {#DiskDrive_get_drive}

{% highlight python %}
get_drive()
{% endhighlight %}

Returns this path for this [DiskDrive][]. The path will always be an upper-case letter followed by
a colon (`:`). For example, if the drive letter is `'G'` then this will return `'G:'`.


Parsing Functions {#parsing_functions}
-----------------

These parsing functions can be used to deserialize (often called "unpickling" in the Python
community) various objects in the `win_unc` library.

### get_unc_directory_from_string {#get_unc_directory_from_string}

Parses a standardized string from
[UncDirectory's `get_auth_path` method](#UncDirectory_get_auth_path) and returns a new
[UncDirectory][] based on it. This may raise any errors that can be raised by
[UncDirectory's constructor](#UncDirectory_init).


### get_creds_from_string {#get_creds_from_string}

Parses a standardized string from
[UncCredentials' `get_auth_string` method](#UncCredentials_get_auth_string) and returns a new
[UncCredentials][] object based on it. This may raise any errors than can be raised by
[UncCredentials' constructor](#UncCredentials_init).


Exception Classes {#exception_classes}
-----------------

`win_unc` uses a set of exception classes to describe errors that could arise when using the
library. They can be imported from the `win_unc.errors` module and they each inherit from
[WinUncError][].

For each exception class, the magic `__str__` method returns a description of the error.


### WinUncError {#WinUncError}

The [WinUncError][] class inherits from `Exception` and acts as an umbrella for all exception
classes that can be raised by the `win_unc` package. This class does not have its own interface
other than what is provided by `Exception`. It is not meant to be raised or instantiated.


### InvalidUncPathError {#InvalidUncPathError}

Represents the error that occurs when an invalid UNC path is provided to [UncDirectory][]'s
constructor.


### InvalidUsernameError {#InvalidUsernameError}

Represents the error that occurs when an invalid Windows username (logon) is provided to
[UncCredentials][]' constructor.


### ShellCommandError {#ShellCommandError}

Represents the error that occurs when a shell command has been executed and returns an error code.



[DiskDrive]: #DiskDrive
[InvalidUncPathError]: #InvalidUncPathError
[InvalidUsernameError]: #InvalidUsernameError
[UncCredentials]: #UncCredentials
[UncDirectory]: #UncDirectory
[UncDirectoryConnection]: #UncDirectoryConnection
[ShellCommandError]: #ShellCommandError
[WinUncError]: #WinUncError


License
=======
This package is released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).

