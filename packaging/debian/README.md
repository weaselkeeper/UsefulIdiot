UsefulIdiot Debian Package
======================

To create an UsefulIdiot DEB package:

    cd src
    make deb

The debian package file will be placed in the `../` directory. This can then be added to an APT repository or installed with `dpkg -i <package-file>`.

Note that `dpkg -i` does not resolve dependencies
