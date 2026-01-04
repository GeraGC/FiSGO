FiSGO Tutorial
################

.. contents::

================
1. Introduction
================

The aim of this tutorial is to introduce and showcase FiSGO's main features
and give usage examples of its various capabilities.

.. important::
    Before proceeding to the tutorial, we strongly recommend reading the
    :doc:`Homepage </index>`'s :ref:`Homepage_intro`, :ref:`Homepage_wcfd`
    and :ref:`Homepage_doc` sections.

FiSGO's functionalities are split across four modules:

    - :py:mod:`FiSGO.SimpleGroups`: Main functions and classes implementing access to all data available
      for all classes of simple groups. We explore this module in :ref:`Section 2 <2. Simple group classes>` and
      :ref:`Section 5 <5. Group Databases>`.
    - :py:mod:`FiSGO.PrimesHandler`: Functions to deal with prime factorizations efficiently tailored to FiSGO's
      needs. We explore this module in the :ref:`Interlude <3. Interlude>`.
    - :py:mod:`FiSGO.OrderSearch`: Functions to search for simple groups given some
      order bounds. We explore this module in :ref:`Section 4 <4. Origin>`.
    - :py:mod:`FiSGO.PIrrepsSearch`: Functions to search for projective representation data
      for simple groups. We explore this module in the :ref:`Section 6 <6. Searching>`.

Throughout this tutorial, all code will be written according to the following import statements:

    >>> import FiSGO.SimpleGroups as sg
    >>> import FiSGO.PrimesHandler as ph
    >>> import FiSGO.OrderSearch as os
    >>> import FiSGO.PIrrepsSearch as pis

This way, it is clear the origin of each function and class at all stages of this tutorial, whenever any code may appear.

.. _2. Simple group classes:

========================
2. Simple group classes
========================

In this section, we will explore the basics of representing simple groups in our Python code, how to access some of
their properties and how we can quickly refer to any simple group using a 'standard' method. This section focuses on
the :py:mod:`FiSGO.SimpleGroups` module.

In FiSGO, we represent simple groups as instances of the class :code:`sg.SimpleGroup` and their respective subclasses.
Each family of simple groups has a class associated to it. These classes are named after the groups as in `Wikipedia's
list of finite simple groups <https://en.wikipedia.org/wiki/List_of_finite_simple_groups>`_. For example, to create
a Chevalley type D group object with :math:`n=5` and :math:`q=8` we would write:

    >>> my_group = sg.ChevalleyD(5,8)

The naming sense of all classes follows a similar convention as above. For instance,
:py:class:`FiSGO.SimpleGroups.ExceptionalChevalleyE8` is
the class for the Exceptional Chevalley groups :math:`E_8(q)`, :py:class:`FiSGO.SimpleGroups.Suzuki` refers
to the Suzuki :math:`{}^2B_2(2^{2n+1})` groups with parameter :math:`n`, etc.

.. tip::
    You can find all names for the classes representing the various simple groups
    under the section `Classes` in the documentation page
    :py:mod:`FiSGO.SimpleGroups` of the module.

With the group object created, we can access some of its methods, for instance, we may request some basic properties
such as the order of the group or its Schur multiplier:

    >>> my_group.order()
    42863636354909175368011800612065142374400
    >>> my_group.multiplier()
    1

Other interesting capabilities include checking if the group is isomorphic to any other group in a different family,
the size of its p-Sylow groups or getting some of its usual notations in a LaTeX format:

    >>> my_group.isomorphisms()
    []
    >>> my_group.p_sylow_power(3)
    9
    >>> my_group.latex_name()
    ['D_{5}(8)', '{\\rm O}^+_{10}(8)', '{\\rm O}^+({10}, 8)', '{\\rm P}\\Omega^+_{10}(8)', '{\\rm P}\\Omega^+({10}, 8)']

In this case, the first function produces an empty list, as :math:`D_5(8)` has no isomorphisms to other classes, the
second returns :code:`9` as :math:`3^9` is the largest power of 3 dividing the order of the group, and the last one
produces::

    ['D_{5}(8)', '{\\rm O}^+_{10}(8)', '{\\rm O}^+({10}, 8)', '{\\rm P}\\Omega^+_{10}(8)', '{\\rm P}\\Omega^+({10}, 8)']

Note that this is not directly in a LaTeX format, as the backslashes are escaped, this is made such that Python properly
prints the strings. The appropriate way of displaying this is using :code:`print` on each string, for example:

    >>> print(my_group.latex_name()[1])
    {\rm O}^+_{10}(8)

Now it returned :code:`{\rm O}^+_{10}(8)` which is the correct LaTeX string. This is specially useful when writing the groups to
a file.

.. tip::
    You can check out all methods of the base class :code:`sg.SimpleGroup` in the documentation :py:mod:`FiSGO.SimpleGroups`.
    You can also check the documentation of any subclass by clicking on its name in the classes list.

