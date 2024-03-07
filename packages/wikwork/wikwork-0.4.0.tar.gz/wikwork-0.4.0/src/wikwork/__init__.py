#   Use REST APIs to get word and audio file info from Wiktionary
#   Copyright (C) 2024 Ray Griner (rgriner_fwd@outlook.com)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

"""Use Wikimedia™ REST APIs to get word and audio file info from Wiktionary™.

TRADEMARK NOTICE
----------------
Wiktionary, Wikimedia, Wikidata, Wikimedia Commons, and MediaWiki are
trademarks of the Wikimedia Foundation and are used with the permission of
the Wikimedia Foundation. We are not endorsed by or affiliated with the
Wikimedia Foundation.

WIKIMEDIA API TERMS AND CONDITIONS
----------------------------------
The REST APIs used are an interface provided by Wikimedia. The version
used is version 1. Global rules, content licensing, and terms of service
set by Wikimedia for using the APIs are currently at:
   https://[xx].wiktionary.org/api/rest_v1, where
[xx] is replaced by the language code of the Wiktionary (eg,
   https://en.wiktionary.org/api/rest_v1 for the English Wiktionary).

FUNCTIONALITY
-------------
This package extracts word and audio file information (but not audio files
themselves) from Wiktionary. Support to download audio may be added in the
future. For german words, the most common elements of the dictionary entry
or entries for a word can be extracted into separate fields. Similar 
functionality may be added in the future for other languages, or users can
write their own parsers on the downloaded objects.

Downloading all audio files for a given headword (ie, page or page title)
technically only requires two REST API calls, one to get the list of audio
files for the headword and then to download the audio file. However, doing
this and nothing else would ignore the downloader's potential attribution
and other responsibilities imposed by the file licenses. Furthermore, the
audio files obtained from the media list API for a given headword should
consist of all audio files from the headword page, including those in
languages other than the one in which the Wiktionary is written.

The package therefore contains the following functionality:

1. Automatic removal of audio files that are likely (based on file naming
convention) not pronunciations in the target language.

2. Creation of a flag to indicate whether the audio file is probably a
pronunciation of the headword and not, say, an example expression (again
based on file naming conventions).

3. Assignment of a probable author and probable license based on parsing
the wikitext of the file that is meant to contain such information using a
regular expressions. Regular expression parsing of such text files may not
be perfect, and therefore users should review the assigned probable
license and probable author with the wikitext to confirm the necessary
information was correctly extracted. A wrapper function is provided to
print the probable license, probable author, and wikitext to a single
file for easier review.

4. Support for user-created functions that assign the probable author and
probable license for users that want to write their own parser or write
a wrapper around a parser from a different third-party package.

5. Sorting of audio files by user-defined keys (which might include sorting
by preferred probable licenses, probable authors, language variants [eg,
American vs British English], or pronunciations).

6. Creation of cache/output directories that will store downloaded HTML and
wikitext information. Users can configure whether or not to use the cache.
Page revision is part of the key when retrieving from the cache, so
deletion of the cache files with the revision information will result in
the latest revision number being retrieved. If the revision is not changed
and reading from the cache is configured, the program will know there is
no need to re-update the media list or HTML/wikitext output for the page.

7. An easy-to-use wrapper that downloads headword and audio file
information into objects, and then optionally outputs the results in a
text file at the word or audio file level.

8. Support to sleep a specified amount of time after a REST API call to
comply with Wikimedia™ rate limits.

9. Logging using the `logging` package is used in the standard manner
with a null handler attached in the `__init__.py`.

10. Support for `GermanWord` objects, which are like `Headword` objects, but
have an additional list of grammar information for each dictionary entry (ie,
for each third-level heading in the page). The information extracted includes:
word separation information, pronunciations, abbreviations, definitions,
origins, synonyms, opposites, hyponyms, hypernyms, examples, expressions,
characteristic word combinations, word formations, references and additional
information, sources, alternate spellings, sayings/proverbs, comparative and
superlative form(s) of adjectives, verb forms (first, second and third person
singular present, first/third singular preterite, past participle, helper
verb, and the Subjunctive II [Konjuntiv II]), the usual 8 noun declinations
(4 cases by singular/plural) and whether the noun declines as an adjective).

11. Support for `PolishWord` objects, which are like `Headword` objects,
but have an additional list of over sixty attributes with grammar information
for the dictionary entry. The information extracted includes: pronunciations,
definitions, etymology, synonyms, antonyms, hyponyms, hypernyms, examples,
expressions, word combinations, word formations, references, syntax,
meronyms, holonyms, and cautions. Up to two comparative forms for the
adjective are presented, along with over 15 verb conjugated or
derived forms, noun gender (both as {'m','f','n'} and also as subcategories
for the masculine nouns by person, animal, and/or thing.), and the usual
14 declinations (7 cases by singular/plural).

In the future (potentially), users can record their decision about
whether to request download of an audio file and pass the decision back
into package objects or functions to select files for download. Currently,
the decision will be stored in the object but will not cause downloading
until the package is updated to support this.

EXAMPLE
-------
from wikwork import wrapper, page_media, io_options
import logging

# set up the logger to print to the console
logger = logging.getLogger('wikwork')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

my_headers = {
    'User-Agent': '(wikwork Python package) (email or phone)'
}

io_opts = io_options.IOOptions(
     output_dir='cache_output/de',
     project='Wiktionary',
     headers=my_headers)

pref_licenses = ['{{cc-by-sa 4.0}}', '{{cc-by-sa-4.0}}',
                 '{{self|cc-by-sa-4.0}}']

# Sort first by pronunciation not from Austria, then by whether the audio
# is likely a pronuncation of only the headword, then by preferred license
# status, then by pronunciation (as German words ending in '-ig' often
# have two variants recorded, so this preferentially selects those
# sounding like '-ik' [IPA: -ɪk] over '-isch' [IPA: -ɪç]).
def my_sort(x: page_media.AudioFile):
     return (not x.filename.startswith('De-at-'),
     x.prob_headword,
     x.prob_license in pref_licenses,
     re.search('ɪk/', x.wikitext) is not None)

# can use the wrapper (de_input.txt has a column  with header = 'Word'
# and then rows with values given by input_list).

input_list = ['Kind','Montag','helfen','Zahl','Wunderbar!',
              'rot','sonnig','zum Beispiel']

res = wrapper.words_wrapper(
     input_words_filename=f'de_input.txt',
     headword_lang_code='de',
     audio_html_lang_code='en',
     io_options=io_opts,
     input_words_column_name='Word',
     fetch_word_page=True,
     fetch_audio_info=True,
     sort_key=my_sort,
     output_words_filename='de_output_words.txt',
     output_audios_filename='de_output_audios.txt',
     output_wikitext_filename='de_wiki.txt'
     )

# ... do other things with res if desired ...

# ... or instead of using the wrapper, create Headword objects directly ...
# (One could also make german.GermanWord objects instead of Headword objects.
# The difference is GermanWord objects will parse the wikitext of the headword
# page for grammar information. See german.GermanWord for details.)

res2 = []
for word in input_list:
    word_info = page_media.Headword(headword=word, lang_code='de')
    if word_info.valid_input:
        # need to get revision info first
        word_info.fetch_revision_info(io_options=io_opts)
        # optionally get word_page (https://de.wiktionary.org/wiki/foo)
        word_info.fetch_word_page(io_options=io_opts)
        # optionally get list of audio files and their info from from
        #    (https://en.wiktionary.org/wiki/File:audio_filename.ogg)
        word_info.fetch_audio_info(io_options=io_opts,
            audio_html_lang_code='en', sort_key=my_sort)
        # ... whatever else user wants to do ...
        res2.append(word_info)

OTHER CONSIDERATIONS
--------------------
1. The following page has other useful points to consider when deciding
whether or how to use downloaded media:
    https://commons.wikimedia.org/wiki/Commons:Reusing_content_outside_Wikimedia

2. Users should familiarize themselves with wikitext and especially
templates.  For example, the file-namespace pages with license/author
information are typically quite small (<100 characters). The 'Template:'
namespace on Wikimedia Commons™ can be used to find information about a
template (ie, strings enclosed in two braces '{{...}}'. For example,
information about the template '{{cc-zero}}' can be found at
    https://commons.wikimedia.org/wiki/Template:cc-zero (which redirects to
    https://commons.wikimedia.org/wiki/Template:Cc-zero).
One would expect these templates to not change much over time (the one
linked above was changed only four times from when it was protected in
October 2013 to February 2024).

3. There may be other methods of retrieving license information, perhaps
through MediaWiki™ action APIs or Wikidata™. For action APIs, it does seem
to be possible with images.

4. Determining which template parameters to assign to which attributes was
based on researching templates at the time of writing the function that
parses such templates. Templates are not retrieved 'in real time' by the
package at the time of function execution. Information in the docstrings of
the relevant `GermanEntry` or `PolishEntry` objects indicate the source
parameter for all such attributes so that users can verify at the time of
program execution, if desired, the meaning of the parameter has not changed.

5. Users planning a very large number of requests might be better off using
a database dump.

KNOWN ISSUES
-------------
The media list REST API call for the Spanish Wiktionary returns information
about very few audio files compared to what is available on the headword
page.  Presumably whatever parser the REST API call uses to extract the
media list doesn't recognize the template the files are nested in.
"""

#------------------------------------------------------------------------------
# File:    __init__.py
# Date:    2024-02-29
# Author:  Ray Griner
# Changes:
# 20240301RG: Add __author__, __version__, and __all__
#------------------------------------------------------------------------------
__author__ = 'Ray Griner'
__version__ = '0.4.0'
__all__ = ['io_options','page_media','wrapper']

import logging

from .page_media import Headword, AudioFile
from .io_options import IOOptions

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

