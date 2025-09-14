
Precomputed Data
================

The operation of FiSGO requires some data that has already been computed
at some point.

In this folder, we store the files containing key information to be used
in the different modules of FiSGO. The data currently stored includes:

- The first 10^5 prime numbers.
- Data on almost all absolutely irreducible representations of the
  quasi-simple groups, compiled and partially computed by Hiss and Malle
  in [1], [2].
- Data on all properties of the sporadic simple groups (and their
  covers) relevant to FiSGO.
- Lower bounds to the degree of zero characteristic projective
  representations of the simple groups. Mainly due to Landazuri, Seitz,
  Tiep and Zalesskii. ## Description of the files

In the sequel, we describe the content of each file.

- ``BuiltinPrimes.txt``: A txt file containing the first 10^5 prime
  numbers. Each line contains a single prime number. The prime numbers
  are stored in increasing order, with line 1 containing the first prime
  number, line 2 containing the second prime number, etc.

- ``Hiss_Malle_data.json``: A JSON file containing the data on almost
  all absolutely irreducible representations of the quasi-simple groups.
  A discussion on the missing representations is given in the
  repository’s folder ``HissMalleTableFormats`` README. The file
  consists of an array of JSON objects, each of which contains the data
  on a single representation. The objects have the following fields:

  - ``"degree"``: Degree of the representation.
  - ``"name"``: Name of the quasi-simple group in LaTeX.
  - ``"field"``: Irrationalities of the Brauer characters.
  - ``"ind"``: Frobenius-Schur indicators. See [1, :math:`\S` 5].
  - ``"char"``: Field characteristics where the representation is
    defined. If ``null``, then all characteristics are admited unless
    stated otherwise in ``"not_char"``.
  - ``"not_char"``: Field characteristics where the representation is
    **NOT** defined. In ``null``, then all characteristics are admited
    unless stated otherwise in ``"char"``.
  - ``"code"``: FiSGO’s simple group code of :math:`G/Z(G)`. If the
    group is simple, then the code is simply that of the group. If the
    group is a cover of a simple group, the code of the associated
    simple group (:math:`G/Z(G)`) is given.

- ``smallest_pirrep_degree_exceptions.json``: A JSON file containing
  exceptions to the lower-bound formulas for the degree of zero
  characteristic projective representations of the simple groups, mainly
  due to Landazuri, Lübeck, Seitz, Tiep and Zalesskii. The file consists
  of an array of JSON objects, each of which contains the data on a
  single group (up to isomorphism). The objects have the following
  fields:

  - ``"code"``: An array of FiSGO’s simple group codes. All the codes
    conform the same simple group (up to isomorphism).
  - ``"degree"``: Lower bound on the degree of zero characteristic
    projective representations of the simple groups.
  - ``"irreps"``: Number of distinct irreducible representations of the
    given ``"degree"``.

- ``sporadic_groups_data.json``: A JSON file containing the data on all
  properties of the sporadic simple groups (and their covers) relevant
  to FiSGO. The file consists of an array of JSON objects, each of which
  contains the data on a single group (up to isomorphism). The objects
  have the following fields:

  - ``"code"``: FiSGO’s simple group code.
  - ``"id"``: A unique identifier of the sporadic group.
  - ``"order"``: Order of the group.
  - ``"latex_name"``: List of possible notations for the group in LaTeX.
  - ``"multiplier"``: Schur multiplier of the group.
  - ``"pirreps"``: Array of JSON objects, each of which contains the
    data on the irreducible representations of a cover of the sporadic
    group. The objects have the following fields:

    - ``"name"``: A possible notation for the cover in LaTeX.
    - ``"degrees"``: Degrees of the irreducible representations. Given
      as a list of pairs, each pair contains the degree of an
      irreducible representation and the number of distinct irreducible
      representations of that degree.

Source of the data
------------------

We now provide a detailed description of how and where the data was
obtained. We give a description for each file:

- ``BuiltinPrimes.txt``: Taken form the OEIS [5] sequence |Static Badge|
  . The table was contributed by N. J. A. Sloane and can be found
  `here <https://oeis.org/A000040/a000040.txt>`__.