------------------------
2.1. Simple group codes
------------------------

Since each simple group family has its own class, the creation of these objects can get rather tedious. This is why
we introduce the idea of `simple group codes`. These `codes` are strings which uniquely identify any simple group. They
must encode:

    #. The group family.
    #. The parameters of the group (if any).
    #. For the sporadic groups, a way to identify each group instead of considering parameters.

With this premise, our simple group codes are structured as follows::

    [group ID]-[first parameter/sporadic ID]-[second parameter]

Here the different parts of the code are as follows:

    - **group ID**: Formed by exactly two alphanumerical characters, it identifies the simple group family. For example,
      the letters ``CA`` identify Chevalley type A groups, while ``E6`` identifies Exceptional Chevalley groups and ``SP`` the
      sporadic groups. See :doc:`_autosummary/FiSGO.SimpleGroups.simple_group_ids` for a complete list, or run the function
      :code:`sg.simple_group_ids()`.
    - **first parameter/sporadic ID**: This part is optional depending on the number of parameters of the family.
        - **Zero-parametric group**: The code terminates here and no parameter is added. Example: Tits group code: ``TT``.
        - **Uniparametric group**: The group only has a parameter, so we add it here. Example: ``E6-9``.
        - **Biparametric group**: The group has two parameters, a dimensional parameter "n" and a finite field parameter
          "q". In this case, the first parameter is "n". Example: ``CA-6-25`` where n=6, q=25.
        - **Sporadic group**: If the group is sporadic, then this first parameter corresponds to the name of the sporadic
          group as in `Wikipedia <https://en.wikipedia.org/wiki/List_of_finite_simple_groups>`_. A list of these sporadic
          ID's can be viewed using the function :code:`sg.sporadic_group_ids()`.
    - **second parameter**: Only for biparametric groups, contains the finite field parameter
          "q". Example: ``CA-6-25`` where n=6, q=25.

Furthermore, the parameters corresponding to the finite field parameter "q" can be expressed in two different ways up
to convenience. Since "q" is always a prime power, one may choose to write the full number or a pair containing the
prime and its power. The first is the *simple* syntax, while the second is called *normalized*:

    - **Simple syntax**: We write "q" numerically. Some examples include ``CA-1-2``, ``CD-4-25``, ``E8-169``, ``SD-6-8``.
    - **Normalized syntax**: We write "q" as a pair ``[prime]_[power]``. The previous examples in normalized form:
      ``CA-1-2_1``, ``CD-4-5_2``, ``E8-13_2``, ``SD-6-2_3``.

.. note::
    A code whose syntax is normalized is called a *normalized code*. Internally, FiSGO always uses the normalized syntax.

It is convenient to consider a few examples to get familiar with the group code concept. Consider the following table:

