from datetime import datetime, UTC
from abc import ABC
from typing import Optional
from lgt_jobs.lgt_common.lgt_logging import log
from lgt_jobs.lgt_common.slack_client.web_client import SlackWebClient
from lgt_jobs.lgt_data.mongo_repository import DedicatedBotRepository, UserContactsRepository
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob

"""
Send Slack Message
"""


class SendSlackMessageJobData(BaseBackgroundJobData, BaseModel):
    sender_id: str
    bot_id: str
    text: Optional[str]
    files_ids: Optional[list] = []


class SendSlackMessageJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SendSlackMessageJobData

    def exec(self, data: SendSlackMessageJobData):
        bot = DedicatedBotRepository().get_one(id=data.bot_id)
        if not bot:
            return

        user_contacts_repository = UserContactsRepository()
        uc = user_contacts_repository.find_one(bot.user_id, sender_id=data.sender_id,
                                               source_id=bot.source.source_id)
        uc.scheduled_messages = [message.to_dic() for message in uc.scheduled_messages
                                 if message.post_at.replace(tzinfo=UTC) > datetime.now(UTC)]
        user_contacts_repository.update(bot.user_id, uc.sender_id, bot.source.source_id,
                                        scheduled_messages=uc.scheduled_messages)
        slack_client = SlackWebClient(bot.token, bot.cookies)
        resp = slack_client.im_open(data.sender_id)
        if not resp['ok']:
            log.warning(f"Unable to open im with user: {resp}")
            return

        channel_id = resp['channel']['id']
        if data.files_ids:
            slack_client.share_files(data.files_ids, channel_id, data.text)
        else:
            slack_client.post_message(channel_id, data.text)
