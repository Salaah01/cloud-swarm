import typing as _t
from datetime import datetime
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import (
    AsyncJsonWebsocketConsumer,
    DenyConnection
)
from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from sites import models as site_models
from accounts import models as account_models


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
        account = await self.get_account()

        site_id = self.scope['url_route']['kwargs']['site_id']
        await sync_to_async(self.get_site)(site_id, account)

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
        status: str,
        num_servers: int,
        num_requests: int,
        completed_requests: int,
        failed_requests: int,
        created_on: _t.Optional[datetime] = None,
        scheduled_on: _t.Optional[datetime] = None,
        min_time: _t.Optional[int] = None,
        mean_time: _t.Optional[int] = None,
        max_time: _t.Optional[int] = None,
    ) -> None:
        """Send an update to the websocket.

        Args:
            site_id (int): The site id.
            benchmark_id (int): The benchmark id.
            status (str): The new status.
            num_servers (int): The number of servers.
            num_requests (int): The number of requests per server.
            completed_requests (int): The number of completed requests.
            failed_requests (int): The number of failed requests.
            created_on (datetime): The time the benchmark was created.
            scheduled_on (datetime): The time the benchmark was scheduled.
            min_time (int): The minimum time in milliseconds.
            mean_time (int): The mean time in milliseconds.
            max_time (int): The maximum time in milliseconds.
        """
        group_name = get_site_group_name(site_id)
        channel_layer = get_channel_layer()
        datetime_fmt = '%d-%m-%Y %H:%M'
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'benchmark_progress_update',
                'message': {
                    'benchmark_id': benchmark_id,
                    'status': status,
                    'num_servers': num_servers,
                    'num_requests': num_requests,
                    'completed_requests': completed_requests,
                    'failed_requests': failed_requests,
                    'created_on': created_on.strftime(datetime_fmt),
                    'scheduled_on': (
                        scheduled_on
                        and scheduled_on.strftime(datetime_fmt)
                        or None
                    ),
                    'min_time': min_time,
                    'mean_time': mean_time,
                    'max_time': max_time,
                }
            },
        )

    @database_sync_to_async
    def get_site(
        self,
        site_id: int,
        account: account_models.Account
    ) -> site_models.Site:
        """Get the site for the account."""
        site = site_models.Site.objects.filter(
            id=site_id
        ).first()
        if not site:
            raise DenyConnection()
        if not site_models.SiteAccess.account_access(
            site,
            account_models.Account
        ):
            raise DenyConnection()
        return site

    @database_sync_to_async
    def get_account(self) -> account_models.Account:
        """Get the account for the user."""
        user_id = self.scope['user'].id
        if user_id is None:
            raise DenyConnection()

        account = account_models.Account.objects.filter(
            user_id=user_id).first()
        if not account:
            raise DenyConnection()

        return account

    async def benchmark_progress_update(self, event):
        """Handle an update from the benchmark."""
        message = event['message']
        await self.send_json({
            'benchmark_id': message['benchmark_id'],
            'status': message['status'],
            'num_servers': message['num_servers'],
            'num_requests': message['num_requests'],
            'completed_requests': message['completed_requests'],
            'failed_requests': message['failed_requests'],
            'created_on': message['created_on'],
            'scheduled_on': message['scheduled_on'],
            'min_time': message['min_time'],
            'mean_time': message['mean_time'],
            'max_time': message['max_time'],
        })