==============      ============================================================================================
Group code          Description
==============      ============================================================================================
CA-3-2              Chevalley group :math:`A_3(2)` with paramaters (n,q) = (3,2). Simple syntax.
CC-7                Cyclic group :math:`C_7` of order 7.
AA-26               Alternating :math:`A_{26}` group of order 26.
CD-6-625            Chevalley group D :math:`D_6(625)` with parameters (n,q) = (6,625). Simple syntax.
CD-6-5_4            Chevalley group D :math:`D_6(625)` with parameters (n,q) = (6,625=5^4). Normalized syntax.
2E-9                Exceptional Steinberg group :math:`{}^2E_6(9^2)` with parameter q=9. Simple syntax.
G2-13_1             Exceptional Chevalley group :math:`G_2(13)` with parameter q=13. Normalized syntax.
SP-He               Sporadic Held group :math:`{\rm He}`.
SP-M11              Sporadic Mathieu 11 group :math:`{\rm M}_{11}`.
SP-Fi24'            Sporadic Fischer group 24 (derived subgroup) :math:`{\rm Fi}_{24}'`.
==============      ============================================================================================

.. danger::
    The symbol ``'`` must be properly typeset when giving the group code. The recommended way is to use the raw
    string :code:`r"SP-Fi24'"`. Otherwise, the code might be invalid.

Let us return to the initial code example:

    >>> my_group = sg.ChevalleyD(5,8)

We can easily obtain its codes via:

    >>> my_group.code()
    'CD-5-8'
    >>> my_group.normalized_code()
    'CD-5-2_3'

Similarly, we can use codes to obtain simple group objects. This can be done in two ways, let us obtain a simple
group object from the code ``RF-5`` which corresponds to the Ree group :math:`{}^2F_4(2^{11})`.

>>> group_first_way = sg.SimpleGroup.from_code("RF-5")
>>> group_second_way = sg.simple_group("RF-5")

Both methods produce the same result, so it is left to the user's convenience.

.. note::
    An advantage of being able to store each group as a string rather than as a class object is external storage.
    If we want to store a list of interesting groups, we can just save the codes to a text file, which we may read later.
    This also helps reduce memory usage internally in cases when one does not need the object itself, but rather just
    requires a way to identify the group for later use. It is more memory efficient to store a string than a class object.


-------------------------------------------------------------
2.2. Zero-parametric, uniparametric and biparametric groups.
-------------------------------------------------------------

Internally, FiSGO separates the simple groups into three different types:

    - Zero-parametric groups: Simple groups with no parameters, these are the Tits group ``TT`` and the sporadics.
    - Uniparametric groups: Simple groups whose family is determined by a single parameter. Examples are the Suzuki
      groups, alternating groups or the exceptional chevalley groups are examples of these groups.
    - Biparametric groups: Simple groups whose family is determined by two parameters, these are the Chevalley and
      Steinberg groups.

This separation matters when we need to access the parameters of each group type. Let us show it through some examples.

Take the groups ``SA-3-25`` and ``G2-17_2``, let us create their group objects and access their parameters:

>>> biparametric = sg.simple_group("SA-3-25")
>>> uniparametric = sg.simple_group("G2-17_2")

Let us start with the uniparametric case. In this situation, the unique parameter can be accessed in two ways:

>>> uniparametric.par
(17,2)
>>> uniparametric.par_value()
289

Notice that we have created the group from the normalized code ``G2-17_2``. Thus, the parameter has been stored as a pair
separating the prime and the power. To obtain the actual value of the parameter, we must use the :code:`par_value()`.

.. note::
    The :code:`par_value()` method will always give the integer value of the parameter, independently of the value of
    :code:`par`.

In the biparametric case, we can access the parameters as follows:

>>> biparametric.n
3
>>> biparametric.q
25
>>> biparametric.q_value()
25

The parameter "n" always refers to the dimensional parameter and "q" is a prime power. While "n" will always be
an integer, "q" may be given as a pair of integers as before. In such case, the method :code:`q_value()` will
always give an integer value.

.. warning::

    Trying to access a parameter using the wrong method for the group type will raise an error.

--------------------------------
2.3. Some common/useful methods
--------------------------------

We finish this section of the tutorial briefly introducing the rest of the methods of the :code:`sg.SimpleGroup` class.
For the examples, we will use the group ``CA-3-5`` for the examples.

>>> group = sg.simple_group("CA-3-5")

.. admonition:: sg.SimpleGroup.GAP_name

    Returns a string with the name of the simple group in GAP4/Atlas like notation.
    See :py:meth:`FiSGO.SimpleGroups.SimpleGroup.GAP_name` for the full documentation.

>>> group.GAP_name()
'L4(5)'

.. admonition:: sg.SimpleGroup.hiss_malle_pirreps

    This function looks for projective representations of degree up to 250 from the Hiss-Malle database.
    See `Section 4.2 <4.2.Hiss_Malle_Data>`_ and :py:meth:`FiSGO.SimpleGroups.SimpleGroup.hiss_malle_pirreps`
    for the full documentation.

>>> group.hiss_malle_pirreps()
[155, 156, 248]

.. admonition:: sg.SimpleGroup.lubeck_pirreps

    This function computes degrees of projective representations of Lie type groups of rank at most 8. The multiplicity
    corresponds to that of the linear irreducible characters of the Schur covering.
    See `Section 4.3 <4.3.Lubeck_data>`_ and :py:meth:`lubeck_pirreps <FiSGO.SimpleGroups.SimpleGroup.lubeck_pirreps>`
    for the full documentation.

>>> group.lubeck_pirreps() # Output shortened!
[[155, 1], [156, 3], [248, 2], [403, 2], [496, 2], [650, 1],..., [24180, 3]]

.. admonition:: sg.SimpleGroup.smallest_pirrep_degree

    Using the bounds of Seitz, Landazuri, Tiep and Zalesskii, returns the degree of the smallest non-trivial projective
    irreducible complex representation of the simple group.
    See :py:class:`FiSGO.SimpleGroups.SimpleGroup` for the full documentation.

>>> group.smallest_pirrep_degree()
(155, 1)

.. _3. Interlude:

==============================
 Interlude: Prime handling
==============================

We open a brief interlude to talk about the :py:mod:`FiSGO.PrimesHandler` module. This should be regarded as an internal
module, and it is unlikely the end-user would need to access it fully. It mainly contains routines devoted to prime
factorization and listing primes. The main takeaway, and the reason we talk about it at all, is the following warning.

.. warning::

    FiSGO works with a precomputed list of the first :math:`10^5` prime numbers to handle factorizations, prime
    recognition, and any operation related to prime numbers.

While we consider it unlikely for any operation using FiSGO to exceed this limit, checks are put in place such that,
should the need arise, the user will be notified or an error will be raised. In such scenario, the user can provide
their own path to a larger list by changing the constant :py:const:`FiSGO.PrimesHandler.PRIMES_PATH`. The file should be a
text file where each line contains a prime number, in ascending order (2 in the first line).

There are a couple functions which may be situationally relevant, and we introduce them as needed throughout this
tutorial as additional "tips". However, we won't go into much detail.

Finally, should anyone wish to use any functions in the :py:mod:`FiSGO.PrimesHandler` module, it is fully documented.

.. _4. Origin:

==================================================
3. FiSGO's origin: Simple groups from their order
==================================================

Having established how to deal with the simple group objects and classes, we move on to one of the first applications
of FiSGO, contained in the module :py:mod:`FiSGO.OrderSearch`.

.. tip::
    You can check out the full documentation for this section on :py:mod:`FiSGO.OrderSearch`.

Let us first define what is the main goal of this module:

.. admonition:: Main goal

    Given an integer :math:`M`, determine all non-abelian finite simple groups of order :math:`g` such that :math:`g \mid M`, i.e.
    determine all finite simple groups whose order divides the bound :math:`M`.

The high-level function that fulfills this goal is :py:func:`FiSGO.OrderSearch.simple_group_by_order`. Let us detail
how to use it through an example. Consider :math:`M = 119952 = 2^4 3^2 7^2 17^1`, since we are interested in divisibility,
we can arrange the bound as a list of prime powers: ``[4,2,0,2,0,0,1]``, which is the same as writing
:math:`2^4 3^2 5^0 7^2 11^0 13^0 17^1`. This is the only required argument, and it must be given in list form.

>>> import FiSGO.OrderSearch as os
>>> os.simple_group_by_order([4,2,0,2,0,0,1])
['CA-2-2_1', 'CA-1-2_3', 'CA-1-17_1']

.. tip::
    Depending on the use case, writing out the list of primes may be rather tedious. Imagine our bound is
    :math:`2^{10} 11^{10} 223^{10} 233^{10}`. Since 223 is the 51st prime, the list turns out rather long and with
    lots of zeros. In such case, the function :py:func:`FiSGO.PrimesHandler.prime_scanner` can come in very handy:

        >>> ph.prime_scanner(2**10*11**10*223**10*233**10, 234) # Output reduced!
            ([10, 0, 0, 0, 10, 0,..., 0, 0, 10, 0, 0, 10], 1)

    Check the documentation of :py:func:`FiSGO.PrimesHandler.prime_scanner` (click it!) for more details on the given
    parameters and output.


Thus, the groups satisfying the bounds are :math:`{\rm PSL}_{3}(2), {\rm PSL}_{2}(8), {\rm PSL}_{2}(17)`, in
their classical group notation. This function accepts three keyword arguments. These arguments are: ``abs_bound``,
``return_codes`` and ``ignore``. The first allows us to specify an upper bound :math:`N` to the order of the found
groups, i.e. only consider groups that divide :math:`M` and with order less than or equal to :math:`N`.

>>> os.simple_group_by_order([4,2,0,2,0,0,1], abs_bound=1000)
['CA-2-2_1', 'CA-1-2_3']

Note that the order of :math:`{\rm PSL}_{2}(17)` is 2448 while the other two do not exceed 1000. By default, no
absolute bound is imposed.

The parameter ``return_codes`` allows us to choose if the function should return a list of codes or a list of simple
group objects. As seen, by default it returns codes. Finally, ``ignore`` allows us to skip some group families we may
not be interested in. This parameter accepts a list of group ID's:

>>> os.simple_group_by_order([4,2,0,2,0,0,1], ignore=["CA", "AA"])
[]

Since all the candidates were Chevalley A groups, and we ignore them, we do not find any groups.

.. hint::

    Should you be interested in only one or a few families, it is not necessary to put all groups in ignore. Rather,
    it is more efficient to call the individual functions that search within each family. For instance, if we are only
    interested in Chevalley A groups, we would call

        >>> os.candidates_CA([4, 2, 0, 2, 0, 0, 1])
        ['CA-2-2_1', 'CA-1-2_3', 'CA-1-7_1', 'CA-1-17_1']

    The only drawback is that these functions do not check for duplicates. Note that ``CA-2-2_1`` and ``CA-1-7_1``
    are isomorphic. So we should use the function :py:func:`FiSGO.OrderSearch.clear_duplicates` to handle duplicates!

        >>> os.candidates_CA([4, 2, 0, 2, 0, 0, 1])
        ['CA-2-2_1', 'CA-1-2_3', 'CA-1-7_1', 'CA-1-17_1']
        >>> os.clear_duplicates(['CA-2-2_1', 'CA-1-2_3', 'CA-1-7_1', 'CA-1-17_1'],True)
        ['CA-2-2_1', 'CA-1-2_3', 'CA-1-17_1']

    There are specific candidate search functions for all families, and they all are of the form ``candidates_[ID]``
    where ``[ID]`` corresponds to the simple group family ID.

Finally, it is convenient to bring attention to the function :py:func:`FiSGO.OrderSearch.check_candidate`, which allows
us to check if a specific group satisfies a given bound. For example:

>>> os.check_candidate("SP-M11", [4, 2, 0, 2, 0, 0, 1])
False

Indeed, the Mathieu 11 sporadic group was not a candidate for this bound.

.. _5. Group Databases:

==========================
4. Simple Group Databases
==========================

A main feature of FiSGO is the implementation of three databases containing information on simple groups and their
projective irreducible representations. These databases are

    - Database of sporadic groups.
    - Hiss-Malle table of irreducible representations of quasisimple groups up to degree 250 in any characteristic.
    - Professor Frank Lübeck's data on projective irreducible representations of Lie type groups up to rank 8 with
      non-exceptional Schur coverings.

Each of these databases is used in many methods already presented in `Section 2 <2. Simple group classes>`_, such as
:py:meth:`SimpleGroup.hiss_malle_pirreps` or :py:meth:`SimpleGroup.lubeck_pirreps`, and for most class properties of
the sporadic groups.

All these databases are stored as JSON files, and are packaged into FiSGO as compressed BZip2 files with maximum
compression. A completely detailed description of the JSON files, its fields and overall contents can be found in
the `FiSGO/PrecomputedData <https://github.com/GeraGC/FiSGO/tree/master/FiSGO/PrecomputedData>`_ directory README in
GitHub or in the documentation :doc:`PrecomputedData`.

