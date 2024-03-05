# print('Loading modules...', end='')

# I know, the following is ugly, but I need those try's to
# run the command in my dev setting AND from
# a deployment set-up... surely I'm setting
# things wrong [TODO] find why and clean up this mess
try:
    from . import yaltc
except:
    import yaltc
try:
    from . import device_scanner
except:
    import device_scanner
try:
    from . import timeline
except:
    import timeline
try:
    from . import multi2polywav
except:
    import multi2polywav

import argparse
from loguru import logger
from pathlib import Path
# import os, sys
import os, sys
from rich.progress import track
# from pprint import pprint
from rich.console import Console
# from rich.text import Text
from rich.table import Table
from rich import print
# import itertools
# from datetime import timedelta

# print(' done')


av_file_extensions = \
"""MOV webm mkv flv flv vob ogv ogg drc gif gifv mng avi MTS M2TS TS mov qt
wmv yuv rm rmvb viv asf amv mp4 m4p m4v mpg mp2 mpeg mpe mpv mpg mpeg m2v
m4v svi 3gp 3g2 mxf roq nsv flv f4v f4p f4a f4b 3gp aa aac aax act aiff alac
amr ape au awb dss dvf flac gsm iklax ivs m4a m4b m4p mmf mp3 mpc msv nmf
ogg oga mogg opus ra rm raw rf64 sln tta voc vox wav wma wv webm 8svx cda""".split()

logger.level("DEBUG", color="<yellow>")

def process_files_with_progress_bars(medias):
    recordings = []
    rec_with_yaltc = []
    times = []
    for m in track(medias,
            description="1/4 Initializing Recording objects:"):
        # file_alias = 'dummy'
        recordings.append(yaltc.Recording(m))
    for r in track(recordings,
            description="2/4   Checking if files have YaLTC:"):
        if r.seems_to_have_YaLTC_at_beginning():
            rec_with_yaltc.append(r)
    for r in track(rec_with_yaltc,
            description="3/4            Finding start times:"):
        times.append(r.get_start_time())
    return recordings, rec_with_yaltc, times

def process_files(medias):
    recordings = []
    rec_with_yaltc = []
    times = []
    for m in medias:
        recordings.append(yaltc.Recording(m))
    for r in recordings:
        # print('%s duration %.2fs'%(r.AVpath.name, r.get_duration()))
        if r.seems_to_have_YaLTC_at_beginning():
            rec_with_yaltc.append(r)
    for r in rec_with_yaltc:
        times.append(r.get_start_time())
    return recordings, rec_with_yaltc, times

