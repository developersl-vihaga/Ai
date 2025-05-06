""" An example of a plugin. """
from lib.common.plugins import Plugin
import lib.common.helpers as helpers
print("Hello from your new plugin!")
class Plugin(Plugin):
    description = "An example plugin."
    def onLoad(self):
        """ any custom loading behavior - called by init, so any
        behavior you'd normally put in __init__ goes here """
        print("Custom loading behavior happens now.")
        self.calledTimes = 0
    def register(self, mainMenu):
        """ any modifications to the mainMenu go here - e.g.
        registering functions to be run by user commands """
        mainMenu.__class__.do_test = self.do_test
    def do_test(self, args):
        "An example of a plugin function."
        print("This is executed from a plugin!")
        print(helpers.color("[*] It can even import Empire functionality!"))
        self.calledTimes += 1
        print("This function has been called {} times.".format(self.calledTimes))