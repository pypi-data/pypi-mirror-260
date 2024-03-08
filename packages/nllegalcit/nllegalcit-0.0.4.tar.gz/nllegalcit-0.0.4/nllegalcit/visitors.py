"""
    nllegalcit/visitors.py

    Copyright 2023-2024, Martijn Staal <nllegalcit [at] martijn-staal.nl>

    Available under the EUPL-1.2, or, at your option, any later version.

    SPDX-License-Identifier: EUPL-1.2
"""

import re
from typing import Optional

from lark import Visitor, ParseTree, Token, Tree

from .citations import Citation, HandelingCitation, KamerstukCitation, CaseLawCitation, EcliCitation, LjnCitation
from .errors import CitationParseException
from .utils import normalize_nl_ecli_court, lark_tree_to_str

re_whitespace: re.Pattern = re.compile(r"\s+")
re_dossiernummer_separator: re.Pattern = re.compile(r"[-.\s]+")
re_replacement_toevoeging_separator: re.Pattern = re.compile(r"[.\s-]+")


class CitationVisitor(Visitor):
    """Generic visitor to create Citation objects for a ParseTree"""

    def __init__(self):
        super().__init__()

        self.citations: list[Citation] = []

    def handeling(self, tree: ParseTree):
        """Create a HandelingCitation from a handeling ParseTree rule"""
        v = HandelingCitationVisitor()
        print(tree.pretty())
        v.visit(tree)
        v.citation.matched_text = lark_tree_to_str(tree)
        self.citations.append(v.citation)

    def kamerstuk(self, tree: ParseTree):
        """Create a KamerstukCitation from a kamerstuk ParseTree rule"""
        v = KamerstukCitationVisitor()
        v.visit(tree)
        v.citation.matched_text = lark_tree_to_str(tree)
        self.citations.append(v.citation)

    def case_law(self, tree: ParseTree):
        """Create a CaseLawCitation from a case_law parse rule"""
        v = CaseLawCitationVisitor()
        v.visit(tree)
        if v.citation is not None:
            v.citation.matched_text = lark_tree_to_str(tree)
            self.citations.append(v.citation)


class CaseLawCitationVisitor(Visitor):
    """Visitor class to create a CaseLawCitation from the parse tree"""

    # pylint: disable=missing-function-docstring

    citation: Optional[CaseLawCitation]

    def __init__(self):
        super().__init__()

        self.citation = None

    def caselaw__nl_ecli(self, tree: ParseTree):
        cit = EcliCitation("NL", "?", -1, "?")

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "caselaw__ECLI_YEAR":
                    cit.year = int(child)
                elif child.type == "caselaw__NL_ECLI_COURT":
                    # TODO: Implement court name normalization
                    cit.court = normalize_nl_ecli_court(str(child))
                elif child.type == "caselaw__NL_ECLI_CASENUMBER":
                    cit.casenumber = str(child)

        self.citation = cit

    def caselaw__eu_ecli(self, tree: ParseTree):
        year: int
        court: str
        casenumber: str

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "caselaw__ECLI_YEAR":
                    year = int(child)
                elif child.type == "caselaw__EU_ECLI_COURT":
                    court = str(child)
                elif child.type == "caselaw__EU_ECLI_CASENUMBER":
                    casenumber = str(child)

        self.citation = EcliCitation("EU", court, year, casenumber)

    def caselaw__ce_ecli(self, tree: ParseTree):
        year: int
        court: str
        casenumber: str

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "caselaw__ECLI_YEAR":
                    year = int(child)
                elif child.type == "caselaw__CE_ECLI_COURT":
                    court = str(child)
                elif child.type == "caselaw__CE_ECLI_CASENUMBER":
                    casenumber = str(child)

        self.citation = EcliCitation("CE", court, year, casenumber)

    def caselaw__other_ecli(self, tree: ParseTree):
        year: int
        country: str
        court: str
        casenumber: str

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "caselaw__ECLI_YEAR":
                    year = int(child)
                elif child.type == "caselaw__OTHER_ECLI_COUNTRY_CODE":
                    country = str(child)
                elif child.type == "caselaw__OTHER_ECLI_COURT":
                    court = str(child)
                elif child.type == "caselaw__OTHER_ECLI_CASENUMBER":
                    casenumber = str(child)

        self.citation = EcliCitation(country, court, year, casenumber)

    def caselaw__ljn(self, tree: ParseTree):
        code: str

        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "caselaw__LJN_CONTENT":
                    code = re_whitespace.sub("", str(child).upper())

        self.citation = LjnCitation(code)


# Shared functions for parlementair visitors
def shared_visitor_kamer(tree: ParseTree) -> str:
    """Shared visitor function for parlementair__kamer"""
    kamer_token = tree.children[0]
    kamer = "?"
    if isinstance(kamer_token, Token):
        if kamer_token.type == "parlementair__TK":
            kamer = "II"
        elif kamer_token.type == "parlementair__EK":
            kamer = "I"
        elif kamer_token.type == "parlementair__VV":
            kamer = "VV"
        else:
            raise CitationParseException("Invalid Kamer in citation")
    else:
        raise CitationParseException("Invalid Kamer in citation")

    return kamer


