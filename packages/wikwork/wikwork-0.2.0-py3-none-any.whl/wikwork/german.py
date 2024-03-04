#    GermanWord subclass and related functions.
#    Copyright (C) 2024 Ray Griner (rgriner_fwd@outlook.com)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

""" GermanWord subclass and related functions. """

#------------------------------------------------------------------------------
# File:    german.py
# Author:  Ray Griner
# Date:    2024-03-03
# Changes:
#------------------------------------------------------------------------------
__author__ = 'Ray Griner'
#__all__ = ['AudioFile','Headword']

# Standard modules
import re
import logging
#import collections
from typing import Optional
from wikwork import page_media
from wikwork import io_options as io_opts

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------
# Type aliases
#------------------------------------------------------------------------------
#HttpHeaders = Dict[str, str]
#MediaList = Any
#AudioReqs = Dict[str, Tuple[int, str]]
#SortKey = Callable[['AudioFile'], Any]

#------------------------------------------------------------------------------
# Class definition: GermanWord
#------------------------------------------------------------------------------
class GermanEntry():
    """German Wiktionary™ entry with selected attributes parsed from wikitext.

    Selected elements of the dictionary entries (for the same language as
    the Wiktionary) parsed from the wikitext. A given headword / page can
    have more than one entry (a third-level heading starts a new entry).
    The wikitext appears to be well-organized for implementing a simple
    parser. In the wikitext, templates are used to delimit elements of
    the definition, and these templates appear to almost always occur
    on a single line. Similarly, templates contain key verb conjugation
    and noun or adjective declension information, and these also appear
    to be almost always on a single line. Therefore, when parsing the file,
    it is assumed that tags always occur on a single line.

    The attributes attracted from the noun, verb, and adjective templates
    start with 'adj_', 'verb_', and 'noun_', respectively, and are
    a single string and likely do not contain wikitext. Other attributes
    were formed by concatenating one or more lines after the identifying
    template in the wikitext file (converting newlines to a '; '
    delimiter). These attributes still do contain wikitext, although it
    may be replaced in the future.

    Attributes
    ----------
    word_separation: str
        Lines after '{{Worttrennung}}' template.
    pronunciations: str
        Lines after '{{Aussprache}}' template.
    definitions: str
        Lines after '{{Bedeutungen}}' template.
    origin: str
        Lines after '{{Herkunft}}' template.
    synonyms: str
        Lines after '{{Synonyme}}' or '{{Sinnverwandte Wörter}} template.
    opposites: str
        Lines after '{{Gegenwörter}}' template.
    hyponyms: str
        Hyponyms are more specific words. For example, for
        headword='Jahreszeit' (season), a hyponym is 'Winter' (winter).
        Lines after '{{Unterbegriffe}}' template.
    hypernyms: str
        Hypernyms are more general words. For example, for
        headword='Winter' (winter), a hypernym is 'Jahreszeit' (season).
        Lines after '{{Oberbegriffe}} template.
    examples: str
        Lines after '{{Beispiele}}' template.
    expressions: str
        Lines after '{{Redewengungen}}' template.
    word_combos: str
        Characteristic word combinations. Lines after
        '{{Charakteristische Wortkombinationen}}' template.
    word_formations: str
        Lines after '{{Wortbildungen}}' template.
    refs_and_more_info: str
        References and additional information. Lines after '{{Referenzen}}'
        template.
    sources: str
        Lines after '{{Quellen}}' template.
    abbreviations: str
        Lines after '{{Abkürzungen}}' template.
    alternate_spellings: str
        Lines after '{{Alternative Schreibweisen}}' template.
    sayings: str
        Sayings / proverbs. Lines after '{{Sprichwörter}}' template.
    adj_comp: str
        Comparative form of adjective. 'Komparativ' parameter of
        '{{{Deutsch Adjektiv Übersicht}}' template.
    adj_comp2: str
        Alternate comparative form of adjective. 'Komparativ*' parameter of
        '{{{Deutsch Adjektiv Übersicht}}' template.
    adj_super: str
        Superlative form of adjective. 'Superlative' parameter of
        '{{{Deutsch Adjektiv Übersicht}}' template, with 'am ' prepended
        (unless 'am' parameter of template is '0' or 'nein' to indicate
        'am' should be omitted or the superlative is '-' or '—').
    adj_super2: str
        Alternate superlative form of adjective. 'Superlative*' parameter
        of '{{{Deutsch Adjektiv Übersicht}}' template, with 'am ' prepended
        (unless 'am' parameter of template is '0' or 'nein' to indicate
        'am' should be omitted or the superlative is '-' or '—').
    verb_present_1s: str
        First person singular present tense. 'Präsens_ich' parameter of
        '{{{Deutsch Verb Übersicht}}' template.
    verb_present_2s: str
        Second person singular present tense. 'Präsens_du' parameter of
        '{{{Deutsch Verb Übersicht}}' template.
    verb_present_3s: str
        Third person singular present tense. 'Präsens_er, sie, es'
        parameter of '{{{Deutsch Verb Übersicht}}' template.
    verb_pret_1s: str
        First or third person simple past (preterite). 'Präteritum_ich'
        parameter of '{{{Deutsch Verb Übersicht}}' template.
    verb_subj_ii: str
        First person conditional subjunctive (Konjunktiv II).
        'Konjunktiv II_ich' parameter of '{{{Deutsch Verb Übersicht}}'
        template.
    verb_imper_s: str
        First person imperative singular. 'Imperativ Singular' parameter of
        '{{{Deutsch Verb Übersicht}}' template.
    verb_imper_p: str
        First person imperative plural. 'Imperativ Plural' parameter of
        '{{{Deutsch Verb Übersicht}}' template.
    verb_past_part: str
        Past participle. 'Partizip II' parameter of
        '{{{Deutsch Verb Übersicht}}' template.
    verb_helper: str
        Helper verb (for past participle). 'Hilfsverb' parameter of
        '{{{Deutsch Verb Übersicht}}' template.
    noun_gender: str
        Noun gender. 'Genus' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. For now, left blank
        if noun has more than one gender, but may be populated in the
        future. See:
        https://de.wiktionary.org/wiki/Vorlage:Deutsch_Substantiv_%C3%9Cbersicht
        for details.
    noun_nom_p: str
        Noun nominative plural. 'Nominativ Plural' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. For now, left blank
        if noun has more than one plural form, but may be populated in the
        future. See template page linked in `noun_gender` parameter for
        details.
    noun_gen_s: str
        Noun genitive singular. 'Genitiv Singular' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. For now, left blank
        if noun has more than one genitive singular, but may be populated
        in the future. See template page linked in `noun_gender` parameter for
        details.
    noun_adj_decl: Optional[bool]
        True if line with '{{{Deutsch Substantiv Übersicht}}' template also
        has '{{adjektivische Deklination}}' template. False if the first
        template is present without the second. None if first template is
        not present.
    """
    def __init__(self) -> None:
        """ Initialize entry. Set all contents to empty strings. """
        self.word_separation: str = ''
        self.pronunciations: str = ''
        self.abbreviations: str = ''
        self.definitions: str = ''
        self.origins: str = ''
        self.synonyms: str = ''
        self.opposites: str = ''
        self.hyponyms: str = ''
        self.hypernyms: str = ''
        self.examples: str = ''
        self.expressions: str = ''
        self.word_combos: str = ''
        self.word_formations: str = ''
        self.refs_and_more_info: str = ''
        self.sources: str = ''
        self.alternate_spellings: str = ''
        self.sayings: str = ''

        self.adj_comp: str = ''
        self.adj_comp2: str = ''
        self.adj_super: str = ''
        self.adj_super2: str = ''

        self.verb_present_1s: str=''
        self.verb_present_2s: str=''
        self.verb_present_3s: str=''
        self.verb_pret_1s: str=''
        self.verb_imper_s: str=''
        self.verb_imper_p: str=''
        self.verb_past_part: str=''
        self.verb_helper: str=''
        self.verb_subj_ii: str=''

        self.noun_gender: str=''
        self.noun_nom_p: str=''
        self.noun_gen_s: str=''
        self.noun_adj_decl: Optional[bool]=None

    def __repr__(self) -> str:
        return ('GermanEntry('
            f'word_separation="{self.word_separation}", '
            f'pronunciations="{self.pronunciations}", '
            f'abbreviations="{self.abbreviations}", '
            f'definitions="{self.definitions}", '
            f'origins="{self.origins}", '
            f'synonyms="{self.synonyms}", '
            f'opposites="{self.opposites}", '
            f'hyponyms="{self.hyponyms}", '
            f'examples="{self.examples}", '
            f'expressions="{self.expressions}", '
            f'word_combos="{self.word_combos}", '
            f'word_formations="{self.word_formations}", '
            f'refs_and_more_info="{self.refs_and_more_info}", '
            f'sources="{self.sources}", '
            f'alternate_spellings="{self.alternate_spellings}", '
            f'hypernyms="{self.hypernyms}", '
            f'sayings="{self.sayings}", '
            f'adj_comp="{self.adj_comp}", '
            f'adj_super="{self.adj_super}", '
            f'adj_comp2="{self.adj_comp2}", '
            f'adj_super2="{self.adj_super2}", '
            f'verb_present_1s="{self.verb_present_1s}", '
            f'verb_present_2s="{self.verb_present_2s}", '
            f'verb_present_3s="{self.verb_present_3s}", '
            f'verb_pret_1s="{self.verb_pret_1s}", '
            f'verb_imper_s="{self.verb_imper_s}", '
            f'verb_imper_p="{self.verb_imper_p}", '
            f'verb_past_part="{self.verb_past_part}", '
            f'verb_subj_ii="{self.verb_subj_ii}", '
            f'verb_helper="{self.verb_helper}", '
            f'noun_gender="{self.noun_gender}", '
            f'noun_nom_p="{self.noun_nom_p}", '
            f'noun_gen_s="{self.noun_gen_s}", '
            f'noun_adj_decl={self.noun_adj_decl})')

