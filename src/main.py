import pygame
from src.manager import Manager


def main():
    """メイン"""

    # ゲーム全体設定
    pygame.display.set_caption("game")

    manager = Manager()
    manager.mainroop()


if __name__ == '__main__':
    main()