- ``Hiss_Malle_data.json``: All fields except ``"code"`` were obtained
  from Hiss and Malle [2, Table 2]. All data has been treated in
  accordance to the description of the table in [1, :math:`\S` 6].
  For further details, see the repository’s ``HissMalleTableFormats``
  directory README. The ``"code"`` field is particular to FiSGO.

  - ``smallest_pirrep_degree_exceptions.json``: The ``"code"`` field is
    particular to FiSGO. All other fields were obtained manually from
    the tables [6, Table 1, Table 2] in a survey of Tiep and Zalesskii
    [6]. The original results can be found in [7], [8] and [9].

- ``sporadic_groups_data.json``: The ``"order"``, ``"latex_name"`` and
  ``"multiplier"`` fields were obtained from Wikipedia [3]. Fields
  ``"id"`` and ``"code"`` are particular to FiSGO. The data in the
  ``"pirreps"`` field was obtained from the GAP [4] database of
  character tables CTblLib. The script used can be found in
  ``DataProcessingScripts/GAP_sporadic_extraction.g``.

References
----------

**[1]** Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of
Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4,
22–63. |DOI:10.1112/s1461157000000796|

**[2]** Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional
Representations of Quasi-simple Groups. LMS Journal of Computation and
Mathematics, 5, 95–126. |DOI:10.1112/s1461157000000711|

**[3]** Wikipedia contributors. (2025, August 22). List of finite simple
groups. In Wikipedia, The Free Encyclopedia. Retrieved 21:49, August 30,
2025, from |image1|

**[4]** The GAP Group, GAP – Groups, Algorithms, and Programming,
Version 4.14.0; 2024. (https://www.gap-system.org)

**[5]** OEIS Foundation Inc.(2025), The On-Line Encyclopedia of Integer
Sequences, Published electronically at https://oeis.org.

**[6]** Tiep, P. H., & Zalesskii, A. E. (2000). Some aspects of finite
linear groups: A survey. Journal of Mathematical Sciences, 100(1),
1893–1914. |DOI:10.1007/bf02677502|

**[7]** Landazuri, V., & Seitz, G. M. (1974). On the minimal degrees of
projective representations of the finite Chevalley groups. Journal of
Algebra, 32(2), 418–443. |DOI:10.1016/0021-8693(74)90150-1|

**[8]** Lübeck, F. (2001). Smallest degrees of representations of
exceptional groups of lie type. Communications in Algebra, 29(5),
2147–2169. |DOI:10.1081/agb-100002175|

**[9]** Tiep, P. H., & Zalesskii, A. E. (1996). Minimal characters of
the finite classical groups. Communications in Algebra, 24(6),
2093–2167. |DOI:10.1080/00927879608825690|

.. |Static Badge| image:: https://img.shields.io/badge/OEIS-A000040-blue
   :target: https://oeis.org/A000040
.. |DOI:10.1112/s1461157000000796| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000796.svg
   :target: https://doi.org/10.1112/s1461157000000796
.. |DOI:10.1112/s1461157000000711| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000711.svg
   :target: https://doi.org/10.1112/s1461157000000711
.. |image1| image:: https://img.shields.io/badge/Wikipedia-List_of_finite_simple_groups-blue
   :target: https://en.wikipedia.org/w/index.php?title=List_of_finite_simple_groups&oldid=1307206155
.. |DOI:10.1007/bf02677502| image:: https://zenodo.org/badge/DOI/10.1007/bf02677502.svg
   :target: https://doi.org/10.1007/bf02677502
.. |DOI:10.1016/0021-8693(74)90150-1| image:: https://zenodo.org/badge/DOI/10.1016/0021-8693(74)90150-1.svg
   :target: https://doi.org/10.1016/0021-8693(74)90150-1
.. |DOI:10.1081/agb-100002175| image:: https://zenodo.org/badge/DOI/10.1081/agb-100002175.svg
   :target: https://doi.org/10.1081/agb-100002175
.. |DOI:10.1080/00927879608825690| image:: https://zenodo.org/badge/DOI/10.1080/00927879608825690.svg
   :target: https://doi.org/10.1080/00927879608825690