class GermanWord(page_media.Headword):
    """Headword information and associated audio files for German headword.

    Attributes
    ----------
    entries : list[GermanEntry]
        Information from the entries on the word page that are from the
        same language as `lang_code`. A new entry is defined as the start
        of a new second or third level heading (ie, lines that start with
        '== ' or '=== ').
    """

    def __init__(self, headword: str, lang_code: str):
        """Initialize instance.

        Initialization does not cause information to be fetched from the
        internet or local application cache/output.

        Parameters
        ----------
        headword : str
            The word or phrase for which information will be retrieved.

        lang_code : str
            Language code specifying the language of the Wiktionary™ from
            which data will be retrieved.

        Trademark Notice
        ----------------
        Wiktionary is a trademark of the Wikimedia Foundation and is used
        with the permission of the Wikimedia Foundation. We are not
        endorsed by or affiliated with the Wikimedia Foundation.
        """
        super().__init__(headword=headword, lang_code=lang_code)
        self.entries: list[GermanEntry] = []

    def __repr__(self) -> str:
        return ('GermanWord('
            f'    lang_code="{self.lang_code}",'
            f'    headword="{self.headword}",'
            f'    title_uncoded="{self.title_uncoded}",'
            f'    valid_input={self.valid_input},'
            f'    status_msg="{self.status_msg}",'
            f'    revision={self.revision},'
            f'    html: len({len(self.html)}) str,'
            f'    html_etag="{self.html_etag}",'
            f'    wikitext: len({len(self.wikitext)}) str,'
            f'    desc="{self.desc}",'
            '     audio_files=[' +
            '\n'.join([f'    {af}' for af in self.audio_files]) +
            '], ' +
            '    entries=[' +
            '\n'.join([f'    {entry}' for entry in self.entries]) +
            '])\n')

    #----------------
    # Public methods
    #----------------
    def fetch_word_page(self, io_options: io_opts.IOOptions) -> None:
        """Fetch the HTML and wikitext for the word page.

        That is, if self.headword='still' and the IOOptions.lang_code='en',
        this will retrieve the page: https://en.wiktionary.org/wiki/still

        Parameters
        ----------
        io_options : io_options.IOOptions
            Control parameters for internet requests and local cache/output

        Returns
        -------
        None
        """
        super().fetch_word_page(io_options=io_options)
        _parse_wikitext(self)