def shared_visitor_vergaderjaar(tree: ParseTree) -> str:
    """Shared visitor function for parlementair__vergaderjaar"""
    first_year = None
    second_year = None

    for c in tree.children:
        if isinstance(c, Token):
            if first_year is None and c.type == "parlementair__JAAR4":
                first_year = str(c)
            elif c.type == "parlementair__JAAR4":
                second_year = str(c)
            elif c.type == "parlementair__JAAR2":
                if first_year == "1999":
                    second_year = "2000"
                elif first_year == "1899":
                    second_year = "1900"
                else:
                    if first_year is not None:
                        second_year = f"{first_year[0:2]}{str(c)}"
                    else:
                        raise CitationParseException("First year is none")

    return f"{first_year}-{second_year}"


def shared_visitor_paginaverwijzing(tree: ParseTree) -> str:
    """Shared visitor function for parlementair__paginaverwijzing"""
    paginaverwijzing = ""
    paginas_los: list[str] = []
    for c in tree.children:
        if isinstance(c, Token):
            if c.type == "parlementair__PAGINA_LOS":
                paginas_los.append(str(c))

    pagina_ranges: list[str] = []
    for c in tree.children:
        if isinstance(c, Tree):
            if c.data == "parlementair__pagina_range":
                start = None
                end = None
                for d in c.children:
                    if isinstance(d, Token):
                        if d.type == "parlementair__PAGINA_START":
                            start = str(d)
                        elif d.type == "parlementair__PAGINA_EIND":
                            end = str(d)
                if end is None:
                    pagina_ranges.append(f"{start}-")
                else:
                    pagina_ranges.append(f"{start}-{end}")
    paginas = paginas_los + pagina_ranges
    if len(paginas) == 1:
        paginaverwijzing = paginas[0]
    else:
        paginaverwijzing = ','.join(paginas)

    return paginaverwijzing

# IDEA/TODO: Maybe make a generalized ParlementairCitationVisitor with this shared code in it?


class HandelingCitationVisitor(Visitor):
    """Visitor class to create a HandelingCitation from the Lark parse tree"""

    # pylint: disable=missing-function-docstring

    def __init__(self) -> None:
        super().__init__()

        self.citation = HandelingCitation("?", "?", -1, -1)

    def parlementair__kamer(self, tree: ParseTree):
        self.citation.kamer = shared_visitor_kamer(tree)  # type: ignore

    def parlementair__vergaderjaar(self, tree: ParseTree):
        self.citation.vergaderjaar = shared_visitor_vergaderjaar(tree)

    def parlementair__handeling_vergaderingnummer(self, tree: ParseTree):
        nummer = str(tree.children[0])

        self.citation.vergaderingnummer = int(nummer)

    def parlementair__handeling_itemnummer(self, tree: ParseTree):
        nummer = str(tree.children[0])

        self.citation.itemnummer = int(nummer)

    def parlementair__paginaverwijzing(self, tree: ParseTree):
        self.citation.paginaverwijzing = shared_visitor_paginaverwijzing(tree)


class KamerstukCitationVisitor(Visitor):
    """Visitor class to create a KamerstukCitation from the Lark parse tree"""

    # pylint: disable=missing-function-docstring

    def __init__(self):
        super().__init__()

        self.citation = KamerstukCitation("?", "?", "?", "?")

    def parlementair__kamer(self, tree: ParseTree):
        self.citation.kamer = shared_visitor_kamer(tree)

    def parlementair__dossiernummer(self, tree: ParseTree):
        dossiernummer = "?"
        dossiernummer_toevoeging: Optional[str] = None
        for c in tree.children:
            if isinstance(c, Token):
                if c.type == "parlementair__DOSSIERNUMMER":
                    dossiernummer = re_dossiernummer_separator.sub("", c)
                elif c.type == "parlementair__DOSSIERNUMMER_TOEVOEGING":
                    dossiernummer_toevoeging = re_replacement_toevoeging_separator.sub("", c).replace("hoofdstuk", "")

        if dossiernummer_toevoeging is None:
            self.citation.dossiernummer = str(dossiernummer)
        else:
            self.citation.dossiernummer = f"{dossiernummer}-{dossiernummer_toevoeging}"

    def parlementair__vergaderjaar(self, tree: ParseTree):
        self.citation.vergaderjaar = shared_visitor_vergaderjaar(tree)

    def parlementair__ondernummer(self, tree: ParseTree):
        self.citation.ondernummer = str(tree.children[0])

    def parlementair__paginaverwijzing(self, tree: ParseTree):
        self.citation.paginaverwijzing = shared_visitor_paginaverwijzing(tree)


class CitationVisitorOnlyKamerstukCitations(Visitor):
    """Generic visitor to create Citation objects for a ParseTree"""

    def __init__(self):
        super().__init__()

        self.citations: list[KamerstukCitation] = []

    def kamerstuk(self, tree: ParseTree):
        """Create a KamerstukCitation from a kamerstuk ParseTree rule"""
        v = KamerstukCitationVisitor()
        v.visit(tree)
        v.citation.matched_text = lark_tree_to_str(tree)
        self.citations.append(v.citation)
