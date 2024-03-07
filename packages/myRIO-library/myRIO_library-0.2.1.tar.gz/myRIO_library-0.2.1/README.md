myRIO_library - a library for working with NI myRIO in Python

This library is an improvement over nifpga, a Python library that
gives access to the FPGA registers of NI targets with FPGA.

In this library, we have created some support functions and a class
named MyRIO. We call it "library" because the aim of this project is
to create a collection of packages for running Python programs in
different environments (multiple myRIOs, for example).

The current version only works locally, inside the myRIO.

The main idea is to be able to install this library from myRIO and to
run basic functions easily.

If you want to use this library, you will need an updated NI Linux RT image,
SSH enabled (it is easy to set in NI MAX, the configuration tool), and Internet
enabled on your myRIO (check the myRIO documentation for that).

When ready, you should connect (ssh) to the myRIO and ensure that everything
is up-to-date before installing myRIO_library:

opkg update
opkg install python3 python3-misc python-pip

python -m pip install myRIO_library

# Last update: 2024/03/06 Aitzol Ezeiza Ramos (UPV/EHU)
# TODO: Prepare examples to check how to use the MyRIO class
