.. role:: raw-math(raw)
    :format: latex html

==========================================
🛠️[WIP]🛠️FiSGO: Finite simple groups by order
==========================================

.. image:: https://readthedocs.org/projects/fisgo/badge/?version=latest
   :target: https://fisgo.readthedocs.io
   :alt: ReadTheDocs

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0.en.html
   :alt: License GPL-3.0

.. image:: https://img.shields.io/badge/python-3.12%2B-blue
   :target: https://www.python.org/
   :alt: Python Version

.. image:: https://img.shields.io/badge/status-WIP-orange
   :target: #
   :alt: Status WIP

.. image:: https://zenodo.org/badge/DOI/10.48550/arXiv.2510.00718.svg
   :target: https://doi.org/10.48550/arXiv.2510.00718
   :alt: Status WIP

..
    .. image:: https://img.shields.io/pypi/dm/<package-name>.svg
       :target: https://pypi.org/project/<package-name>/
       :alt: PyPI Downloads


FiSGO is a Python package that aims to provide a solution to the following problems:

I. Given a number :raw-math:`$k$`, identify all finite simple groups with order dividing :raw-math:`$k$`.
#. Given a range :raw-math:`$[n,m]\subset \mathbb{N}$`, identify all simple groups with complex irreducible projective
   representations of degree :raw-math:`$d\in [n,m]$`.

📖Introduction
------------
FiSGO was born as part of the author's bachelor's thesis on the classification of finite irreducible subgroups
of :raw-math:`$PGL_{n}(\mathbb{C})$`. Originally, only point (I) of the previous list was contemplated, and so the current
given name of the project.

After the defence of the bachelor's thesis, a `survey article`_ was elaborated by greatly
expanding on the literature based research, and so FiSGO was reworked and expanded to contemplate point (II).

In tackling point (II), unlike other software such as GAP, SageMath or CHEVIE, FiSGO's methods are less focused on
actual character computation, and more centered on a computational implementation of general results involving
character degrees, such as general formulas for certain groups, or providing access to already known classifications.

We think of FiSGO more like a tool to efficiently access already existing knowledge (through precomputed data or
evaluating formulas), than a tool to actually carry on heavy computational work on the group structure or
character computation. This philosophy is exemplified at the start of [Section 4.2 Survey article].

Finally, we have decided to use Python and present FiSGO as a Python package so it can be easily integrated with
SageMath. There are a few reasons for this. Firstly, SageMath can interface with other software such as [GAP4]_ and
Magma, both of which are relevant software in the character theory field. Furthermore, since FiSGO's point (II) is
more focused on data treatment and analysis than actual computation, Python seemed ideal.

🧩What can FiSGO do?
------------------
We provide a checklist of FiSGO's main features. Those which are green |check| are fully implemented, yellow ones
|empty| are partially implemented. Finally, those marked red |cross| are currently unimplemented and
in developement.

1. |check| Given a list of prime powers :raw-math:`$N = 2^a3^b5^c\cdots$`, identify all finite simple groups with
   order dividing :raw-math:`$N$`.
#. |check| Compute/access basic information of any simple group, such as its order, Schur multiplier, recommended notations
   in LaTeX, etc.
#. |check| Access to all information on ordinary character degrees and multiplicities of the sporadic groups and their coverings.
#. |check| Compute the minimal degree of a complex irreducible projective representation for any simple group as per
   the results of [TZ96]_, [Lu01a]_, [LS74]_ collected in [TZ00]_.
#. |empty| An interface to the extended Hiss-Malle table, containing all information stored in
   [[HM02]_ Table 2] alongside the omissions specified in [[HM01]_, Table 2].
#. |check| An interface to all data provided by Frank Lübeck in `his website`_ concerning all degrees of irreducible
   complex representations, together with their multiplicities, of the (non-exceptional) covering groups of Lie type of rank at most 8
