#    A wrapper with a relatively simple interface for common use-cases
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

"""A wrapper with a relatively simple interface for common use-cases.
"""

#------------------------------------------------------------------------------
# File:    wrapper.py
# Author:  Ray Griner
# Date:    2024-02-29
# Changes:
# 20240301RG: Add __author__ and __all___
# 20240302RG: Chage write_output_files to QUOTE_MINIMAL from QUOTE_NONE
# 20240303RG: Add support for GermanWord objects in write_output_files and
#   words_wrapper (when lang_code='de', GermanWord objects will be created
#   instead of Headword objects.
#------------------------------------------------------------------------------
__author__ = 'Ray Griner'
__all__ = ['write_output_files','words_wrapper']

from collections.abc import Callable
from typing import Optional, Union, Any
import csv
import logging
from wikwork import page_media
from wikwork import german
from wikwork import polish
from wikwork import io_options as io_opts
#import wikwork.page_media
#import wikwork.io_options as io_opts

logger = logging.getLogger(__name__)

def write_output_files(headword_list :
            Union[list[page_media.Headword],list[german.GermanWord]],
        output_words_filename : Optional[str],
        output_audios_filename : Optional[str],
        output_wikitext_filename : Optional[str]) -> None:
    """Write information from list of Headword objects (or subclass) to files.

    Requires all objects in list to be of the same type. Will use type of
    first object in list to determine which fields to output.

    Parameters
    ----------
    output_words_filename : str, optional
        Print results one record per word. See `wrapper.words_wrapper` for
        details. Output fields vary by type of object.
    output_audios_filename : str, optional
        Print results one record per audio. See `wrapper.words_wrapper` for
        details.
    output_wikitext_filename : str, optional
       Call str_wikitext_etal on each audio file for each headword in the
       object that will be returned, and save the result to a single file.

    Returns
    -------
    None
    """

    empty_pl_entry = polish.PolishEntry()
    empty_de_entry = german.GermanEntry()

    maxlen = max(len(row.audio_files) for row in headword_list)
    #-------------------------------------------------------------
    # Write the output words file (flattened to one row per word)
    #-------------------------------------------------------------
    # Write the words file (flattened)
    if output_words_filename:
        with open (output_words_filename, 'w', encoding='utf-8') as csvfile:
            outwriter = csv.writer(csvfile, delimiter='\t',
                                   quoting=csv.QUOTE_MINIMAL)


            # Write header (headword, status_msg, revision,
            #   filename1, prob_license1, ...)
            flathead = ['headword','status_msg','revision']
            is_german = False
            is_polish = False
            if (headword_list
                    and isinstance(headword_list[0], german.GermanWord)):
                is_german = True
                publicvars = [ var for var in vars(empty_de_entry).keys()
                               if var[0] != '_' ]
                flathead.extend( colnm + '_1' for colnm in publicvars )
            elif (headword_list
                    and isinstance(headword_list[0], polish.PolishWord)):
                is_polish = True
                publicvars = [ var for var in vars(empty_pl_entry).keys()
                               if var[0] != '_' ]
                flathead.extend( colnm + '_1' for colnm in publicvars )

            tuphead = ['filename','prob_license','prob_author','revision',
                       'download_status']
            for i in range(maxlen):
                flathead.extend(tup+'_'+str(i+1) for tup in tuphead)
            outwriter.writerow(flathead)

            # Write the data
            for row in headword_list:
                flattened = [row.headword, row.status_msg, row.revision]
                if (is_german or is_polish) and row.entries:
                    flattened.extend(getattr(row.entries[0],colnm)
                        for colnm in publicvars)
                elif is_german or is_polish:
                    flattened.extend('' for colnm in publicvars)
                for tup in row.audio_files:
                    flattened.extend([tup.filename, tup.prob_license,
                        tup.prob_author, tup.revision, tup.download_status])
                outwriter.writerow(flattened)

    #--------------------------------------------------------------------
    # Write the output audio file (not flattened, one row per audio file)
    #--------------------------------------------------------------------
    if output_audios_filename:
        with open (output_audios_filename, 'w', encoding='utf-8') as csvfile:
            outwriter = csv.writer(csvfile, delimiter='\t',
                                   quoting=csv.QUOTE_MINIMAL)

            # write file header
            flathead = ['headword','word_status_msg','word_revision',
                'word_counter','media_list_position','filename',
                'filename_not_safe', 'prob_license','prob_author',
                'audio_revision', 'request_status','download_status']
            outwriter.writerow(flathead)

            # Write the data
            for row in headword_list:
                for ctr, tup in enumerate(row.audio_files):
                    outwriter.writerow([row.headword, row.status_msg,
                        row.revision, ctr+1, tup.filename,
                        tup.filename_not_safe, tup.media_list_position,
                        tup.prob_license, tup.prob_author, tup.revision,
                        tup.request_status, tup.download_status])

    #--------------------------------------------------------------------
    # Write the wikitext, prob_author, prob_license, etc, in a nice
    #   format for each audio file and save to a single file
    #--------------------------------------------------------------------
    if output_wikitext_filename:
        with open(output_wikitext_filename, 'w', encoding='utf-8') as f:
            for headword in headword_list:
                for audio_file in headword.audio_files:
                    f.write(audio_file.str_wikitext_etal())

