import random
from telethon.sync import TelegramClient
from telethon.tl.types import Chat

class TelegramForwarder:
    def __init__(self, session_name, api_id, api_hash, config):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.client.start()
        self.config = config
        self.channel = self.client.get_entity(self.config['ChannelID'])
        self.messages = self.client.get_messages(entity=self.channel, limit=self.config['MessagesLimit'])

        all_dialogs = self.client.get_dialogs()
        chat_entities = [d.entity for d in all_dialogs if isinstance(d.entity, Chat)]
        specific_chat_entities = [e for e in chat_entities if e.title in self.config['ChatList']]
        self.entities = [e.migrated_to or e for e in specific_chat_entities]

    def get_sample_messages(self):
        if self.config['IsPostNumberRandom']:
            sample_length = random.randint(
                self.config['RandomPostNumberMin'],
                self.config['RandomPostNumberMax']
            )                
        else:
            sample_length = self.config['ConstantPostNumber']
            
        sample_length = min(sample_length, len(self.messages))
        sample_messages = random.sample(self.messages, sample_length)
        
        if self.config['MediaOnly']:
            while True:
                sample_messages = [message for message in sample_messages if message.media is not None]
                if len(sample_messages) == sample_length:
                    break
        
        return sample_messages

    def forward_messages(self):
        for entity in self.entities:
            self.client.forward_messages(entity, self.get_sample_messages())                
