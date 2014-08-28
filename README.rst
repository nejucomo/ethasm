======
ethasm
======

Ethereum assembler / disassembler.

Crash Course
============

Prerequisites
-------------

All dependencies are fetched and installed automatically provided you start with `python`_ and `pip`_.

This project only supports `pip`_ -based installation.  The author also recommends `virtualenv`_.

Installation
------------

**Now:** Clone this repository, then from the repository root, run ``pip install .``

**Future:** Run ``pip install ethasm``.

Usage
-----

It's easiest to start by disassembling some bytecode to get a feel for the syntax:

.. code:: bash

    $ ethasm -d < ./path/to/serpent-compile-output

**FIXME:** serpent outputs hex... either disassemble from hex or provide serpent-to-bytecode instructions.

Assembling the output of disassembly should produce bytewise identical code:

.. code:: bash

    $ ethasm -d < ./path/to/serpent-compile-output | ethasm > /tmp/reassembled
    $ diff -q ./path/to/serpent-compile-output /tmp/reassembled || echo 'Reassembly produced different output.'

Note however, that the output of disassembly is a *subset* of the (future / planned) assembler language.

Target Virtual Machine
----------------------

The (future) goal is to track Ethereum PoC6 and later.  In the future the python package version will reflect the target Ethereum bytecode version, in a manner similar to pyethereum's version.

Development
===========

Status
------

This is still a hard-to-use proof-of-concept.  The codebase is straddling PoC5 / PoC6 and incoherent.

Roadmap
-------

* Full unit test coverage, developing tests to specify PoC6 bytecode (based on `pyethereum`_) and the assembler language.
* Define a python package versioning scheme to track Ethereum specs.  Probably `0.N.j` where `N` is the PoC<N> specification, and `j` is an incrementing integer unique to `ethasm` (and distinct from `pyethereum`_).
* Publish to pypi and announce in Ethereum venues.