In the sequel, we describe each database, how to access it through Python and some relevant auxiliary functions
provided in FiSGO.

---------------------
4.1. Sporadic groups
---------------------

We start with the sporadic groups database. All available data, alongside its relevant field is described in the
following table:

=============   ===========================================================
field           Description
=============   ===========================================================
"code"          FiSGO’s simple group code.
"id"            FiSGO’s simple group code.
"order"         Order of the group.
"latex_name"    List of possible notations for the group in LaTeX.
"multiplier"    Schur multiplier of the group.
"pirreps"       Array of JSON objects, each of which contains the data on
                the irreducible representations of a cover of the sporadic
                group.
=============   ===========================================================

The "pirreps" field contains objects with two fields called "name" and "degrees" where:

    - "name": A possible notation for the cover in LaTeX.
    - "degrees": Degrees of the irreducible representations. Given as a list of pairs,
      each pair contains the degree of an irreducible representation and the number of
      distinct irreducible representations of that degree.

We can access all of this data directly using the :py:func:`FiSGO.SimpleGroups.sporadic_groups_data`. This function
returns a list of Python dictionaries whose keys are the above fields of the JSON file. Let us see an example:

>>> import FiSGO.SimpleGroups as sg
>>> data = sg.sporadic_groups_data()
>>> data[0]["code"]
'SP-M11'
>>> data[10]["id"], data[10]["order"]
('Co2', [18, 6, 3, 1, 1, 0, 0, 0, 1])

