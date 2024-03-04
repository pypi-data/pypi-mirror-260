import unittest
from intelli.function.chatbot import Chatbot
from intelli.model.input.chatbot_input import ChatModelInput
import os
from dotenv import load_dotenv
load_dotenv()

class TestOpenAIWrapper(unittest.TestCase):

    def setUp(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.one_key = os.getenv('CUSTOM_ONE')
        
    def test_multiple_choice(self):
        
        result = gen_10q(self.api_key, self.one_key, "Power supply systems")
        
        print('the model response: \n', result)
        
        self.assertTrue(len(result) > 0, "The result is empty")


def gen_10q(api, one, subject):
    # Creating chatbot with the intellinode one key:
    bot = Chatbot(api, "openai", {"one_key": one})

    input = ChatModelInput("Generate 10 multiple choice questions from the context.", "gpt-4-turbo-preview")
    input.add_user_message(f"Generate 10 multiple choice questions about {subject} from the context, and let me know the correct choice for each.")

    # Optional to return the searched file name:
    input.attach_reference = True

    response = bot.chat(input)
    print(f"Reference used: {response['references']}")
    return response['result'][0]



if __name__ == "__main__":
    unittest.main()