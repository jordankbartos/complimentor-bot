# ------------------------------------------------------------------------------
# Author: Jordan K Bartos
# Description: A class that manages and generates compliments for a slackbot
# ------------------------------------------------------------------------------
import requests
import re
import random

class Complimentor:
    def __init__(self, slack_client):
        self.slack_client = slack_client

        # load the adverbs
        self.adverbs = []
        with open("adverbs.txt", 'r') as adv_file:
            for line in adv_file:
                self.adverbs.append(line.rstrip())
        
        # load the adj_1s
        self.adjectives = []
        with open("adjectives.txt", 'r') as adj_file:
            for line in adj_file:
                self.adjectives.append(line.rstrip())

        # load the nouns
        self.nouns = []
        with open("nouns.txt", 'r') as noun_file:
            for line in noun_file:
                self.nouns.append(line.rstrip())

        
        # load the users from the slack channel
        users = slack_client.api_call("users.list")
        self.names = []

        for i in range(0, len(users["members"])):
            if users["members"][i]["is_bot"] == False and \
               users["members"][i]["id"] != "USLACKBOT":
                self.names.append(users["members"][i]["real_name"])

    def generate_compliment(self, command):
        # get a random name, adverb, two adjectives, and a noun
        if command == "compliment":
            name = self.names[random.randint(0, len(self.names) - 1)]
        else:
            name = command.replace('compliment','',65535)

        adverb = self.adverbs[random.randint(0, len(self.adverbs) - 1)]
        adj_one = self.adjectives[random.randint(0, len(self.adjectives) - 1)]
        adj_two = self.adjectives[random.randint(0, len(self.adjectives) - 1)]
        noun = self.nouns[random.randint(0, len(self.nouns) - 1)]
        # get two different adjectives from the adjectives list
        while adj_one == adj_two:
            adj_two = self.adjectives[random.randint(0, len(self.adjectives) - 1)]

        # return formatted response
        return name + " is " + adverb + " " + adj_one + ", " + adj_two + " " + noun + "."


    def get_noun(self):
        return self.nouns[random.randint(0, len(self.nouns) - 1)]