#------------------------------------------------------------------------------
# Public module-level functions
#------------------------------------------------------------------------------
def words_wrapper(input_words_filename: str,
        input_words_column_name: str,
        headword_lang_code: str,
        audio_html_lang_code: str,
        io_options: io_opts.IOOptions,
        fetch_word_page: bool = False,
        fetch_audio_info: bool = False,
        input_audio_reqs: Union[str, page_media.AudioReqs, None] = None,
        filename_pattern: Optional[str] = None,
        sort_key: page_media.SortKey = lambda x: True,
        parse_wikitext_fn:
            Optional[Callable[[page_media.AudioFile], Any]] = None,
        output_words_filename: Optional[str] = None,
        output_audios_filename: Optional[str] = None,
        output_wikitext_filename: Optional[str] = None,
        ) -> list[page_media.Headword]:
    """Download word and/or audio file info (but not audio files).

    This is intended as an easy-to-use interface to package functionality.
    Users needing more flexibility should call `page_audio.Headword` and
    other public package functions directly. The function takes a list of
    words from an input file and creates a `Headword` object for each. A
    list of the `page_audio.Headword` objects is returned. Key information
    is summarized in three optional output files, the first is one row per
    word, the second is one row per audio file, and the last is a
    print-out of wikitext with the probable author and probable license
    (users interested in downloading audio should check this file if they
    are using `prob_author` and `prob_license` as the regular expression
    parser may not extract all information correctly and the results
    should therefore be cross-checked against the wikitext.

    The function can be called to download word information and then the
    wikitext in the object can be parsed if the user wants to extract
    declination information for nouns, conjugation information for verbs,
    list of references, etc...

    Parameters
    ----------
    input_words_filename : str
        Filename of file contains the words to process. The file should be
        tab-delimited, UTF-8 encoded with no quoting used. The file must
        have a header row and the column containings the words must be
        identified by the input_words_column_name parameter.
    input_words_column_name : str
        Column name containing words to process in input_words_filename
    headword_lang_code : str
        Language code specifying the language of the Wiktionary™ from which
        to retrieve the headword information.
    audio_html_lang_code : str
        Language code specifying the language of the Wiktionary from which
        to retrieve the HTML with info about the audio files
    io_options : io_options.IOOptions
        object controlling how HTTP requests are made and the results are
        cached or output
    fetch_word_page : bool, default: False
        Fetch the page for the headword in HTML and wikitext forms.  See
        `page_audio.Headword` for details.
    fetch_audio_info: bool, default: False
        Fetch the audio file information in HTML and wikitext form for all
        the audio files from the title page of the word, filtering out
        audio files in other languages. See `page_audio.Headword` for
        details.
    input_audio_reqs : {None (default), str, Dict[str, (int, str)]}
        Contains user-specified decisions on which audio files to download.
        See `page_audio.Headword` for details. This function also provides
        the option of passing a str that is the filename of a
        tab-delimited, UTF-8 encoded file with columns 'filename',
        'audio_revision', and 'request_status' (with other columns
        ignored).
    filename_pattern : str, optional
        String containing regular expression used to try to determine the
        language of the audio file. See `page_audio.Headword` for details.
    sort_key : Callable[AudioFile, Any], default: lambda x: True
        Defines a partial key for sorting audio files. See
        `page_audio.Headword.fetch_all_audio` for details.
    parse_wikitext_fn : Callable([AudioFile], None), optional
        User-defined parsing function that if set will replace the default
        parser that sets the `prob_license` and `prob_author` attributes of
        each `page_audio.AudioFile` object. See `page_audio.Headword` for
        details.
    output_words_filename : str, optional
        Outputs selected information about the words and audio files as a
        flat tab-delimited file. Audio files that are fetched (as
        described in the `fetch_audio_info` parameter are included. Output
        columns are: the `headword`, `status_msg`, and `revision`
        attributes of the `page_audio.Headword` (or subclass) object (column
        headers have 'word_' prefixed to the variable name). The next set
        of columns are all the attributes for the first GermanEntry in
        the entries list (if the objects are GermanWord objects), where the
        column name is the attribute name with a '_1' appended. The last set
        of columns are from the audio_files list: `filename`, `prob_license`,
        `prob_author`, `revision`, and `download_status` attributes of each
        item in `Headword.audio_files` (column headers have a counter
        starting '_1', '_2', ... appended to the variable name ['filename_1',
        'prob_license_1', ...]
    output_audios_filename : str, optional
        Formats the same information described in 'output_words_filename'
        parameter (but not including the attributes from the entries list,
        even if the object is GermanWord) as one row per word per audio file
        instead of one row per word. Also adds columns for attributes
        `media_list_position`, `filename_not_safe`, `word_counter`
        (position (starting at 1) in audio_files[]) and `request_status`
        columns.
    output_wikitext_filename : str, optional
        Call `str_wikitext_etal` on each audio file for each headword in
        the object that will be returned, and save the result to a single
        file.

    Returns
    -------
    A list of `page_audio.Headword` objects or german.GermanWord objects, one
    for each word in the input file.

    Trademark Notice
    ----------------
    Wiktionary is a trademark of the Wikimedia Foundation and is used with
    the permission of the Wikimedia Foundation. We are not endorsed by or
    affiliated with the Wikimedia Foundation.
    """

    #----------------------------------------------------------------
    # Validate input
    #----------------------------------------------------------------
    if not isinstance(fetch_word_page, bool):
        raise TypeError('words_wrapper: '
            'fetch_word_page should be bool')
    if not isinstance(fetch_audio_info, bool):
        raise TypeError('words_wrapper: '
            'fetch_audio_info should be bool')
    if not isinstance(input_words_filename, str):
        raise TypeError('words_wrapper: input_words_filename '
                        'should be str')
    if not (output_words_filename is None
            or isinstance(input_words_filename, str)):
        raise TypeError('words_wrapper: output_words_filename '
                        'should be None or str')
    if not (output_audios_filename is None
            or isinstance(output_audios_filename, str)):
        raise TypeError('words_wrapper: output_audios_filename '
                        'should be None or str')

    #-----------------------------------------------------------------
    # Validation done. Get the words to process
    #-----------------------------------------------------------------
    with open(input_words_filename, encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        input_list = [ row[input_words_column_name] for row in reader]

    #-----------------------------------------------------------------
    # Get audio files that are requested for download, and convert
    #   to a dictionary if they were passed in a file
    #-----------------------------------------------------------------

    audio_dict: Optional[page_media.AudioReqs]
    if input_audio_reqs is None:
        audio_dict = None
    elif isinstance(input_audio_reqs, str):
        with open(input_audio_reqs, encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, delimiter='\t',
                                    quoting=csv.QUOTE_NONE)
            audio_dict = {row['filename'] : (int(row['audio_revision']),
                              row['request_status']) for row in reader}
    else:
        audio_dict = input_audio_reqs

    logger.info('Processing %d words from %s in %s.wiktionary.org',
                len(input_list), input_words_filename, headword_lang_code)
    res = []
    for i, word in enumerate(input_list):
        if headword_lang_code not in ['de','pl']:
            word_info = page_media.Headword(headword=word,
                            lang_code=headword_lang_code)
        elif headword_lang_code == 'de':
            word_info = german.GermanWord(headword=word,
                            lang_code=headword_lang_code)
        elif headword_lang_code == 'pl':
            word_info = polish.PolishWord(headword=word,
                            lang_code=headword_lang_code)
        if word_info.valid_input:
            word_info.fetch_revision_info(io_options=io_options)
        if fetch_word_page:
            word_info.fetch_word_page(io_options=io_options)
        if fetch_audio_info:
            word_info.fetch_audio_info(io_options=io_options,
                audio_html_lang_code=audio_html_lang_code,
                sort_key=sort_key, filename_pattern=filename_pattern,
                parse_wikitext_fn=parse_wikitext_fn, audio_reqs=audio_dict)
        if io_options.audio_out_mode is not io_opts.AudioOutMode.NO_OUTPUT:
            pass
            #word_info._fetch_audio(io_options=io_options)
            #word_info._copy_one_audio(io_options=io_options)
        res.append(word_info)
        if ((i+1) % 20) == 0:
            print(f'File: {input_words_filename}: Processed word {i+1}')

    write_output_files(headword_list=res,
        output_words_filename = output_words_filename,
        output_audios_filename = output_audios_filename,
        output_wikitext_filename = output_wikitext_filename)

    return res
