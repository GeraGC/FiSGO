# Hiss and Malle tables of low-dimensional represenations of quasi-simple groups

**Note:** This folder is not included as part of the Python package.

## Introduction

In 2001, Hiss and Malle [1] published a table containing all absolutely irreducible representations of quasi-simple groups
of dimension at most 250, excluding those of groups of Lie type in their defining characteristic. See [1, Theorem 1.1] for the technical details.

In 2002, a corrigendum [2] was published completing the list.

It is important to note that the table contains deliberate omissions of some representations. These include:
- The $n-1$ or $n-2$-dimensional representations of alternating groups (depending on the characteristic of the base field).
- The representations of PSL$(2,q)$ for $q < 499$.

For more information on the omissions, see [1, Table 2] and [1, $\S$6].

## Contents of the folder
We provide a digitalized version of the table in the following formats:
 - Hiss_Malle_table.tex: LaTeX file containing the table, uses the package `longtables` to break the table into multiple pages.
 - Hiss_Malle_table.csv: CSV file containing the table, the LaTeX `$` symbol have been deleted for easier reading.
 - Hiss_Malle_table.md: Markdown file containing the table.
 - Hiss_Malle_table.txt: Plain text file containing the table in an ASCII table format, the LaTeX `$` symbol have been deleted for easier reading..

For a JSON version of the table, see `PrecomputedData/Hiss_Malle_data.json`. Note that this JSON file contains additional data fields
to those in the files above.

The table has been generated from the corrigendum [2] using the AI tool Mathpix as a base. After the first import, the table has been manually corrected.
In the process, we have also renamed the groups to one of the notations used in FiSGO. See the `SimpleGroups.SimpleGroups.latex_name` method documentation for more details
on the naming conventions used.

## References
**[1]** Hiss, G., & Malle, G. (2001). Low-Dimensional Representations of Quasi-Simple Groups. LMS Journal of Computation and Mathematics, 4, 22–63.
[![DOI:10.1112/s1461157000000796](https://zenodo.org/badge/DOI/10.1112/s1461157000000796.svg)](https://doi.org/10.1112/s1461157000000796)

**[2]** Hiss, G., & Malle, G. (2002). Corrigenda: Low-dimensional Representations of Quasi-simple Groups. LMS Journal of Computation and Mathematics, 5, 95–126.
[![DOI:10.1112/s1461157000000711](https://zenodo.org/badge/DOI/10.1112/s1461157000000711.svg)](https://doi.org/10.1112/s1461157000000711)
