from zshgpt.util.chat_util import model_selection


def test_chatgpt4_with_double_hash():
    assert model_selection('## Please help') == 'gpt-4'


def test_chatgpt3_with_hash():
    assert model_selection('# Please help') == 'gpt-3.5-turbo'
