import os
import logging
import sys

import openai
from dotenv import load_dotenv
from llama_index import (
    SimpleDirectoryReader,
    GPTVectorStoreIndex,
    StorageContext,
    LLMPredictor,
    LangchainEmbedding,
    PromptHelper,
    ServiceContext,
    load_index_from_storage,
)
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceEmbeddings

LOG_LEVEL = logging.INFO

def setup():
  # OpenAIのAPIキーを設定
  load_dotenv()
  openai.api_key = os.environ.get("OPENAI_API_KEY")

  # ログの設定
  logging.basicConfig(stream=sys.stdout, level=LOG_LEVEL, force=True)

# インデックスを読み込む
def load_index():
  try:
    logging.info("Loading index...")
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    return load_index_from_storage(storage_context)
  except FileNotFoundError:
    logging.info("Index not found.")
    return None


# インデックスを作成して保存する
def create_index():
  # PromptHelperの準備
  prompt_helper=PromptHelper(
    context_window=4096, # LLM入力の最大トークン数
  )

  # 埋め込みモデルの準備
  # embed_model = LangchainEmbedding(HuggingFaceEmbeddings(
  #   model_name="oshizo/sbert-jsnli-luke-japanese-base-lite"
  # ))

  # LLMPredictorの準備
  llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.7,
    model_name="gpt-3.5-turbo-0613",
  ))

  # ServiceContextの準備
  service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor,
    # embed_model=embed_model,
    prompt_helper=prompt_helper,
  )

  logging.info("Loading documents...")
  documents = SimpleDirectoryReader("./docs").load_data()
  logging.info("Creating index...")
  index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
  index.storage_context.persist()

  return index

def main():
  setup()

  index = load_index()
  if index is None:
    index = create_index()

  # インデックスを使って検索する
  query_engine = index.as_query_engine()
  query = "unkown型とany型の違いを教えてください。"
  response = query_engine.query(query)

  print(f"質問:\n{query}\n")
  print(f"回答:\n{response}\n")

main()