#------------------
# Private functions
#------------------
def _write_entry(self: GermanWord, entry_index: int,
                 attr: Optional[str], results: list[str]) -> None:
    if entry_index<0:
        #logger.warning('No entry found for %s', self.headword)
        return
    value = '; '.join(results)
    if attr is not None:
        setattr(self.entries[entry_index], attr, value)

def _one_parameter(self: GermanWord, entry_index: int, attr: str, line: str,
                   param: str) -> None:
    pattern = (r'\|\s*'
               f'{param}'
               r'\s*=(.*?)(\||\}\})')
    regex_match = re.search(pattern, line)
    if regex_match:
        setattr(self.entries[entry_index], attr,
                str.strip(regex_match.group(1)))

def _parse_noun_template(self: GermanWord, line: str,
                         entry_index: int) -> None:
    """Parse line containing noun template and update entry.
    """
    if line.count('{') != 2 or line.count('}') != 2 or line.count ('}}') != 1:
        logging.info(('Word: %s: Noun template incomplete', self.headword))
        return

    _one_parameter(self, entry_index, 'noun_gender', line, 'Genus')
    _one_parameter(self, entry_index, 'noun_nom_p', line, 'Nominativ Plural')
    _one_parameter(self, entry_index, 'noun_gen_s', line, 'Genitiv Singular')
    adj_decl = re.search(r'\{\{adjektivische Deklination\}\}', line)
    if adj_decl:
        self.entries[entry_index].noun_adj_decl = True
    else:
        self.entries[entry_index].noun_adj_decl = False

