from .game_main import Game
import asyncio

# main for pygbag

async def main():
    game = Game()
    await game.run_async()

asyncio.run(main())