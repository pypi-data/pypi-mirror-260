
# cd /home/lutzray/SyncQUO/Dev/AtomicSync/Sources/PostProduction/tictacsync/tictacsync
# while inotifywait --recursive -e close_write . ; do python entry.py  tests/multi2/; done
# above for linux


av_file_extensions = \
"""webm mkv flv flv vob ogv ogg drc gif gifv mng avi MTS M2TS TS mov qt
wmv yuv rm rmvb viv asf amv mp4 m4p m4v mpg mp2 mpeg mpe mpv mpg mpeg m2v
m4v svi 3gp 3g2 mxf roq nsv flv f4v f4p f4a f4b 3gp aa aac aax act aiff alac
amr ape au awb dss dvf flac gsm iklax ivs m4a m4b m4p mmf mp3 mpc msv nmf
ogg oga mogg opus ra rm raw rf64 sln tta voc vox wav wma wv webm 8svx cda MOV AVI
WEBM MKV FLV FLV VOB OGV OGG DRC GIF GIFV MNG AVI MTS M2TS TS MOV QT
WMV YUV RM RMVB VIV ASF AMV MP4 M4P M4V MPG MP2 MPEG MPE MPV MPG MPEG M2V
M4V SVI 3GP 3G2 MXF ROQ NSV FLV F4V F4P F4A F4B 3GP AA AAC AAX ACT AIFF ALAC
AMR APE AU AWB DSS DVF FLAC GSM IKLAX IVS M4A M4B M4P MMF MP3 MPC MSV NMF
OGG OGA MOGG OPUS RA RM RAW RF64 SLN TTA VOC VOX WAV WMA WV WEBM 8SVX CDA MOV AVI BWF""".split()

import ffmpeg
from os import listdir
from os.path import isfile, join, isdir
from collections import namedtuple
from pathlib import Path
from pprint import pformat 
# from collections import defaultdict
from loguru import logger
# import pathlib, os.path
import sox, tempfile
# from functools import reduce
from rich import print
from itertools import groupby
# from sklearn.cluster import AffinityPropagation
# import distance
try:
    from . import multi2polywav
except:
    import multi2polywav


# utility for accessing pathnames
def _pathname(tempfile_or_path):
    if isinstance(tempfile_or_path, str):
        return tempfile_or_path
    if isinstance(tempfile_or_path, Path):
        return str(tempfile_or_path)
    if isinstance(tempfile_or_path, tempfile._TemporaryFileWrapper):
        return tempfile_or_path.name
    else:
        raise Exception('%s should be Path or tempfile...'%tempfile_or_path)

def print_grby(grby):
    for key, keylist in grby:
        print('\ngrouped by %s:'%key)
        for e in keylist:
            print(' ', e)

Device = namedtuple("Device", ["UID", "folder", "name", "type"])

def media_dict_from_path(p):
        # return dict of metadata for mediafile using ffprobe
        # probe = ffmpeg.probe(p)
        try:
            probe = ffmpeg.probe(p)
            logger.debug('probing %s'%p)
        except ffmpeg._run.Error:
            print('Error ffprobing %s\nquitting.'%p)
            quit()
        
        dev_UID, dev_type = get_device_ffprobe_UID(p)
        time_base = eval(probe['streams'][0]['time_base'])
        duration_in_secondes = float(probe['format']['duration'])
        sample_length = round(duration_in_secondes/time_base)
        return {
            'path' : p,
            'sample length' : sample_length,
            'dev' : Device(dev_UID, p.parent, None, dev_type),
            }

def get_device_ffprobe_UID(file):
    """
    Tries to find an unique hash integer identifying the device that produced
    the file based on the string inside ffprobe metadata  without any
    reference to date nor length nor time. Find out with ffprobe the type
    of device: CAM or REC for videocamera or audio recorder.

    Device UIDs are used later in Montage._get_concatenated_audiofile_for()
    for grouping each audio or video clip along its own timeline track.
    
    Returns a tuple: (UID, CAM|REC)
    
    If an ffmpeg.Error occurs, returns (None, None)
    if no UID is found, but device type is identified, returns (None, CAM|REC)

    """
    file = Path(file)
    logger.debug('trying to find UID probe for %s'%file)
    try:
        probe = ffmpeg.probe(file)
    except ffmpeg.Error as e:
        print('ffmpeg.probe error')
        print(e.stderr, file)
        return None, None
        # fall back to folder name
    streams = probe['streams']
    codecs = [stream['codec_type'] for stream in streams]
    device_type = 'CAM' if 'video' in codecs else 'REC'
    format_dict = probe['format'] # all files should have this
    if 'tags' in format_dict:
        probe_string = pformat(format_dict['tags'])
        probe_lines = [l for l in probe_string.split('\n') 
                if '_time' not in l 
                and 'time_' not in l 
                and 'date' not in l ]
        # this removes any metadata related to the file
        # but keeps metadata related to the device
        UID = hash(''.join(probe_lines))
    else:
        UID = None
    logger.debug('ffprobe_UID is: %s'%UID)
    return UID, device_type


