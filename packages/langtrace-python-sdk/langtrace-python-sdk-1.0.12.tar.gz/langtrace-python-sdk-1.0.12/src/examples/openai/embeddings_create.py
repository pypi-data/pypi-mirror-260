from dotenv import find_dotenv, load_dotenv
from init import init
from openai import OpenAI

from utils.with_root_span import with_langtrace_root_span


_ = load_dotenv(find_dotenv())

init()
client = OpenAI()


@with_langtrace_root_span()
def embeddings_create():
    result = client.embeddings.create(
        model="text-embedding-ada-002",
        input="Once upon a time, there was a frog.",
    )
