import asyncio

from jupyterhub.apihandlers import default_handlers
from jupyterhub.apihandlers.users import SpawnProgressAPIHandler
from jupyterhub.scopes import needs_scope
from outpostspawner.api_flavors_update import async_get_flavors
from tornado import web

from .utils import get_general_spawn_event
from .utils import get_stopped_spawners


class UserSpawnNotificationAPIHandler(SpawnProgressAPIHandler):
    """EventStream handler for active spawns for a specific user"""

    @needs_scope("read:servers")
    async def get(self, user_name):
        self.set_header("Cache-Control", "no-cache")
        user = self.find_user(user_name)
        if user is None:
            # no such user
            raise web.HTTPError(404)
        # Start sending keepalive to avoid proxies closing the connection
        asyncio.ensure_future(self.keepalive())

        event = get_general_spawn_event()
        await event.wait()

        user_spawners = user.spawners.values()
        stopped_spawners = get_stopped_spawners()
        spawning = []
        stopped = []
        for s in user_spawners:
            if s.pending:
                spawning.append(s.name)
            if s.name in stopped_spawners:
                stopped.append(s.name)
                stopped_spawners.remove(s.name)
        flavors = await async_get_flavors(self.log, user)
        event_data = {
            # Set active spawners as event data
            "spawning": spawning,
            "stopped": stopped,
            "outpostflavors": flavors,
        }
        await self.send_event(event_data)
        # Clear event after sending in case stream has been closed
        event.clear()
        return
    

default_handlers.append(
    (r"/api/users/([^/]+)/notifications/spawners", UserSpawnNotificationAPIHandler)
)
