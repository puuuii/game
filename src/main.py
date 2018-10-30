import pygame

from src.manager import GameManager


def main():
    """メイン"""

    # ゲーム全体設定
    pygame.display.set_caption("game")

    manager = GameManager()
    manager.mainroop()


if __name__ == '__main__':
    main()