def _parse_verb_template(self: GermanWord, line: str,
                         entry_index: int) -> None:
    """Parse line containing verb template and update entry.
    """
    if line.count('{') != 2 or line.count('}') != 2 or line.count ('}}') != 1:
        logging.info(('Word: %s: Verb template incomplete', self.headword))
        return

    _one_parameter(self, entry_index, 'verb_present_1s', line, 'Präsens_ich')
    _one_parameter(self, entry_index, 'verb_present_2s', line, 'Präsens_du')
    _one_parameter(self, entry_index, 'verb_present_3s', line,
                   'Präsens_er, sie, es')
    _one_parameter(self, entry_index, 'verb_pret_1s', line, 'Präteritum_ich')
    _one_parameter(self, entry_index, 'verb_subj_ii', line,
                   'Konjunktiv II_ich')
    _one_parameter(self, entry_index, 'verb_imper_s', line,
                   'Imperativ Singular')
    _one_parameter(self, entry_index, 'verb_imper_p', line, 'Imperativ Plural')
    _one_parameter(self, entry_index, 'verb_past_part', line, 'Partizip II')
    _one_parameter(self, entry_index, 'verb_helper', line, 'Hilfsverb')

def _parse_adjective_template(self: GermanWord, line: str,
                              entry_index: int) -> None:
    """Parse line containing adjective template and update entry.
    """
    if line.count('{') != 2 or line.count('}') != 2 or line.count ('}}') != 1:
        logging.info('Word: %s: Adjective template incomplete',
                     self.headword)
        return

    positive = re.search(r'\|\s*Positiv\s*=(.*?)\|', line)
    if positive and str.strip(positive.group(1)) != self.headword:
        logging.info(('Word: %s: Positiv attribute in adjective '
                       'template does not match headword %s'),
                      positive, self.headword)
        return

    # defined in template but seems rare
    am_param = re.search(r'\|\s*am\s*=(.*?)(\||\}\})', line)
    if am_param and str.strip(am_param.group(1)) in ['0','nein']:
        am_str=''
    else:
        am_str='am '

    _one_parameter(self, entry_index, 'adj_comp', line, 'Komparativ')
    _one_parameter(self, entry_index, 'adj_comp2', line, r'Komparativ\*')

    superlative = re.search(r'\|\s*Superlativ\s*=(.*?)(\||\}\})', line)
    if superlative:
        if superlative.group(1) in ['-','—']: am_str = ''
        self.entries[entry_index].adj_super = (
            f'{am_str}{str.strip(superlative.group(1))}')

    superlative2 = re.search(r'\|\s*Superlativ\*\s*=(.*?)(\||\}\})', line)
    if superlative2:
        if superlative2.group(1) in ['-','—']: am_str = ''
        self.entries[entry_index].adj_super2 = (
            f'{am_str}{str.strip(superlative2.group(1))}')

