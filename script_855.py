import asyncio
import sys
from theHarvester import __main__
def main():
    platform = sys.platform
    if platform == 'win32':
        import multiprocessing
        multiprocessing.freeze_support()
        try:
            import winloop
            asyncio.DefaultEventLoopPolicy = winloop.EventLoopPolicy
        except ModuleNotFoundError:
            asyncio.DefaultEventLoopPolicy = asyncio.WindowsSelectorEventLoopPolicy
    else:
        import uvloop
        uvloop.install()
        if 'linux' in platform:
            import aiomultiprocess
            aiomultiprocess.set_context('fork')
    asyncio.run(__main__.entry_point())