def process_single(file, args):
    # argument is a single file
    m = device_scanner.media_dict_from_path(Path(file))
    a_rec = yaltc.Recording(m)
    time = a_rec.get_start_time(plots=args.plotting)
    if time != None:
        frac_time = int(time.microsecond / 1e2)
        d = '%s.%s'%(time.strftime("%Y-%m-%d %H:%M:%S"),frac_time)
        if args.terse:
            print('%s UTC:%s pulse: %i in chan %i'%(file, d, a_rec.sync_position,
                        a_rec.YaLTC_channel))
        else:
            print('\nRecording started at [gold1]%s[/gold1] UTC'%d)
            print('true sample rate: [gold1]%.3f Hz[/gold1]'%a_rec.true_samplerate)
            print('first sync at [gold1]%i[/gold1] samples in channel %i'%(a_rec.sync_position,
                        a_rec.YaLTC_channel))
            print('N.B.: all results are precise to the displayed digits!\n')
    else:
        if args.terse:
            print('%s UTC: None'%(file))
        else:
            print('Start time couldnt be determined')
    quit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
                "directory",
                type=str,
                nargs=1,
                help="path of media directory"
                )
    # parser.add_argument("directory", nargs="?", help="path of media directory")
    # parser.add_argument('-v', action='store_true')
    parser.add_argument('-v', action='store_true', default=False,
                    dest='verbose_output',
                    help='Set verbose ouput')
    parser.add_argument('-p', action='store_true', default=False,
                    dest='plotting',
                    help='Make plots')
    parser.add_argument('--isos', action='store_true', default=False,
                    dest='write_ISOs',
                    help='Write ISO sound files')
    parser.add_argument('--nosync', action='store_true',
                    dest='nosync',
                    help='just scan and decode')
    parser.add_argument('--terse', action='store_true',
                    dest='terse',
                    help='terse output')
    # parser.add_argument('--io', dest='output_structure', type=str, default='loose',
    #                 help='should be one of: loose [DEFAULT], foldercam')
    args = parser.parse_args()
    # if not args.output_structure in 'loose foldercam reconf'.split():
    #     print('Unknown --io option value "%s", should be one of: loose [DEFAULT] or foldercam'%args.output_structure)
    #     quit()
    if args.verbose_output:
        logger.add(sys.stderr, level="DEBUG")
    # logger.add(sys.stdout, filter="__main__")
    # logger.add(sys.stdout, filter="device_scanner")
    # logger.add(sys.stdout, filter="yaltc")
    # logger.add(sys.stdout, filter="timeline")
    # logger.add(sys.stdout, filter=lambda r: r["function"] == "_enforce_folder_is_device")
    # logger.add(sys.stdout, filter=lambda r: r["function"] == "build_audio_and_write_video")
    # logger.add(sys.stdout, filter=lambda r: r["function"] == "_get_BFSK_word_boundaries")
    top_dir = args.directory[0]
    if os.path.isfile(top_dir):
        file = top_dir
        process_single(file, args)
    if not os.path.isdir(top_dir):
        print('%s is not a directory or doesnt exist.'%top_dir)
        quit()
    multi2polywav.poly_all(top_dir)
    scanner = device_scanner.Scanner(top_dir, stay_silent=args.terse)
    # (Path(top_dir)/Path('tictacsynced')).mkdir(exist_ok=True)
    # scanner.cluster_media_files_by_name()
    scanner.scan_media_and_build_devices_UID(recursive=False)
    if not args.terse:
        print('\n\nFound [gold1]%i[/gold1] media files from [gold1]%i[/gold1] devices'%(
            len(scanner.found_media_files),
            scanner.get_devices_number()), end='')
        print('\nThese recordings will be analysed for timestamps:\n')
        for m in (scanner.found_media_files):
            print('   ', '[gold1]%s[/gold1]'%m['path'].name)
        print()
    if args.verbose_output or args.terse: # verbose or terse, so no progress bars
        rez = process_files(scanner.found_media_files)
    else: 
        rez = process_files_with_progress_bars(scanner.found_media_files)
    recordings, rec_with_yaltc, times = rez
    recordings_with_time =  [
        rec 
        for rec in rec_with_yaltc
        if rec.get_start_time()
        ]
    if not args.terse:    
        print('\n\n')
        table = Table(title="tictacsync results")
        table.add_column("Recording\n", justify="center", style='gold1')
        table.add_column("YaLTC\nChannel", justify="center", style='gold1')
        # table.add_column("Device\n", justify="center", style='gold1')
        table.add_column("UTC times\nstart:end", justify="center", style='gold1')
        table.add_column("Clock drift\n(ppm)", justify="right", style='gold1')
        table.add_column("SN ratio\n(dB)", justify="center", style='gold1')
        table.add_column("Date\n", justify="center", style='gold1')
        rec_WO_time = [
            rec.AVpath.name
            for rec in rec_with_yaltc
            if not rec.get_start_time()
            ]
        if rec_WO_time:
            print('No time found for: ',end='')
            [print(rec, end=' ') for rec in rec_WO_time]
            print('\n')
        for r in recordings_with_time:
            date = r.get_start_time().strftime("%y-%m-%d")
            start_HHMMSS = r.get_start_time().strftime("%Hh%Mm%Ss")
            end_MMSS = r.get_end_time().strftime("%Mm%Ss")
            times_range = start_HHMMSS + ':' + end_MMSS
            table.add_row(
                str(r.AVpath.name),
                str(r.YaLTC_channel),
                # r.device,
                times_range,
                # '%.6f'%(r.true_samplerate/1e3),
                '%2i'%(r.get_samplerate_drift()),
                '%.0f'%r.decoder.SN_ratio,
                date
                )
        console = Console()
        console.print(table)
        print('\n')
    n_devices = scanner.get_devices_number()
    OUT_struct_for_mcam = scanner.top_dir_has_multicam
    # if n_devices > 2:
    #     print('\nMerging for more than 2 devices is not implemented yet, quitting...')
    #     quit()
    if len(recordings_with_time) < 2:
        if not args.terse:
            print('\nNothing to sync, exiting.\n')
        quit()
    matcher = timeline.Matcher(recordings_with_time)
    matcher.scan_audio_for_each_ref_rec()
    if not matcher.video_mergers:
        if not args.terse:
            print('\nNothing to sync, bye.\n')
        quit()
    if args.verbose_output or args.terse: # verbose, so no progress bars
        for stitcher in matcher.video_mergers:
            stitcher.build_audio_and_write_video(top_dir, OUT_struct_for_mcam,
                                                    args.write_ISOs)
    else: 
        for stitcher in track(matcher.video_mergers,
            description="4/4         Merging sound to videos:"):
            stitcher.build_audio_and_write_video(top_dir, OUT_struct_for_mcam,    
                                                    args.write_ISOs)
    if not args.terse:
        print("\n")
    # if args.output_structure == 'foldercam':
    print('output written in [gold1]%s[/gold1] folder in [gold1]%s[/gold1]\n'%(
            'SyncedMedia',top_dir))
    # if args.output_structure == 'loose':
    for stitcher in matcher.video_mergers:
        print('[gold1]%s[/gold1]'%stitcher.ref_recording.AVpath.name, end='')
        for audio in stitcher.get_matched_audio_recs():
            print(' + [gold1]%s[/gold1]'%audio.AVpath.name, end='')
        new_file = stitcher.ref_recording.final_synced_file.parts
        print(' became [gold1]%s[/gold1]'%stitcher.ref_recording.final_synced_file.name)
        # matcher._build_otio_tracks_for_cam()
    matcher.shrink_gaps_between_takes()
    
if __name__ == '__main__':
    main()






