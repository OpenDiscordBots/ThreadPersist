from dotenv import load_dotenv
from os import environ as env

from src.bot import Bot

load_dotenv()


def main() -> None:
    bot = Bot(command_prefix="!", help_command=None)  # type: ignore
    bot.load_extensions([
        "src.exts.threads",
    ])

    bot.run(env["TOKEN"])


if __name__ == "__main__":
    main()
