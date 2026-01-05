
Precomputed Data
================

The operation of FiSGO requires some data that has already been computed
at some point.

In this folder, we store the files containing key information to be used
in the different modules of FiSGO. The data currently stored includes:

- The first 10^5 prime numbers.
- Data on almost all absolutely irreducible representations of the
  quasi-simple groups, compiled and partially computed by Hiss and Malle
  in [[1]_], [[2]_].
- Data on all properties of the sporadic simple groups (and their
  covers) relevant to FiSGO.
- Lower bounds to the degree of zero characteristic projective
  representations of the simple groups. Mainly due to Landazuri, Seitz,
  Tiep and Zalesskii.
- `Lübeck's data <https://www.math.rwth-aachen.de/~Frank.Luebeck/chev/DegMult/index.html?LANG=en>`_
  on the projective representations of finite simple groups of Lie type with non-exceptional
  Schur multiplier. Available in his `website <https://www.math.rwth-aachen.de/~Frank.Luebeck/chev/DegMult/index.html?LANG=en>`_.


Description of the files
------------------------

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
  - ``"ind"``: Frobenius-Schur indicators. See [[1]_, :math:`\S` 5].
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

- ``Lubeck/Lubeck_[ID].json``: A collection of JSON files, one per Lie type simple group family. Each file
  contains all information on the degrees of projective representations of such groups up to rank 8, with the
  exception of those groups of Lie type with an exceptional Schur multiplier.

  The top level of each file consists of a JSON object with a single field, which depends on the number of parameters
  of the group:
    - Uniparametric: The field is simply the group ID string. Example: "RF".
    - Biparametric: Each field contains the group ID followed by the dimensional parameter. Example: "CA-2", "SD-5".

  With the exception of the groups with ID: "RF", "SZ" and "RG"; each of the above fields contains an array
  of JSON objects with the following fields:
    - ``"files"``: An array containing the names of the original files indexed in the current object. The names are
      the ones as downloaded from `Lübeck's website <https://www.math.rwth-aachen.de/~Frank.Luebeck/chev/DegMult/index.html?LANG=en>`_
    - ``"mod"``: Representations are grouped by the modularity of the :math:`q` parameter of the group. This field
      contains the integer indicating such modularity. Example: If we care aboud :math:`q \mod 4`, then this field contains
      the number 4.
    - ``"mod_groups"``: Certain modular values produce the same representations, so they are grouped together. We label
      such groups as ``"0"``, ``"1"``, ``"2"``, ect., this field provides a correspondence between the group labels and
      the actual modular values. Example: if ``"mod" : 4`` then a possible value for this field
      is ``{"0": [0, 2], "1": [1], "2": [3]}``. This field is ``null`` whenever ``"mod" : 0``.
    - ``"irreps"``: For each modularity group, an array of JSON objects is given, each corresponding to a different
      representation and with the following fields:
        - ``"degree"``: A rational polynomial with variable :math:`q` given as a list of integer coefficients and a
          common divisor, which is a single integer that divides all integer coefficients.
          Example: [[1, -1, 2, -1, 1, 0], 2]. This polynomial represents the degree of the representation in terms of
          the group parameter :math:`q`.
        - ``"mult"``: Same as the previous field. This polynomial represents the multiplicity of the representation
          in terms of the group parameter :math:`q`.

  For the cases of the groups with ID: "RF", "SZ" and "RG"; all fields are the same except for the ones inside ``"irreps"``.
  This case contained a difficulty: the polynomials were not rational, they contained multiples of :math:`\sqrt{2}` for
  "SZ" and "RF", and multiples of :math:`\sqrt{3}` for "RG". I.e. their fields of definition were :math:`\mathbb{Q}(\sqrt{2})`
  and :math:`\mathbb{Q}(\sqrt{3})` respectively. This is due to the parameter :math:`q` being taken as
  :math:`q^2 = 2^{2*n+1}` or :math:`q^2 = 3^{3*n+1}` where :math:`n` is the actual parameter used for these families.

  Nevertheless, the values these polynomials take are integer values, and :math:`q^2` is an integer. Thus, we store
  two rational polynomials in the same form as above. The first polynomial corresponds to the even coefficients and
  the second to the odd ones quotient :math:`\mathbb{Q}(\sqrt{k})` for :math:`k=2,3` depending on the case. Example:
    - ``"degree"``: ``[[[1, 0, -1], 1], [[-1, 1], 1]]``
    - ``"mult"``: ``[[[1, 0], 4], [[1], 4]]``
  To evaluate this polynomial, note :math:`q^2` is an integer and :math:`\sqrt{k}q` is also an integer. Thus, if
  :math:`p(q)` represents the original polynomial over :math:`\mathbb{Q}(\sqrt{k})`, this can be writen as follows:
    - Consider :math:`p_0(x)`, :math:`p_1(x)` the rational polynomials corresponding to the even and odd coefficients.
      For the above example of the degree, :math:`p_0(x)=x^2-1` and :math:`p_1(x)=-x+1`.
      Then :math:`p(q) = p_0(q^2) + \sqrt{k}q p_1(q^2)`. In this way, the evaluation is completely done over the rationals
      and we avoid precision problems.