.. tip::
    Group orders are given in terms of their prime factors, the corresponding integer can be easily reconstructed
    using the :py:func:`FiSGO.PrimesHandler.prime_reconstructor` function as follows:

        >>> ph.prime_reconstructor(data[10]["order"], 1)
        42305421312000


As we see, different elements of the list correspond to different groups, there are 26 in total. Let us see
some examples of the field "pirreps":

>>> data[0]["code"], data[0]["pirreps"] # Has trivial Schur multiplier
('SP-M11', [{'name': 'M11', 'degrees': [[1, 1], [10, 3], [11, 1], [16, 2], [44, 1], [45, 1], [55, 1]]}])
>>> data[6]["code"], data[6]["multiplier"]
('SP-J2', 2)
>>> data[6]["pirreps"][0] # Reduced output
{'name': 'J2', 'degrees': [[1, 1], [14, 2], [21, 2], [36, 1],..., [300, 1], [336, 1]]}
>>> data[6]["pirreps"][1] # Reduced output
{'name': '2.J2', 'degrees': [[6, 2], [14, 1], [50, 2], [56, 2],..., [350, 1], [448, 1]]}

As we can see, ``data[i]["pirreps"]`` returns a list containing the irreducible representations of both the group
and its coverings. This consists of all projective representations of the group. All this data is taken from GAP.

Since the data is not indexed in any particular order, it can be difficult to access and browse particular information
directly from the output of :py:func:`FiSGO.SimpleGroups.sporadic_groups_data`. Thus, we provide a helper function that
allows to search for specific fields. This is :py:func:`FiSGO.SimpleGroups.sporadic_lookup_property`.

Let us give some examples, first, we fetch the order of the Mathieu 12 group:
>>> import FiSGO.SimpleGroups as sg
>>> sg.sporadic_lookup_property("code", "SP-M12", "order")
[6, 3, 1, 0, 1]

Next, we may want to know some possible LaTeX notations for the Held group:

>>> sg.sporadic_lookup_property("id", "He", "latex_name")
['{\\rm He}', '{\\rm HHM}', '{\\rm HTH}', 'F_7']