#. |cross| An implementation of Tiep and Zalesskii's main theorem in [TZ96]_ (also found in [TZ00]_ as Theorem 6.1) concerning
   the relatively small complex irreducible representations of the quasisimple groups.
#. |empty| A function to search for all complex projective irreducible representation data of the simple groups stored
   in the program (as files or formulas) for a fixed degree or a range of degrees.

The above list contains all features at the top of the priority list of implementation. Other less prioritary potential features
are listed below.

9. |cross| Interface to the complete Hiss-Malle table, containing all degree less than 251 absolutely irreducible representations
   of the quasisimple groups in cross characteristic. Obtained by complementing the Hiss-Malle table with the results of
   [Lu01b]_.
#. |cross| Small rework of the search function for complex projective representations. The idea is to use directly the knowledge
   on the minimal projective representation instead of an order search using quasi-primitive group bounds.
#. |cross| Access to all known Brauer character degrees for the sporadic groups.
#. |cross| Interface to Dixon and Zalesskii's results on primitive and imprimitive simple groups of prime degree. See [DZ04]_,
   [DZ08]_ and [DZ98]_.
#. |cross| Computation of the degrees of all complex projective representations of the alternating groups.

Additionally, this GitHub repository contains a directory (``FiSGO/HissMalleTableFormats``) with a series of files in different
formats containing all the data in the Hiss-Malle tables (feature #5), such that anyone can access it and process it themselves.
For more information, refer to the documentation or ``FiSGO/HissMalleTableFormats/README.rst``.

🚦Feature status (01/01/2026)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
We breafly describe the status of the partially implemented features.

5. The only missing data is the ``field`` field in the JSON file for the groups ommited from the original Hiss-Malle
   table, i.e. those listed in the omissions table [[HM01]_, Table 2].
8. All searching logic is complete, and the function already works as intended. However, the results of this function
   can be refined once feature #7 is implemented. Furthermore, auxiliary functions to deal with the function's output
   may be needed.


📝Documentation and tutorial
--------------------------
.. image:: https://app.readthedocs.org/projects/fisgo/badge/?version=latest
    :target: https://fisgo.readthedocs.io/en/latest
    :alt: Documentation Status

All documentation for FiSGO can be found in its `readthedocs website`_, accessible through the previous link or
by clicking the badge.

A basic tutorial of all the main features and the general working of the program will be provided in the
documentation website when the main features are all implemented.

💻Installation
------------
FiSGO will be provided as a Python package available through PyPI when all its main features are implemented.
As of today (17/09/2025), this is still a work in progress. For now, all modules can be imported manually by
cloning the repository directory ``FiSGO/FiSGO/``, where all modules are contained.


🤝Acknowledgements
----------------

This project is licensed under the GNU GENERAL PUBLIC LICENSE (Version 3), see LICENSE for more details.

-------------------

The author would like to thank Professor Francesc Bars who directed the author's
bachelor's thesis and encouraged its refinement in the form of the survey which this software is based on.
His support and encouragement during the preparation of FiSGO, alongside his many comments and
revisions, have proven to be invaluable.

We would also like to thank Professor Ivan Cheltsov, for proposing turning the bachelor's thesis into
a survey in the first place; and Professor G.R. Robinson, for his assistance in accessing his PhD thesis
and his comments to improve the finished survey.

The creation and development of this software would not have been realized whithout the assistance of the aforementioned
people.

--------------------------------------------------------

| Gerard Gonzalo Calbetó
| Departament Matemàtiques, Edif. C,
| Universitat Autònoma de Barcelona,
| 08193 Bellaterra, Catalonia, Spain
| ggonzalo.math@gmail.com // gerard.gonzalo@uab.cat

📚Project wide references
-----------------------

.. _readthedocs website: https://fisgo.readthedocs.io/en/latest
.. _survey article: https://doi.org/10.48550/arXiv.2510.00718
.. _his website: https://www.math.rwth-aachen.de/~Frank.Luebeck/chev/DegMult/index.html?LANG=en
.. |check| replace:: 🟩
.. |empty| replace:: 🟨
.. |cross| replace:: 🟥


.. [HM01] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of
    Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4,
    22–63. |DOI:10.1112/s1461157000000796|

.. [HM02] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional
    Representations of Quasi-simple Groups. LMS Journal of Computation and
    Mathematics, 5, 95–126. |DOI:10.1112/s1461157000000711|

.. [Wi25] Wikipedia contributors. (2025, August 22). List of finite simple
    groups. In Wikipedia, The Free Encyclopedia. Retrieved 21:49, August 30,
    2025, from |image1|

.. [GAP4] The GAP Group, GAP – Groups, Algorithms, and Programming,
    Version 4.14.0; 2024. (https://www.gap-system.org)

.. [OEIS] OEIS Foundation Inc.(2025), The On-Line Encyclopedia of Integer
    Sequences, Published electronically at https://oeis.org.

.. [TZ00] Tiep, P. H., & Zalesskii, A. E. (2000). Some aspects of finite
    linear groups: A survey. Journal of Mathematical Sciences, 100(1),
    1893–1914. |DOI:10.1007/bf02677502|

.. [TZ96] Tiep, P. H., & Zalesskii, A. E. (1996). Minimal characters of
    the finite classical groups. Communications in Algebra, 24(6),
    2093–2167. |DOI:10.1080/00927879608825690|

.. [LS74] Landazuri, V., & Seitz, G. M. (1974). On the minimal degrees of
    projective representations of the finite Chevalley groups. Journal of
    Algebra, 32(2), 418–443. |DOI:10.1016/0021-8693(74)90150-1|

.. [Lu01a] Lübeck, F. (2001). Smallest degrees of representations of
    exceptional groups of lie type. Communications in Algebra, 29(5),
    2147–2169. |DOI:10.1081/agb-100002175|

.. [Lu01b] Lübeck, F. (2001). Small Degree Representations of
    Finite Chevalley Groups in Defining Characteristic. LMS Journal of
    Computation and Mathematics, 4, 135–169. |DOI:10.1112/s1461157000000838|

.. [DZ04] Dixon, J. D., & Zalesski, A. E. (2004). Finite imprimitive linear
    groups of prime degree. Journal of Algebra, 276(1), 340–370. |DOI:10.1016/j.jalgebra.2004.02.005|

.. [DZ08] Dixon, J. D., & Zalesskii, A. E. (2008). Finite primitive linear
    groups of prime degree. Journal of the London Mathematical Society, 77(3), 808–812. |DOI:10.1112/jlms/jdm103|

.. [DZ98] Dixon, J. D., & Zalesskii, A. E. (1998). Finite Primitive Linear Groups of Prime Degree.
    Journal of the London Mathematical Society, 57(1), 126–134. |DOI:10.1112/s0024610798005778|


.. |Static Badge| image:: https://img.shields.io/badge/OEIS-A000040-blue
   :target: https://oeis.org/A000040
.. |DOI:| image:: https://zenodo.org/badge/DOI/.svg
   :target: https://doi.org/
.. |DOI:10.1112/s0024610798005778| image:: https://zenodo.org/badge/DOI/10.1112/s0024610798005778.svg
   :target: https://doi.org/10.1112/s0024610798005778
.. |DOI:10.1112/jlms/jdm103| image:: https://zenodo.org/badge/DOI/10.1112/jlms/jdm103.svg
   :target: https://doi.org/10.1112/jlms/jdm103
.. |DOI:10.1016/j.jalgebra.2004.02.005| image:: https://zenodo.org/badge/DOI/10.1016/j.jalgebra.2004.02.005.svg
   :target: https://doi.org/10.1016/j.jalgebra.2004.02.005
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
.. |DOI:10.1112/s1461157000000838| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000838.svg
   :target: https://doi.org/10.1112/s1461157000000838
