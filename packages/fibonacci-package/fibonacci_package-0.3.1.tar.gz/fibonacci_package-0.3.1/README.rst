Fibonacci Package
=================

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

    # Get the number of terms from the user
    n = int(input("Enter the number of terms you want in the Fibonacci sequence: "))

    # Calculate the Fibonacci sequence
    result = calculate_fibonacci(n)

    # Print the result
    print(f"The first {n} terms of the Fibonacci sequence are: {result}")

Memoizing the Recursive Algorithm
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from fibonacci_package.fibonacci import fibonacci_with_memoization

    n = int(input("Enter the number of terms you want in the Fibonacci sequence: "))

    fibonacci_sequence = [fibonacci_with_memoization(i) for i in range(n)]

    print(f"The first {n} terms of the Fibonacci sequence (memoized) are: {fibonacci_sequence}")

Output for two cases
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python your_script.py
    Enter the number of terms you want in the Fibonacci sequence: 10
    The first 10 terms of the Fibonacci sequence are: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


.. |fibonacci-package on PyPI| image:: https://img.shields.io/pypi/v/fibonacci-package.svg
   :target: https://pypi.org/project/fibonacci-package/
