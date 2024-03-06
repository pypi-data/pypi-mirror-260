Fibonacci Package
================

|fibonacci-package on PyPI|


Overview
--------

This is a simple Python package for calculating the Fibonacci sequence. This package is created for testing purposes and uploading to PyPI.

Installation
------------

You can install this package using pip:

.. code-block:: bash

    pip install fibonacci_package

Example
-------

Once installed, you can use the package in your Python scripts. Here are two different ways to calculate the Fibonacci sequence:

Recursive Algorithm
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from fibonacci_package.fibonacci import calculate_fibonacci
    from builtins import input, print

    # Get the number of terms from the user
    n = int(input("Enter the number of terms you want in the Fibonacci sequence: "))

    # Calculate the Fibonacci sequence
    result = calculate_fibonacci(n)

    # Print the result
    print(f"The first {n} terms of the Fibonacci sequence are: {result}")

Memoizing the Recursive Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


...
