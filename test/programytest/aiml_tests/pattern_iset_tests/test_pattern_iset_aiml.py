import unittest
import os

from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient


class BasicTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments):
        super(BasicTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].files.aiml_files._files=[os.path.dirname(__file__)]


class PatternISetAIMLTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(BasicTestClient(), "testid")
        self._client_context.bot = self._client_context.client.bot
        self._client_context.brain = self._client_context.bot.brain

    def test_patten_set_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS RED")
        self.assertEqual(response, "RED IS A NICE COLOR.")

        response = self._client_context.bot.ask_question(self._client_context,  "MY FAVORITE COLOR IS GREEN")
        self.assertEqual(response, "")

    def test_patten_set_one_or_more_wildcard_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "WHAT IS YOUR FAVOURITE COLOUR PLEASE")
        self.assertEqual(response, "My favourite colour is Red")

        response = self._client_context.bot.ask_question(self._client_context,  "WHAT IS YOUR FAVOURITE COLOR PLEASE")
        self.assertEqual(response, "My favourite color is Red")

    def test_patten_set_zero_or_more_wildcard_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE TO EAT BURGERS")
        self.assertEqual(response, "Wow, I like to eat burgers too.")

        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE TO MUNCH SUSHI")
        self.assertEqual(response, "Wow, I like to munch sushi too.")

        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE TO CHOW FRENCH FRIES")
        self.assertEqual(response, "Wow, I like to chow french fries too.")

    def test_patten_alternative_set_match(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I LIKE RIDING BMW MOTORCYCLES")
        self.assertEqual(response, "I prefer a Harley Davidson to a BMW")

    def test_united_kingdom(self):
        response = self._client_context.bot.ask_question(self._client_context,  "I live in wales")
        self.assertEqual(response, "Thats great, I live in the UK too!")

        response = self._client_context.bot.ask_question(self._client_context,  "I live in WALES")
        self.assertEqual(response, "Thats great, I live in the UK too!")

        response = self._client_context.bot.ask_question(self._client_context,  "I live in Wales")
        self.assertEqual(response, "Thats great, I live in the UK too!")
