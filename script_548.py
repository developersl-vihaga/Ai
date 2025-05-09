""" Utilities and helpers and etc. for plugins """
import importlib
import lib.common.helpers as helpers
def load_plugin(mainMenu, pluginName):
    """ Given the name of a plugin and a menu object, load it into the menu """
    fullPluginName = "plugins." + pluginName
    module = importlib.import_module(fullPluginName)
    pluginObj = module.Plugin(mainMenu)
    mainMenu.loadedPlugins[pluginName] = pluginObj
class Plugin(object):
    description = "This is a description of this plugin."
    def __init__(self, mainMenu):
        print(helpers.color("[*] Initializing plugin..."))
        print(helpers.color("[*] Doing custom initialization..."))
        self.onLoad()
        print(helpers.color("[*] Registering plugin with menu..."))
        self.register(mainMenu)
    def onLoad(self):
        """ Things to do during init: meant to be overridden by
        the inheriting plugin. """
        pass
    def register(self, mainMenu):
        """ Any modifications made to the main menu are done here
        (meant to be overriden by child) """
        pass