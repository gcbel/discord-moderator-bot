# bot.py
import discord
from discord.ext import commands
import os
import json
import logging
import re
import requests
from report import Report
from report_mod import Report_Mod
import pdb

# Set up logging to the console
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# There should be a file called 'tokens.json' inside the same folder as this file
token_path = 'tokens.json'
if not os.path.isfile(token_path):
    raise Exception(f"{token_path} not found!")
with open(token_path) as f:
    # If you get an error here, it means your token is formatted incorrectly. Did you put it in quotes?
    tokens = json.load(f)
    discord_token = tokens['discord']

class ModBot(discord.Client):
    def __init__(self): 
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='.', intents=intents)
        self.group_num = None
        self.mod_channels = {} # Map from guild to the mod channel id for that guild
        self.reports = {} # Map from user IDs to the state of their report
        self.mod_reports = {} # Map from mod IDs to the state of their report
        self.saved_report_history = {} # Map from user IDs to their saved report history
        self.counter = 0 # Counter for reports to have unique IDs
        self.mod_channel = None
        # Check if reports data file exists
        if os.path.isfile("saved_report_history.json"):
            with open("saved_report_history.json", "r") as json_file:
                json_data = json.load(json_file)
                self.counter = json_data["counter"]
                self.saved_report_history = json_data["user_reports"]
        else:
            initial_data = {
                "counter": 0,
                "user_reports": {}
            }
            with open("saved_report_history.json", "w") as json_file:
                json.dump(initial_data, json_file)
            self.counter = initial_data["counter"]
            self.saved_report_history = initial_data["user_reports"]   


    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord! It is these guilds:')
        for guild in self.guilds:
            print(f' - {guild.name}')
        print('Press Ctrl-C to quit.')

        # Parse the group number out of the bot's name
        match = re.search('[gG]roup (\d+) [bB]ot', self.user.name)
        if match:
            self.group_num = match.group(1)
        else:
            raise Exception("Group number not found in bot's name. Name format should be \"Group # Bot\".")

        # Find the mod channel in each guild that this bot should report to
        for guild in self.guilds:
            for channel in guild.text_channels:
                if channel.name == f'group-{self.group_num}-mod':
                    self.mod_channels[guild.id] = channel
                    self.mod_channel = channel
        

    async def on_message(self, message):
        '''
        This function is called whenever a message is sent in a channel that the bot can see (including DMs). 
        Currently the bot is configured to only handle messages that are sent over DMs or in your group's "group-#" channel. 
        '''
        # Ignore messages from the bot 
        if message.author.id == self.user.id:
            return

        # Check if this message was sent in a server ("guild") or if it's a DM
        if message.guild:
            # Forward mod messages to mod channel
            if message.channel.name == f'group-{self.group_num}-mod':
                await self.handle_mod_channel_message_reply(message)
            else:
                await self.handle_channel_message(message)
        else:
            await self.handle_dm(message)

    async def handle_dm(self, message):
        # Handle a help message
        if message.content == Report.HELP_KEYWORD:
            reply =  "Use the `report` command to begin the reporting process.\n"
            reply += "Use the `cancel` command to cancel the report process.\n"
            await message.channel.send(reply)
            return

        author_id = message.author.id
        responses = []

        # Only respond to messages if they're part of a reporting flow
        if author_id not in self.reports and not message.content.startswith(Report.START_KEYWORD):
            return

        # If we don't currently have an active report for this user, add one
        if author_id not in self.reports:
            self.reports[author_id] = Report(self)

        # Let the report class handle this message; forward all the messages it returns to us
        responses = await self.reports[author_id].handle_message(message)
        for r in responses:
            await message.channel.send(r)

        # If the report is complete or cancelled, remove it from our map
        if author_id in self.reports and self.reports[author_id].report_complete():
            # Get report details
            report_details = self.reports[author_id].get_details()
            # Remove
            self.reports.pop(author_id)
            # Add unqiue ID
            report_details["ID"] = self.counter
            self.counter += 1
            # Formart report details
            report_details_formatted = "\n".join([f"{i}:   *{j}*" for i, j in report_details.items()])
            # Send report to mod channel
            await self.mod_channel.send(f"🚨__**Reported Message:**__🚨\n{report_details_formatted}")

            # Save report to JSON file
            # Check if individual has a saved report history (they have been reported before)
            reported_user = report_details["Reported user"]
            if reported_user not in self.saved_report_history:
                self.saved_report_history[reported_user] = []
            # Append report to user's report history
            self.saved_report_history[reported_user].append(report_details)
            # Save data to JSON file
            data_to_save = {
                "counter": self.counter,
                "user_reports": self.saved_report_history
            }
            with open("saved_report_history.json", "w") as json_file:
                json.dump(data_to_save, json_file, indent=4)


    async def handle_mod_channel_message_reply(self, message):
        # if not message.reference:
        # See if 
        if message.content == Report_Mod.HELP_KEYWORD:
            reply =  "Use the `start` command to begin the evaluation/priority process.\n"
            reply += "Use the `cancel` command to cancel the evaluation/priority process.\n"
            await message.reply(reply)
            return

        author_id = message.author.id
        responses = []

        # Only respond to messages if they're part of a reporting flow
        if author_id not in self.mod_reports and not message.content.startswith(Report_Mod.START_KEYWORD):
            return

        # If we don't currently have an active report for this user, add one
        if author_id not in self.mod_reports:
            self.mod_reports[author_id] = Report_Mod(self)

        # Let the report class handle this message; forward all the messages it returns to us
        responses = await self.mod_reports[author_id].handle_message(message)
        for r in responses:
            await message.channel.send(r)

        # If the report is complete or cancelled, remove it from our map
        if author_id in self.mod_reports and self.mod_reports[author_id].report_complete():
            # Close report
            self.mod_reports[author_id].close_report()

            # Remove
            self.mod_reports.pop(author_id)


    async def handle_channel_message(self, message):
        # Only handle messages sent in the "group-#" channel
        if not message.channel.name == f'group-{self.group_num}':
            return

        # Forward the message to the mod channel
        mod_channel = self.mod_channels[message.guild.id]
        print(f"****{type(mod_channel)}****")
        await mod_channel.send(f'Forwarded message:\n{message.author.name}: "{message.content}"')
        scores = self.eval_text(message.content)
        await mod_channel.send(self.code_format(scores))

    
    def eval_text(self, message):
        ''''
        TODO: Once you know how you want to evaluate messages in your channel, 
        insert your code here! This will primarily be used in Milestone 3. 
        '''
        return message

    
    def code_format(self, text):
        ''''
        TODO: Once you know how you want to show that a message has been 
        evaluated, insert your code here for formatting the string to be 
        shown in the mod channel. 
        '''
        return "Evaluated: '" + text+ "'"


    def forward_user_report(self, report):
        '''
        This function is called by the Report class when it has collected all the necessary information and is ready to send it to the mod channel. 
        '''
        pass

        
client = ModBot()
client.run(discord_token)