We could also ask wether there is a group of order [6,3,2,1] or [7,3,2,1]:

>>> sg.sporadic_lookup_property("order", [6,3,2,1], "code")
None
>>> sg.sporadic_lookup_property("order", [7,3,2,1], "code")
'SP-J2'

.. warning::
    This function always returns a single match, but there could be more! It is specially intended to match codes
    to group properties. See for example:

        >>> sg.sporadic_lookup_property("multiplier", 2, "code")
        'SP-M12'
        >>> sg.sporadic_lookup_property("id", "J2", "multiplier")
        2

    Thus, it should not be used in such a way. We will eventually make it so it is possible. For now, however, the
    interested user may modify it themselves...

.. _4.2.Hiss_Malle_Data:

--------------------
4.2. Hiss and Malle
--------------------

We move on to the Hiss-Malle database. We briefly describe what this database is and its contents, then we
will proceed to showcase the fields and some examples.

In 2001, Hiss and Malle [HM01]_ published a table containing all absolutely
irreducible representations of quasi-simple groups of dimension at most
250, excluding those of groups of Lie type in their defining
characteristic. See [[HM01]_, Theorem 1.1] for the technical details. In 2002, a corrigendum [HM02]_
was published completing the list. These tables have been completed with **most** deliberate omissions and processed
into the database included in FiSGO.

All the details regarding the obtention and processing of this data may (and should) be consulted
in its documentation page :doc:`HissMalleTableFormats` and in :doc:`PrecomputedData`.

All available data, alongside its relevant field is described in the
following table:

=============   ===============================================================
field           Description
=============   ===============================================================
"degree":       Degree of the representation.
"name":         Name of the quasi-simple group in LaTeX.
"field":        Irrationalities of the Brauer characters.
"ind":          Frobenius-Schur indicators. See [[HM01], §5].
"char":         Field characteristics where the representation is defined.
"not_char":     Field characteristics where the representation is **NOT** defined.
"code":         FiSGO’s simple group code of :math:`G/Z(G)`.
=============   ===============================================================

In a similar fashion as in the sporadic group case, we can access the database using the function
:py:func:`FiSGO.SimpleGroups.hiss_malle_data`. This function returns a list of dictionaries, each containing
keys corresponding to the above fields.

>>> hm_data = sg.hiss_malle_data()
>>> hm_data[0]['code'], hm_data[0]['char'], hm_data[0]['not_char'], hm_data[0]['degree']

We see that the first entry in the list contains a representation of the alternating group on 6 letters. It corresponds
to a degree 3 representation in characteristics 2 and 0, with no other characteristic restrictions.

>>> hm_data[100]['code'], hm_data[100]['char'], hm_data[100]['not_char'], hm_data[100]['degree']

We see that the 101st entry in the list contains a representation of the Steinberg :math:`{}^2A_{2}(4^2)` group.
It corresponds to a degree 13 representation in all characteristics except for 2 and 5.

Again, since the data is not indexed in any particular order, it can be difficult to access and browse particular information
directly from the output of :py:func:`FiSGO.SimpleGroups.hiss_malle_data`. Thus, we provide a helper function that
allows to search for specific fields. This is :py:func:`FiSGO.SimpleGroups.hiss_malle_lookup`.

In this case, this function is more versatile than :py:func:`FiSGO.SimpleGroups.sporadic_lookup_property`, as it matches
multiple fields simultaneously and returns all found matches. Let us see some examples:

>>> sg.hiss_malle_lookup({"code":"CA-2-2_3"}, ["degree", "name"])
[{'degree': 71, 'name': '{\\rm PSL}_{3}(8)'},
 {'degree': 72, 'name': '{\\rm PSL}_{3}(8)'},
 {'degree': 73, 'name': '{\\rm PSL}_{3}(8)'}]

The previous instruction has requested for all entries with code ``"CA-2-2_3"`` to return its "degree" and "name" fields

.. warning::
    The codes found in the database are all **normalized**, so the lookup function won't match properly if the
    provided code is of simple syntax:

        >>> sg.hiss_malle_lookup({"code":"CA-2-8"}, ["degree", "name"])
        []

We can try to match multiple fields:

>>> sg.hiss_malle_lookup({"code":"CA-2-2_3", "ind":0}, ["degree", "name"])
[{'degree': 73, 'name': '{\\rm PSL}_{3}(8)'}]

One of the limitations of this search method is the characteristic. Through this function, it is not easy to, for
instance, to request all characteristic 13 representations of degree 73. For this, we provide a more specific function,
which is part of the projective representation search module py:mod:`PIrrepsSearch`. This is py:func:`hiss_malle_range`.

The function py:func:`hiss_malle_range` allows to search for projective representations in a given degree range.
We can also specify the characteristic through the ``char`` keyword argument. Let us see an example:

>>> import FiSGO.PIrrepsSearch as pis
>>> pis.hiss_malle_range([73,73])
[(73, 'AA-74'), (73, 'CA-1-73_1'), (73, 'CA-2-2_3'), (73, 'SA-2-3_2')]

By default, this search is done in characteristic 0. We can specify the characteristic as follows:

>>> pis.hiss_malle_range([73,73], char=13)
[(73, 'AA-74'), (73, 'CA-1-73_1'), (73, 'CA-2-2_3'), (73, 'SA-2-3_2')]
>>> pis.hiss_malle_range([73,73], char=7)
[(73, 'AA-74'), (73, 'CA-1-73_1'), (73, 'SA-2-3_2')]

.. note::
    This function cleans duplicates by default, as it returns projective representations. It is possible for a group
    to have two projective representations of the same degree :math:`d` given by two different coverings. This
    behaviour may be changes adding ``allow_duplicates=True`` as a keyword argument.

.. tip::
    Should one need only information about a specific group, one should use the :py:meth:`SimpleGroup.hiss_malle_pirreps`
    method of the corresponding group object:

        >>> sg.simple_group("CA-2-2_3").hiss_malle_pirreps(char=13)
        [72, 73]

    See :py:meth:`SimpleGroup.hiss_malle_pirreps` for the complete documentation of this method.


.. _4.3.Lubeck_data:

----------------------------
4.3. Lübeck's Lie type data
----------------------------

We move on to describe Lübeck's database on the character degrees and multiplicities of the standard coverings of
the Lie type groups up to rank 8. This data can be found in
`Lübeck's website <https://www.math.rwth-aachen.de/~Frank.Luebeck/chev/DegMult/index.html?LANG=en>`_
from where it has been extracted and processed. Note that his website contains much more information than what we
provide in this module. In his notation, we are interested in the simply connected groups.

Similar to the previous databases, we can access the data using the function
:py:func:`FiSGO.SimpleGroups.lubeck_data`. This function returns a list of dictionaries when given a group ID of a Lie
type group.

As you can see, we have yet to go into detail on the keys and ths structure of the database, which is given in the form
of many compressed JSON files. This is due to the following warning.

.. warning::
    The direct access and usage of the data provided by :py:func:`FiSGO.SimpleGroups.lubeck_data` is discouraged.
    This is partly due to the way the data is presented, and the difficulty in handling exceptions in the data.

    Lübeck's original data consists of a list of polynomials in the parameter :math:`q`. To avoid security issues and
    improve efficiency, these polynomials have been stored in a particular way, and FiSGO has internal functions to
    properly handle their evaluation in the various cases that arise.

    Should a user be interested in actually using the data provided by the function, all information on the data
    structure, how to read it, and the polynomial encoding, may be found in :doc:`PrecomutedData`.

Instead, we provide two alternative ways of accessing the data in an already readable state. One of them has already
been showcased in `Section 2 <2. Simple group classes>`_. That is, for any simple group of Lie type of rank at most 8,
we can compute the irreducible representations of its Schur covering as follows:

>>> group = sg.simple_group("CA-3-5")
>>> group.lubeck_pirreps() # Output shortened!
[[155, 1], [156, 3], [248, 2], [403, 2], [496, 2], [650, 1],..., [24180, 3]]

.. note::
    This is equivalent to computing the degrees of projective representations of Lie type groups of rank at most 8.
    The multiplicity still corresponds to that of the linear irreducible characters of the Schur covering.

This method is convenient when we want the information for a single group. If one needs information on multiple groups
at the same time, one should use :py:func:`FiSGO.PIrrepsSearch.lubeck_bulk_get`. Given a group ID and a list of group
objects or codes with such ID, returns a tuple containing a dictionary pairing each group with a list of degree and
multiplicity pairs, and a list of all groups whose data is unavailable.

>>> pis.lubeck_bulk_get("CA", ["CA-2-3", "CA-9-2"])
({'CA-2-3_1': [[12, 1], [13, 1], [16, 4], [26, 3], [27, 1], [39, 1]]}, ['CA-9-2_1'])

And an example using group objects:

>>> groups = [sg.simple_group(code) for code in ["CA-2-3", "CA-9-2"]]
>>> pis.lubeck_bulk_get("CA", groups)
({simple_group(CA-2-3_1): [[12, 1], [13, 1], [16, 4], [26, 3], [27, 1], [39, 1]]}, [simple_group(CA-9-2_1)])


.. _6. Searching:

============================================
5. Searching for projective representations
============================================

We finish this tutorial diving into the remaining module :py:mod:`FiSGO.PIrrepsSearch`. This module is devoted
to searching through all databases and use the :py:mod:`FiSGO.OrderSearch` and :py:mod:`FiSGO.SimpleGroups` modules
to determine all simple groups with characteristic zero irreducible projective representations in a given dimension
range.

The main function of this module is :py:func:`FiSGO.PIrrepsSearch.pirreps_search`. Before going through some examples,
it is important to know what the function is doing and what steps it takes to reach the result.

