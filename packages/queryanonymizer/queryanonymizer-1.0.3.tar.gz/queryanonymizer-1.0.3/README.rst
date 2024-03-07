queryanonymizer
===============

.. image:: https://img.shields.io/pypi/pyversions/queryanonymizer
   :target: https://pypi.org/project/queryanonymizer/
   :alt: PyPI - Python Version


Description
===========

`queryanonymizer` is a Python library designed to anonymize SQL, DAX or others languages queries. It allows safe sharing of queries for debugging, documentation, or educational purposes without the risk of exposing sensitive data. The library provides functions for both anonymizing and deanonymizing queries, with support for various SQL dialects and allows using also custom keywords.

Installation
============

To install `queryanonymizer`, run the following command:

.. code-block:: bash

    pip install queryanonymizer

Usage
=====

Import `queryanonymizer` in your Python project and use the provided functions to anonymize or deanonymize your queries/prompts.

.. code-block:: python

    from queryanonymizer import anonymize, deanonymize, keywords_list

    query = "SELECT * FROM users WHERE user_id = 123;"
    anonymized_query, decoder_dictionary, _ = anonymize(query)

    # Example of deanonymizing a query
    deanonymize(anonymized_query, decoder_dictionary)


Features
========

- **Anonymization of SQL, DAX and other types of queries**: Replace sensitive data in your queries with randomized, case sensitive equivalents.
- **Support for Multiple SQL Dialects**: Customize the anonymization process based on different SQL dialects including T-SQL, MySQL, and others.
- **Customization Options**: Offers various customization options for the anonymization process, such as handling of string literals, numbers, dates, and more.
- **Decoding Dictionary**: Generate a decoding dictionary that allows you to revert your anonymized queries back to their original form.

Contributing
============

Contributions to `queryanonymizer` are welcome! Please refer to the contributing guidelines for more information.

License
=======

`queryanonymizer` is licensed under the MIT License. See the LICENSE file for more details.

Authors
=======

`queryanonymizer` was created by DataTeam.pl (Mariusz & Mateusz Cieciura).
