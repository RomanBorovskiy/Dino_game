import logging

from game import GameApp


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('start game')
    game = GameApp()
    game.run()
    game.close()
    logging.info('exit game')


if __name__ == '__main__':
    main()