def _parse_wikitext(self: GermanWord) -> None:
    """Parse the wikitext and put results in the entries attribute.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # List of tags and the field the result will be put in
    section_dict = {
        '{{Worttrennung}}' : 'word_separation',
        '{{Aussprache}}' : 'pronunciation',
        '{{Bedeutungen}}' : 'definitions',
        '{{Herkunft}}' : 'origins',
        '{{Sinnverwandte Wörter}}' : 'synonyms',
        # next one is intentionally the same as above
        '{{Synonyme}}' : 'synonyms',
        '{{Gegenwörter}}' : 'opposites',
        '{{Unterbegriffe}}' : 'hyponyms',
        '{{Beispiele}}' : 'examples',
        '{{Redewendungen}}' : 'expressions',
        '{{Charakteristische Wortkombinationen}}' : 'word_combos',
        '{{Wortbildungen}}' : 'word_formations',
        '{{Referenzen}}' : 'refs_and_more_info',
        '{{Quellen}}' : 'sources',
        '{{Abkürzungen}}' : 'abbreviations',
        '{{Alternative Schreibweisen}}' : 'alternate_spellings',
        '{{Oberbegriffe}}' : 'hypernyms',
        '{{Sprichwörter}}' : 'sayings',
    }
    lines = self.wikitext.splitlines()
    h2_german_str: str = r'^== .* \(\{\{Sprache\|Deutsch\}\}\) ==$'
    h2_str: str = r'^== .* ==$'
    h3_german_str: str = r'^=== \{\{Wortart\|.*\|Deutsch\}\}.* ===$'
    h4_str: str = r'^==== .* ====$'

    in_german_sect: bool = False
    german_sect_counter: int = 0
    entry_index: int = -1
    saved_attr_name: Optional[str] = None
    results: list[str] = []
    for line in lines:
        if re.search(h2_german_str, line):
            german_sect_counter += 1
            if in_german_sect:
                _write_entry(self, entry_index, saved_attr_name, results)
            if german_sect_counter>1:
                logger.info('German section %d', german_sect_counter)
                in_german_sect = False
            else:
                in_german_sect = True
        elif re.search(h3_german_str, line):
            _write_entry(self, entry_index, saved_attr_name, results)
            entry_index += 1
            self.entries.append(GermanEntry())
            results = []
            saved_attr_name = None
        elif re.search(h2_str, line) or re.search(h4_str, line):
            in_german_sect = False

        if in_german_sect:
            if line.startswith('{{'):
                # New template, so write contents of results to attribute
                _write_entry(self, entry_index, saved_attr_name, results)
                # Done writing, so process current line
                results = []
                val = section_dict.get(line, None)
                if val is not None:
                    saved_attr_name = val
                else:
                    saved_attr_name = None
                    if line.startswith('{{Ü-Tabelle|'):
                        pass
                    elif line.startswith('{{Ähnlichkeiten '):
                        pass
                    elif line.startswith('{{Deutsch Verb Übersicht|'):
                        _parse_verb_template(self, line, entry_index)
                    elif line.startswith('{{Deutsch Substantiv Übersicht|'):
                        _parse_noun_template(self, line, entry_index)
                    elif line.startswith('{{Deutsch Adjektiv Übersicht|'):
                        _parse_adjective_template(self, line, entry_index)
                    elif line.startswith('{{Deutsch Adverb Übersicht|'):
                        pass
                    elif line.startswith('{{Deutsch Pronomen Übersicht|'):
                        pass
                    elif line.startswith('{{Deutsch Vorname Übersicht '):
                        pass
                    elif line.startswith('{{Deutsch Toponym Übersicht|'):
                        pass
                    elif line.startswith('{{Grundformverweis Dekl|'):
                        pass
                    elif line.startswith('{{Grundformverweis Konj|'):
                        pass
                    elif line.startswith('{{Grundformverweis|'):
                        pass
                    elif line.startswith('{{Pronomina-Tabelle|'):
                        pass
                    elif line.startswith('{{erweitern|'):
                        pass
                    elif line.startswith('{{überarbeiten|'):
                        pass
                    else:
                        pass
                        #logger.info('Word %s: Template not handled: %s',
                        #            self.headword, line)
            else:
                if line: results.append(line)
    if in_german_sect:
        _write_entry(self, entry_index, saved_attr_name, results)

