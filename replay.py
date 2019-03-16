import display.gui as gui
import game.util as util


def main():
    config = util.readConfig('settings.ini')

    app = gui.createApp([])
    guiInstance = gui.createReplayGui(config)
    
    app.exec()
    
    # Please linter, use app and guiInstance somewhere
    util.clear([app, guiInstance])


if __name__ == '__main__':
    main()
