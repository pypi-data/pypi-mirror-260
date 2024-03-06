import chromadb
from chromadb.utils import embedding_functions
from dotenv import find_dotenv, load_dotenv

from instrumentation.setup import setup_instrumentation
from instrumentation.with_root_span import with_langtrace_root_span

_ = load_dotenv(find_dotenv())

setup_instrumentation()


@with_langtrace_root_span()
def basic():
    chroma_client = chromadb.Client()
    embedder = embedding_functions.DefaultEmbeddingFunction()
    collection = chroma_client.create_collection(
        name="my6_collection", embedding_function=embedder)
    collection.add(
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )
    results = collection.query(
        query_texts=["This is a query document"],
        n_results=2
    )
