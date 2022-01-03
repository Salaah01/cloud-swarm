import typing as _t
import datetime
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth.models import User
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    DenyConnection
)
from channels.layers import get_channel_layer
from sites import models as site_models


def get_site_group_name(site_id: int) -> str:
    """Get the group name for a site."""
    return f'site_{site_id}'


class BenchmarkProgressConsumer(AsyncJsonWebsocketConsumer):
    """Websocket for tracking the progress of a benchmark.
    A user subscribes to notifications to a site as a single site can have
    multiple benchmarks.
    """

    async def connect(self):
        """Connect to the websocket."""
        user = self.scope['user']
        if user.is_anonymous:
            raise DenyConnection()

        site_id = self.scope['url_route']['kwargs']['site_id']

        await sync_to_async(self.get_site)(site_id, user)

        group_name = get_site_group_name(site_id)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect from the websocket."""
        site_id = self.scope['url_route']['kwargs']['site_id']
        group_name = get_site_group_name(site_id)
        await self.channel_layer.group_discard(
            group_name,
            self.channel_name
        )

    @classmethod
    def send_status_update(
        cls,
        site_id: int,
        benchmark_id: int,
        new_status: str,
        scheduled_on: _t.Optional[datetime.datetime] = None,
    ) -> None:
        """Send an update to the websocket.

        Args:
            site_id (int): The site id.
            benchmark_id (int): The benchmark id.
            new_status (str): The new status.
        """
        group_name = get_site_group_name(site_id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'benchmark_progress_update',
                'message': {
                    'benchmark_id': benchmark_id,
                    'status': new_status,
                    'scheduled_on': (
                        scheduled_on
                        and scheduled_on.strftime('%d-%m-%Y %H:%M')
                        or None
                    )

                }
            },
        )

    def get_site(self, site_id: int, user: User) -> site_models.Site:
        """Get the site for the user."""
        site = site_models.Site.objects.filter(
            id=site_id
        ).first()
        if not site:
            raise DenyConnection()
        if not site_models.SiteAccess.user_access(site, user):
            raise DenyConnection()
        return site

    async def benchmark_progress_update(self, event):
        """Handle an update from the benchmark."""
        message = event['message']
        await self.send_json({
            'benchmark_id': message['benchmark_id'],
            'status': message['status'],
            'scheduled_on': message['scheduled_on'],
        })