The function :py:func:`FiSGO.PIrrepsSearch.pirreps_search` **attempts** to determine all simple groups with characteristic
zero irreducible projective representations in a given dimension range. An attempt results in three lists. The first one
is a list of found representations within the range. The two remaining lists have to do with how successful the attempt
was. To understand their meaning, let us go through the steps :py:func:`FiSGO.PIrrepsSearch.pirreps_search` is taking:

    - Input: Dimension range :math:`[n,m) \cap \mathbb{N}`

    #. Check if the range is contained in the Hiss-Malle database. If not, we take all representations satisfying the
       degree condition and continue with :math:`[\max(n, 251), m)` as the new range. This yields partial data.
    #. Build a bound :math:`M` such that **any** group with
       a projective representation within the range **must** have order dividing :math:`M`.
    #. Use :py:func:`FiSGO.OrderSearch.simple_group_by_order` to find all simple groups satisfying the previous bound.
       Henceforth call them group candidates.
    #. Use the :py:meth:`FiSGO.SimpleGroups.SimpleGroup.smallest_pirrep_degree` method on all group candidates to discard those whose
       smallest projective representation exceeds the dimensional bound :math:`m`.
    #. All smallest representations that belong to the range are stored as partial data.
    #. Check all sporadic group candidates against the sporadic group database. This yields complete data.
    #. Check all Lie groups of rank at most 8 against Lübeck's data. This yields complete data.
    #. Return all found representations, the list of candidates with complete data, and the list of candidates with
       partial data.

Note we have partitioned the groups into two:

    Partial data:
        The candidate may or may not have a representation in the range. If it does, we cannot assure these are all.
        If it doesn't, we cannot assure there are none.
    Complete data:
        All representations within the range are accounted for, all data for such group is available in the given range.

.. note::
    Bound :math:`M` is built using :py:func:`FiSGO.PIrrepsSearch.build_bounds`. The bounds used are detailed in the
    documentation of :py:func:`FiSGO.PIrrepsSearch.build_single_bound`.

As an example, we may search for all groups with projective representations in the range :math:`[12,15]`.

>>> pis.pirreps_search([12,16])  # Reduced output
([(12, 'AA-13'), (12, 'AA-6'),..., (15, 'SA-3-3_1')], ['AA-14',..., 'CA-1-2_4'], [])

As we can see, in this range, all groups are found to be complete data, as we are using the Hiss-Malle database.

Let us briefly now look into the keyword arguments we can pass to the function:

    - ``use_absolute_bound``: If True, it will use Collins' absolute bound, see
      :py:func:`FiSGO.PIrrepsSearch.build_absolute_bound`.
    - ``include_origin``: If True, each representation will display the database/method from which it was sourced.
    - ``ignore``: List of group ID's passed to :py:func:`FiSGO.OrderSearch.simple_group_by_order`. It has already
      been discussed in `Section 3 <4. Origin>`_.

.. warning::
    The ``ignore`` argument is ignored on ranges within the Hiss-Malle data.

.. warning::
    At the time of writing this tutorial (03/01/2026), no functions are implemented to deal with the projective
    irreducible representations of the alternating groups. Thus, for searches outside of the Hiss-Malle range,
    it is recommended to always ignore the alternating groups, i.e. add ``ignore=["AA"]`` as an argument.

As a final example:

>>> pis.pirreps_search([251,252], ignore=["AA"], use_absolute_bound=True, include_origin=True) # Reduced output
([(251, 'CA-1-503_1', 'Smallest pirrep'), (251, 'CA-1-251_1', 'Lübeck'), (251, 'CA-1-503_1', 'Lübeck')],
['SZ-2',...,'G2-5_1'],
['CA-2-2_1',..., 'TT'])

.. note::
    The output of this function may not be the same if the tutorial has not been updated but refinements have been
    made to :py:func:`FiSGO.PIrrepsSearch.pirreps_search`.



===========
References
===========

.. [HM01] Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of
    Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4,
    22–63. |DOI:10.1112/s1461157000000796|

.. [HM02] Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional
    Representations of Quasi-simple Groups. LMS Journal of Computation and
    Mathematics, 5, 95–126. |DOI:10.1112/s1461157000000711|

.. |DOI:10.1112/s1461157000000796| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000796.svg
   :target: https://doi.org/10.1112/s1461157000000796
.. |DOI:10.1112/s1461157000000711| image:: https://zenodo.org/badge/DOI/10.1112/s1461157000000711.svg
   :target: https://doi.org/10.1112/s1461157000000711



.. |FiSGO.SimpleGroups| replace:: :doc:`FiSGO.SimpleGroups <_autosummary/FiSGO.SimpleGroups>`
.. |FiSGO.SimpleGroups.SimpleGroup| replace:: :doc:`FiSGO.SimpleGroups.SimpleGroup <_autosummary/FiSGO.SimpleGroups.SimpleGroup>`