class Scanner:
    """
    Class that encapsulates scanning of the directory given as CLI argument.
    Depending on the IO structure choosen (loose|folder_is_device), enforce some directory
    structure (or not). Build a list of media files found and a try to 
    indentify uniquely the device used to record each media file.

    Attributes:

        input_structure: string

            Any of
                'loose'
                    all files audio + video are in top folder
                'folder_is_device'
                    eg for multicam on Davinci Resolve

        top_directory : string

            String of path of where to start searching for media files.

        top_dir_has_multicam : bool

            If top dir is folder structures AND more than on cam

        devices_names : dict of str

            more evocative names for each device, keys are same as
            self.devices_UID_count

        found_media_files: list of dicts
                {
                'path' : as is ,
                'sample length' : as is
                'dev' : Device namedtuple
                }
    """

    def __init__(
                    self,
                    top_directory,
                    stay_silent=False,
                ):
        """
        Initialises Scanner

        """
        self.top_directory = top_directory
        self.found_media_files = []
        self.stay_silent = stay_silent


    def get_devices_number(self):
        # how many devices have been found
        return len(set([m['dev'].UID for m in self.found_media_files]))

    def scan_media_and_build_devices_UID(self, recursive=True):
        """
        Scans self.top_directory recursively for files with known audio-video
        extensions. For each file found, a device fingerprint is obtained from
        their ffprobe result to ID the device used.


        Also looked for are multifile recordings: files with the exact same
        length. When done, calls

        Returns nothing

        Populates Scanner.found_media_files, a list of dict as
                {
                'path' : as is ,
                'sample length' : as is
                'dev' : Device namedtuple
                }

        Sets input_structure = 'loose'|'folder_is_device'

        """
        visible = [f for f in listdir(self.top_directory) if f[0] != '.']
        logger.debug('visible: %s'%visible)
        are_dir = all([isdir(join(self.top_directory, f)) for f in visible])
        are_files = all([isfile(join(self.top_directory, f)) for f in visible])
        # onlyfiles = [f for f in listdir(self.top_directory) if isfile()]

        logger.debug('dir: %s'%[isdir(join(self.top_directory, f)) for f in visible])
        if are_dir:
            print('\nAssuming those are device folders: ',end='')
            [print(f, end=', ') for f in visible[:-1]]
            print('%s.\n'%visible[-1])
            self.input_structure = 'folder_is_device'
        else: # are_files
            self.input_structure = 'loose'
        if not are_dir and not are_files:
            print('\nInput structure mixed up, files AND folders at top level')
            print('  %s, quitting.\n'%self.top_directory)
            quit()
        # quit()
        files = Path(self.top_directory).rglob('*.*')
        paths = [
            p
            for p in files
            if p.suffix[1:] in av_file_extensions
            and 'SyncedMedia' not in p.parts
        ]
        for p in paths:
            new_media = media_dict_from_path(p) # dev UID set here
            self.found_media_files.append(new_media)
        logger.debug('Scanner.found_media_files = %s'%self.found_media_files)
        if self.input_structure == 'folder_is_device':
                self._enforce_folder_is_device()
                self._use_folder_as_device_name()
        else:
            self.top_dir_has_multicam = False
        pprint_found_media_files = pformat(self.found_media_files)
        logger.debug('scanner.found_media_files = %s'%pprint_found_media_files)

    def _use_folder_as_device_name(self):
        """
        For each media in self.found_media_files replace existing Device.name by
        folder name.

        Returns nothing
        """
        for m in self.found_media_files:
            folder_name = m['path'].parent.name
            # known_folder_name = [media['dev'].UID for media
            #     in self.found_media_files]
            # if folder_name not in known_folder_name:
            # print('l238', m['dev']) 
            m['dev'] = m['dev']._replace(name=folder_name)
            # print('l240', m['dev']) 
            # m['dev'].UID = folder_name
            # else:
            #     print('already existing folder name: [gold1]%s[/gold1] please change it and rerun'%m['path'].parent)
            #     quit()
        logger.debug(self.found_media_files)

    def _enforce_folder_is_device(self):
        """

        Checks for files in self.found_media_files for structure as following.

        Warns user and quit program for:
          A- folders with mix of video and audio
          B- folders with mix of uniquely identified devices and unUIDied ones
          C- folders with mixed audio (or video) devices
        
        Warns user but proceeds for:
          D- folder with only unUIDied files (overlaps will be check later)
        
        Proceeds silently if 
          E- all files in the folder are from the same device

        Returns nothing
        """
        def _list_duplicates(seq):
          seen = set()
          seen_add = seen.add
          # adds all elements it doesn't know yet to seen and all other to seen_twice
          seen_twice = set( x for x in seq if x in seen or seen_add(x) )
          # turn the set into a list (as requested)
          return list( seen_twice )
        folder_key = lambda m: m['path'].parent
        medias = sorted(self.found_media_files, key=folder_key)
        # build lists for multiple reference of iterators
        media_grouped_by_folder = [ (k, list(iterator)) for k, iterator
                        in groupby(medias, folder_key)]
        logger.debug('media_grouped_by_folder %s'%media_grouped_by_folder)
        complete_path_folders = [e[0] for e in media_grouped_by_folder]
        name_of_folders = [p.name for p in complete_path_folders]
        logger.debug('complete_path_folders with media files %s'%complete_path_folders)
        logger.debug('name_of_folders with media files %s'%name_of_folders)
        # unique_folder_names = set(name_of_folders)
        repeated_folders = _list_duplicates(name_of_folders)
        logger.debug('repeated_folders %s'%repeated_folders)
        if repeated_folders:
            print('There are conflicts for some repeated folder names:')
            for f in [str(p) for p in repeated_folders]:
                print(' [gold1]%s[/gold1]'%f)
            print('Here are the complete paths:')
            for f in [str(p) for p in complete_path_folders]:
                print(' [gold1]%s[/gold1]'%f)
            print('please rename and rerun. Quitting..')
            quit()
        # print(media_grouped_by_folder)
        n_CAM_folder = 0
        for folder, list_of_medias_in_folder in media_grouped_by_folder:
            # list_of_medias_in_folder = list(media_files_same_folder_iterator)
            # check all medias are either video or audio recordings in folder
            # if not, warn user and quit.
            dev_types = set([m['dev'].type for m in list_of_medias_in_folder])
            logger.debug('dev_types %s'%dev_types)
            if dev_types == {'CAM'}:
                n_CAM_folder += 1
            if len(dev_types) != 1:
                print('\nProblem while scanning for media files. In [gold1]%s[/gold1]:'%folder)
                print('There is a mix of video and audio files:')
                [print('[gold1]%s[/gold1]'%m['path'].name, end =', ')
                    for m in list_of_medias_in_folder]
                print('\nplease move them in exclusive folders and rerun.\n')
                quit()
            unidentified = [m for m in list_of_medias_in_folder
                if m['dev'].UID == None]
            UIDed = [m for m in list_of_medias_in_folder
                if m['dev'].UID != None]
            logger.debug('devices in folder %s:'%folder)
            logger.debug('  media with unknown devices %s'%unidentified)
            logger.debug('  media with UIDed devices %s'%UIDed)
            if len(unidentified) != 0 and len(UIDed) != 0:
                print('\nProblem while grouping files in [gold1]%s[/gold1]:'%folder)
                print('There is a mix of unidentifiable and identified devices.')
                print('Is this file:')
                for m in unidentified:
                    print(' [gold1]%s[/gold1]'%m['path'].name)
                answer = input("In the right folder?")
                if answer.upper() in ["Y", "YES"]:
                    continue
                elif answer.upper() in ["N", "NO"]:
                    # Do action you need
                    print('please move the following files in a folder named appropriately:\n')
                    quit()
            # if, in a folder, there's a mix of different identified devices,
            # Warn user and quit.
            # devices = set([m['dev'].UID for m in list_of_medias_in_folder])
            if len(dev_types) != 1:
                print('\nProblem while scanning for media files. In [gold1]%s[/gold1]:'%folder)
                print('There is a mix of files from different devices:')
                [print('[gold1]%s[/gold1]'%m['path'].name, end =', ')
                    for m in list_of_medias_in_folder]
                print('\nplease move them in exclusive folders and rerun.\n')
                quit()
            if len(unidentified) == len(list_of_medias_in_folder):
                # all unidentified
                if len(unidentified) > 1:
                    print('Assuming those files are from the same device:')
                    [print('[gold1]%s[/gold1]'%m['path'].name, end =', ')
                        for m in unidentified]
                    print('\nIf not, there\'s a risk of error: put them in exclusive folders and rerun.')
            # if we are here, the check is done: either 
            #   all files in folder are from unidentified device or
            #   all files in folder are from the same identified device
        logger.debug('n_CAM_folder %i'%n_CAM_folder)
        self.top_dir_has_multicam = n_CAM_folder > 1
        logger.debug('top_dir_has_multicam: %s'%self.top_dir_has_multicam)
        return





