from asyncio import sleep
from datetime import datetime, timedelta

from disnake import Thread, AuditLogAction, AuditLogEntry
from disnake.ext.commands import Cog
from loguru import logger

from src.bot import Bot


class Threads(Cog):
    """Core functionality for ThreadPersist."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

        self.handled = set()

    @property
    def old(self) -> datetime:
        return datetime.utcnow() - timedelta(seconds=20)

    @Cog.listener()
    async def on_thread_update(self, before: Thread, after: Thread) -> None:
        if before.archived and not after.archived:
            self.handled.remove(before.id)
            return

        if before.id in self.handled:
            return

        if after.archived and not before.archived:
            old = self.old

            await sleep(10)

            logs = await before.guild.audit_logs(limit=25, action=AuditLogAction.thread_update).flatten()

            for log in logs:
                log: AuditLogEntry

                if log.created_at.timestamp() < old.timestamp():
                    continue

                if log.target.id == before.id:
                    logger.info(f"Thread {before.id} archived manually, not persisting it.")
                    return

        await after.edit(archived=False)


def setup(bot: Bot) -> None:
    bot.add_cog(Threads(bot))