- ``Lubeck/Lubeck_exceptional_mult.json``: A JSON file containing the degrees and multiplicities of the linear irreducible
  representations of the Schur coverings of Lie type groups with exceptional Schur multiplier. Currently some groups are
  missing. The file contains a single JSON object with the normalized codes as fields. Each field provides an array
  of (degree, multiplicity) pairs. The trivial representation is omitted.


Source of the data
------------------

We now provide a detailed description of how and where the data was
obtained. We give a description for each file:

- ``BuiltinPrimes.txt``: Taken form the OEIS [[5]_] sequence |Static Badge|
  . The table was contributed by N. J. A. Sloane and can be found
  `here <https://oeis.org/A000040/a000040.txt>`__.
- ``Hiss_Malle_data.json``: All fields except ``"code"`` were obtained
  from Hiss and Malle [[2]_, Table 2]. All data has been treated in
  accordance to the description of the table in [[1]_, :math:`\S` 6].
  For further details, see the repository’s ``HissMalleTableFormats``
  directory README. The ``"code"`` field is particular to FiSGO.

  - ``smallest_pirrep_degree_exceptions.json``: The ``"code"`` field is
    particular to FiSGO. All other fields were obtained manually from
    the tables [[6]_, Table 1, Table 2] in a survey of Tiep and Zalesskii
    [[6]_]. The original results can be found in [[7]_], [[8]_] and [[9]_].

- ``sporadic_groups_data.json``: The ``"order"``, ``"latex_name"`` and
  ``"multiplier"`` fields were obtained from Wikipedia [[3]_]. Fields
  ``"id"`` and ``"code"`` are particular to FiSGO. The data in the
  ``"pirreps"`` field was obtained from the GAP [[4]_] database of
  character tables CTblLib. The script used can be found in
  ``DataProcessingScripts/GAP_sporadic_extraction.g``.
- ``Lubeck/Lubeck_[ID].json``: All data is sourced from
  `Lübeck's website <https://www.math.rwth-aachen.de/~Frank.Luebeck/chev/DegMult/index.html?LANG=en>`_ and should be
  credited to him.
- ``Lubeck/Lubeck_exceptional_mult.json``: All data except for ``"SA-3-3_1"`` has been obtained using GAP. We have used
  GAP's database of character tables for those whose Schur covering was present. We have used GAP's database of perfect
  groups to find the remaining Schur covers, and used GAP standard functions to compute the character tables.
  Finally, the character table of ``"SA-3-3_1"`` has been computed using GAP standard functions using a permutation
  representation computed by A. Hulpke, it can be found in his `GitHub <https://github.com/hulpke/perfect/blob/main/particulars/coveru43.g>`_


References
----------

.. [1] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of
    Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4,
    22–63. |DOI:10.1112/s1461157000000796|

.. [2] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional
    Representations of Quasi-simple Groups. LMS Journal of Computation and
    Mathematics, 5, 95–126. |DOI:10.1112/s1461157000000711|

.. [3] Wikipedia contributors. (2025, August 22). List of finite simple
    groups. In Wikipedia, The Free Encyclopedia. Retrieved 21:49, August 30,
    2025, from |image1|

.. [4] The GAP Group, GAP – Groups, Algorithms, and Programming,
    Version 4.14.0; 2024. (https://www.gap-system.org)

.. [5] OEIS Foundation Inc.(2025), The On-Line Encyclopedia of Integer
    Sequences, Published electronically at https://oeis.org.

.. [6] Tiep, P. H., & Zalesskii, A. E. (2000). Some aspects of finite
    linear groups: A survey. Journal of Mathematical Sciences, 100(1),
    1893–1914. |DOI:10.1007/bf02677502|

.. [7] Landazuri, V., & Seitz, G. M. (1974). On the minimal degrees of
    projective representations of the finite Chevalley groups. Journal of
    Algebra, 32(2), 418–443. |DOI:10.1016/0021-8693(74)90150-1|

.. [8] Lübeck, F. (2001). Smallest degrees of representations of
    exceptional groups of lie type. Communications in Algebra, 29(5),
    2147–2169. |DOI:10.1081/agb-100002175|

.. [9] Tiep, P. H., & Zalesskii, A. E. (1996). Minimal characters of
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
