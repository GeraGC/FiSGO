Data Processing Scripts
=======================

.. note:: This folder is not included as part of the Python package.

This folder contains Python and `GAP <https://www.gap-system.org>`__
scripts to process various data into a suitable format for the FiSGO
package, or for verification purposes.

Many of these scripts are not properly documented, and the naming of the
files is a bit all over the place. We make them publicly available for
data source tracking purposes. The results of these scripts are some of
the files in the ``PrecomputedData`` folder, whose files contain the
data in a suitable format for use in the FiSGO package.

In the sequel, we briefly describe the contents of each script file in
this folder.

- ``GAP_small_irreps_extraction.g``: GAP script to browse the CTblLib
  package. We search for all available quasi-simple groups available and
  generate a txt file formated in JSON containing a list of objects
  containing, for each degree from 2 to 250, all ordinary
  (zero-characterisic) irreducible representations of the available
  groups.
- ``GAP_sporadic_extraction.g``: GAP script to obtain all degree
  information on the zero characteristic projective irreducible
  representations of the sporadic groups. The output can be seen in the
  file ``sporadic_data_pirreps.json``.
- ``Hiss_Malle_table_data.py``: Python script to transform the data
  contained in ``raw_Hiss_Malle_table.json`` into a more suitable
  format. The script also generates the simple group code for every
  indexed quasi-simple group. If the group is a covering, the code of
  the associated simple group is provided. The output is stored in
  ``Hiss_Malle_table_data.json``.
- ``Hiss_Malle_missing_data.py``: Python script to generate the missing
  data for the Hiss-Malle table. This data corresponds to the generic
  representations given in Table 2 of [[1]_]. The data is encoded as a JSON
  file and stored in ``Hiss_Malle_missing_data.json``.
- ``Hiss_Malle_omissions_table.py``: Python script to generate a table
  from the data contained in ``Hiss_Malle_missing_data.json``. The table
  is stored in ``Hiss_Malle_omissions_table.json``.
- ``Hiss_Malle_data_merge.py``: Python script to merge the data
  contained in ``Hiss_Malle_table_data.json`` and
  ``Hiss_Malle_missing_data.json``. The output is stored in
  ``Hiss_Malle_data.json``.
- ``sporadic_data_encoding.py``: Python script to transform the data
  contained in ``sporadic_data_pirreps.json`` into a more suitable
  format. The script also adds all relevant data (to FiSGO) of each
  sporadic group (order, Schur multiplier,…). The output is stored in
  ``..\PrecomputedData\sporadic_groups_data.json``.

References
----------

.. [1] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of
    Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4,
    22–63. |DOI:10.1112/s1461157000000796|

.. |DOI:10.1112/s1461157000000796| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000796.svg
   :target: https://doi.org/10.1112/s1461157000000796
