
Hiss and Malle tables of low-dimensional represenations of quasi-simple groups
==============================================================================

.. note:: This folder is not included as part of the Python package.

.. warning:: (11/09/2025) Due to a code bug, the complete and omissions
    tables lack the representations of the alternating group :math:`A_5`,
    this will be in the next table update.

Introduction
------------

In 2001, Hiss and Malle [[1]_] published a table containing all absolutely
irreducible representations of quasi-simple groups of dimension at most
250, excluding those of groups of Lie type in their defining
characteristic. See [[1]_, Theorem 1.1] for the technical details.

In 2002, a corrigendum [[2]_] was published completing the list.

It is important to note that the table [[2]_, Table 2] contains deliberate
omissions of some representations. These include:

- The :math:`n-1` or :math:`n-2`-dimensional representations of alternating groups
  (depending on the characteristic of the base field).
- The representations of PSL\ :math:`(2,q)` for :math:`q < 499`.

For more information on the omissions, see [[1]_, Table 2] and [[1]_,
:math:`\S` 6].

Contents of Hiss_Malle_table
----------------------------

We provide a digitalized version of table [[2]_, Table 2] in the following
formats:

* Hiss_Malle_table.tex: LaTeX file containing the table, uses
  the package ``longtables`` to break the table into multiple pages.
* Hiss_Malle_table.csv: CSV file containing the table, the LaTeX ``$``
  symbol have been deleted for easier reading.
* Hiss_Malle_table.md: Markdown file containing the table.
* Hiss_Malle_table.txt: Plain text
  file containing the table in an ASCII table format, the LaTeX ``$``
  symbol have been deleted for easier reading.

For a JSON version of the table, see
``DataProcessingScripts/Hiss_Malle_table_data.json``. Note that this
JSON file contains additional data fields to those in the files above.

The table has been generated using the AI tool Mathpix as a base. After
the first import, the table has been manually corrected. In the process,
we have also renamed the groups to one of the notations used in FiSGO.
See the ``SimpleGroups.SimpleGroup.latex_name`` method documentation for
more details on the naming conventions used.

Contents of Hiss_Malle_omissions
--------------------------------

For completeness, we provide an unpacked version of table [[1]_, Table 2],
containing all omissions excluding those of groups of Lie type in their
defining characteristic. The table is given in the following formats:

- Hiss_Malle_omissions.tex: LaTeX file containing the table, uses the
  package ``longtables`` to break the table into multiple pages.
- Hiss_Malle_omissions.csv: CSV file containing the table, the LaTeX ``$``
  symbol have been deleted for easier reading.
- Hiss_Malle_omissions.md: Markdown file containing the table.
- Hiss_Malle_omissions.txt: Plain text file containing the table in an ASCII
  table format, the LaTeX ``$`` symbol have been deleted for easier reading.

For a JSON version of the table, see
``DataProcessingScripts/Hiss_Malle_missing_data.json``. Note that this
JSON file contains additional data fields to those in the files above.

This table has been generated using the formulas given in [[1]_, Table 2]
for all the omissions listed above, taking into account not to produce
redundacies according to what is stated in [[1]_, :math:`\S` 6]. The
scripts used to generate and treat the data can be found in
``DataProcessingScripts/`` by the name ``Hiss_Malle_missing_data.py``
and ``Hiss_Malle_omissions_table.py``.

Contents of Hiss_Malle_complete
-------------------------------

We provide a complete version of table [[2]_, Table 2] (excluding those of
groups of Lie type in their defining characteristic) in the following
formats:

- Hiss_Malle_complete.tex: LaTeX file containing the table,
  uses the package ``longtables`` to break the table into multiple pages.
- Hiss_Malle_complete.csv: CSV file containing the table, the LaTeX
  ``$`` symbol have been deleted for easier reading.
- Hiss_Malle_complete.md: Markdown file containing the table.
- Hiss_Malle_complete.txt: Plain text file containing the table in an
  ASCII table format, the LaTeX ``$`` symbol have been deleted for easier
  reading..

For a JSON version of the table, see
``DataProcessingScripts/Hiss_Malle_data.json``. Note that this JSON file
contains additional data fields to those in the files above.

References
----------

.. [1] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of
    Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4,
    22–63. |DOI:10.1112/s1461157000000796|

.. [2] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional
    Representations of Quasi-simple Groups. LMS Journal of Computation and
    Mathematics, 5, 95–126. |DOI:10.1112/s1461157000000711|

.. |DOI:10.1112/s1461157000000796| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000796.svg
   :target: https://doi.org/10.1112/s1461157000000796
.. |DOI:10.1112/s1461157000000711| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000711.svg
   :target: https://doi.org/10.1112/s1461157000000711
