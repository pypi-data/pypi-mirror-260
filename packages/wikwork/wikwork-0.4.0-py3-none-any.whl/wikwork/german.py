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

""" GermanWord subclass and related functions.

Key objects are the `GermanWord` object, a subclass of `Headword` object that
has an additional attribute called entries, which is a list of `GermanEntry`
objects. A `GermanEntry` object has attributes that contain raw wikitext
or parameter values of parsed templates with most of the information presented
for each dictionary entry.

"""

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
from wikwork import parse
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
    word_separations: str
        Lines after '{{Worttrennung}}' template.
    pronunciations: str
        Lines after '{{Aussprache}}' template.
    definitions: str
        Lines after '{{Bedeutungen}}' template.
    etymology: str
        Lines after '{{Herkunft}}' template.
    synonyms: str
        Lines after '{{Synonyme}}' or '{{Sinnverwandte Wörter}} template.
    antonyms: str
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
    noun_nom_s: str
        Noun nominative singular. 'Nominativ Singular' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. 
        See template page linked
        in `noun_gender` parameter for details.
    noun_nom_p: str
        Noun nominative plural. 'Nominativ Plural' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Blank if the 
        declination has multiple forms and these forms are recorded in the
        template with parameter names: 'Nominative Plural 1',
        'Nominative Plural 2', etc...  This behavior may change in the
        future.
        See template page linked in `noun_gender` parameter for details.
    noun_acc_s: str
        Noun accusative singular. 'Akkusativ Singular' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Alternate forms
        are handled as described for the `noun_nom_p` attribute.
    noun_acc_p: str
        Noun accusative plural. 'Akkusativ Plural' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Alternate forms
        are handled as described for the `noun_nom_p` attribute.
    noun_dat_s: str
        Noun dative singular. 'Dative Singular' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Alternate forms
        are handled as described for the `noun_nom_p` attribute.
    noun_dat_p: str
        Noun dative plural. 'Dative Plural' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Alternate forms
        are handled as described for the `noun_nom_p` attribute.
    noun_gen_s: str
        Noun genitive singular. 'Genitiv Singular' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Alternate forms
        are handled as described for the `noun_nom_p` attribute.
    noun_gen_p: str
        Noun genitive singular. 'Genitiv Plural' parameter of
        '{{{Deutsch Substantiv Übersicht}}' template. Alternate forms
        are handled as described for the `noun_nom_p` attribute.
    noun_adj_decl: bool
        True if line with '{{{Deutsch Substantiv Übersicht}}' template also
        has '{{adjektivische Deklination}}' template. False if the first
        template is present without the second. None if first template is
        not present.
    noun_weak: bool
        None if `noun_nom_s`doesn't match the `headword` of the word the
        entry belongs to or if any of the 7 declinations are missing. True
        if all 7 declinations can be formed by adding '-n' or '-en' to the
        nominative singular. Otherwise, false. Because attributes holding
        the declensions are missing if there is an alternate form, this
        currently fails to flag words that have multiple declensions,
        even if one of the variants is weak.
    """
    def __init__(self) -> None:
        """ Initialize entry. Set all contents to empty strings. """
        self.word_separations: str = ''
        self.pronunciations: str = ''
        self.abbreviations: str = ''
        self.definitions: str = ''
        self.etymology: str = ''
        self.synonyms: str = ''
        self.antonyms: str = ''
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

        self._adj_written: bool=False
        self.adj_comp: str = ''
        self.adj_comp2: str = ''
        self.adj_super: str = ''
        self.adj_super2: str = ''

        self._verb_written: bool=False
        self.verb_present_1s: str=''
        self.verb_present_2s: str=''
        self.verb_present_3s: str=''
        self.verb_pret_1s: str=''
        self.verb_imper_s: str=''
        self.verb_imper_p: str=''
        self.verb_past_part: str=''
        self.verb_helper: str=''
        self.verb_subj_ii: str=''

        self._noun_written: bool=False
        self.noun_gender: str=''
        self.noun_nom_s: str=''
        self.noun_nom_p: str=''
        self.noun_acc_s: str=''
        self.noun_acc_p: str=''
        self.noun_dat_s: str=''
        self.noun_dat_p: str=''
        self.noun_gen_s: str=''
        self.noun_gen_p: str=''
        self.noun_adj_decl: Optional[bool]=None
        self.noun_weak: Optional[bool]=None

    @classmethod
    def build_new(cls) -> 'GermanEntry':
        """ Build new GermanEntry instance """
        return cls()

    def __repr__(self) -> str:
        selfvars = vars(self)
        output_list = []
        for k, v in selfvars.items():
            output_list.append(f'{k}="{v}"')
        return 'GermanEntry(' + ', '.join(output_list) + ')'

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
def _parse_noun_template(self: GermanWord, line: str,
                         entry_index: int) -> None:
    """Parse line containing noun template and update entry.
    """
    wiki_temp, err_msg = parse._parse_one_template(line)
    if wiki_temp is None:
        logger.warning('Word: %s: Template parser: %s',
                        self.headword, err_msg)
        return

    temp_dict = wiki_temp.params
    current_entry = self.entries[entry_index]

    if current_entry._noun_written:
        logger.info('Word %s: Template not handled: already found: %s',
            self.headword, line)
        return
    current_entry._noun_written = True
    current_entry.noun_gender = temp_dict.get('Genus', '')
    current_entry.noun_nom_s = temp_dict.get('Nominativ Singular', '')
    current_entry.noun_nom_p = temp_dict.get('Nominativ Plural', '')
    current_entry.noun_gen_s = temp_dict.get('Genitiv Singular', '')
    current_entry.noun_gen_p = temp_dict.get('Genitiv Plural', '')
    current_entry.noun_dat_s = temp_dict.get('Dativ Singular', '')
    current_entry.noun_dat_p = temp_dict.get('Dativ Plural', '')
    current_entry.noun_acc_s = temp_dict.get('Akkusativ Singular', '')
    current_entry.noun_acc_p = temp_dict.get('Akkusativ Plural', '')

    print(all([bool(str) for str in [current_entry.noun_nom_p,
             current_entry.noun_gen_s, current_entry.noun_gen_p,
             current_entry.noun_dat_s, current_entry.noun_dat_p,
             current_entry.noun_acc_s, current_entry.noun_acc_p]]))
    # Assign `noun_weak` attribute
    if (self.headword == current_entry.noun_nom_s
        and all( [bool(str) for str in [current_entry.noun_nom_p,
             current_entry.noun_gen_s, current_entry.noun_gen_p,
             current_entry.noun_dat_s, current_entry.noun_dat_p,
             current_entry.noun_acc_s, current_entry.noun_acc_p]])):
        current_entry.noun_weak = False
        for suffix in ['n', 'en']:
            if ( (self.headword + suffix == current_entry.noun_nom_p)
                and (self.headword + suffix == current_entry.noun_gen_s)
                and (self.headword + suffix == current_entry.noun_gen_p)
                and (self.headword + suffix == current_entry.noun_dat_s)
                and (self.headword + suffix == current_entry.noun_dat_p)
                and (self.headword + suffix == current_entry.noun_acc_s)
                and (self.headword + suffix == current_entry.noun_acc_p)):
                current_entry.noun_weak = True
                break

def _parse_verb_template(self: GermanWord, line: str,
                         entry_index: int) -> None:
    """Parse line containing verb template and update entry.
    """
    wiki_temp, err_msg = parse._parse_one_template(line)
    if wiki_temp is None:
        logger.warning('Word: %s: Template parser: %s',
                        self.headword, err_msg)
        return
    temp_dict = wiki_temp.params
    current_entry = self.entries[entry_index]

    if current_entry._verb_written:
        logger.info('Word %s: Template not handled: already found: %s',
            self.headword, line)
        return
    current_entry._verb_written = True
    current_entry.verb_present_1s = temp_dict.get('Präsens_ich','')
    current_entry.verb_present_2s = temp_dict.get('Präsens_du','')
    current_entry.verb_present_3s = temp_dict.get('Präsens_er, sie, es','')
    current_entry.verb_pret_1s = temp_dict.get('Präteritum_ich', '')
    current_entry.verb_subj_ii = temp_dict.get('Konjunktiv II_ich','')
    current_entry.verb_imper_s = temp_dict.get('Imperativ Singular','')
    current_entry.verb_imper_p = temp_dict.get('Imperativ Plural','')
    current_entry.verb_past_part = temp_dict.get('Partizip II','')
    current_entry.verb_helper = temp_dict.get('Hilfsverb')

def _parse_adjective_template(self: GermanWord, line: str,
                              entry_index: int) -> None:
    """Parse line containing adjective template and update entry.
    """
    wiki_temp, err_msg = parse._parse_one_template(line)
    if wiki_temp is None:
        logger.warning('Word: %s: Template parser: %s',
                        self.headword, err_msg)
        return
    temp_dict = wiki_temp.params
    current_entry = self.entries[entry_index]

    if 'positive' in temp_dict and temp_dict['positive'] != self.headword:
        logging.info(('Word: %s: Positiv attribute in adjective '
                       'template does not match headword %s'),
                      temp_dict['positive'], self.headword)
        return

    # defined in template but seems rare
    if 'am' in temp_dict and temp_dict['am'] in ['0','nein']:
        am_str=''
    else:
        am_str='am '

    if current_entry._adj_written:
        logger.info('Word %s: Template not handled: already found: %s',
            self.headword, line)
        return

    current_entry._adj_written = True
    current_entry.adj_comp = temp_dict.get('Komparativ')
    current_entry.adj_comp2 = temp_dict.get('Komparativ*')

    sup_val = temp_dict.get('Superlativ', None)
    if sup_val is not None:
        if sup_val in ['-','—']: am_str = ''
        current_entry.adj_super = f'{am_str}{sup_val}'

    sup_val2 = temp_dict.get('Superlativ*', None)
    if sup_val2 is not None:
        current_entry.adj_super2 = f'{am_str}{sup_val2}'

def _parse_wikitext(self: GermanWord) -> None:
    """Parse the wikitext and put results in the entries attribute.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """

    # List of templates and the field the result will be put in
    temp_to_attrib_dict = {
        '{{Worttrennung}}' : 'word_separations',
        '{{Aussprache}}' : 'pronunciations',
        '{{Bedeutungen}}' : 'definitions',
        '{{Herkunft}}' : 'etymology',
        '{{Sinnverwandte Wörter}}' : 'synonyms',
        # next one is intentionally the same as above
        '{{Synonyme}}' : 'synonyms',
        '{{Gegenwörter}}' : 'antonyms',
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
    h2_german_str: str = r'^== .* \(\{\{Sprache\|Deutsch\}\}\) ==$'
    h2_str: str = r'^== .* ==$'
    h3_german_str: str = r'^=== \{\{Wortart\|.*\|Deutsch\}\}.* ===$'
    h4_str: str = r'^==== .* ====$'
    adj_decl_str = (r'^=== \{\{Wortart\|Substantiv\|Deutsch\}\}'
                    r'.*\{\{adjektivische Deklination\}\}')

    def in_target_sect2(line: str) -> bool:
        return bool(re.search(h2_german_str, line))
    def in_target_sect3(line: str) -> bool:
        return bool(re.search(h3_german_str, line))
    def in_sect2(line: str) -> bool:
        return bool(re.search(h2_str, line))
    def in_sect4(line: str) -> bool:
        return bool(re.search(h4_str, line))
    def makes_new_field(line: str) -> bool:
        return bool(line.startswith('{{')
            or re.search(adj_decl_str, line))
    def do_on_each_line(self: GermanWord, entry_index: int, line: str) -> None:
        return
    def ignore_template(line: str) -> bool:
        return bool(re.search((r'\{\{Ü-Tabelle\||'
                     r'\{\{Ähnlichkeiten\||'
                     r'\{\{Deutsch Adverb Übersicht\||'
                     r'\{\{Deutsch Pronomen Übersicht\||'
                     r'\{\{Deutsch Vorname Übersicht |'
                     r'\{\{Deutsch Toponym Übersicht\||'
                     r'\{\{Grundformverweis Dekl\||'
                     r'\{\{Grundformverweis Konj\||'
                     r'\{\{Grundformverweis\||'
                     r'\{\{Pronomina-Tabelle\||'
                     r'\{\{erweitern\||'
                     r'\{\{überarbeiten\|'), line))

    def process_other_templates(self: GermanWord,
                                line: str, entry_index: int) -> bool:
        if line.startswith('{{Deutsch Verb Übersicht|'):
            _parse_verb_template(self, line, entry_index)
            return True
        elif line.startswith('{{Deutsch Substantiv Übersicht|'):
            _parse_noun_template(self, line, entry_index)
            return True
        elif line.startswith('{{Deutsch Adjektiv Übersicht|'):
            _parse_adjective_template(self, line, entry_index)
            return True
        elif re.search(adj_decl_str, line):
            self.entries[entry_index].noun_adj_decl = True
            return True
        else:
            return False

    parse._parse_multi(self, temp_to_attrib_dict=temp_to_attrib_dict,
        in_target_sect2=in_target_sect2,
        in_target_add_entry=in_target_sect3,
        in_sect2=in_sect2, in_sect4=in_sect4,
        makes_new_field=makes_new_field, ignore_template=ignore_template,
        entry_constructor=GermanEntry.build_new,
        allow_data_after_template=False,
        do_on_each_line=do_on_each_line,
        process_other_templates=process_other_templates)

