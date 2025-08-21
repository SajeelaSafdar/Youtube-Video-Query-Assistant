from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from deep_translator import MyMemoryTranslator
from googletrans import Translator
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.schema.runnable import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
import os

load_dotenv()
llm = HuggingFaceEndpoint(
    repo_id="openai/gpt-oss-120b",
    task = 'text-generation'
)
model  = ChatHuggingFace(llm=llm)

def load_transcript(vid):
    api = YouTubeTranscriptApi()
    transcripts = api.list(video_id=vid)
    try:
        transcript = transcripts.find_transcript(['en'])
        text = " ".join([t.text for t in transcript.fetch()])
        return text
    except:
        transcript = list(transcripts)[0]
        transcript_text = " ".join([t.text for t in transcript.fetch()])
        chunks = [transcript_text[i:i + 4000] for i in range(0, len(transcript_text), 4000)]
        translated_chunks = []
        for chunk in chunks:
            translator = Translator()
            translated_chunk = translator.translate(chunk, src="auto", dest="en").text
            translated_chunks.append(translated_chunk)
        return "".join(translated_chunks)
def format_docs(documents):
    context_text = "".join(doc.page_content for doc in documents)
    return context_text

def get_response(transcript, question):
    # ii- text splitting
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    chunks = splitter.split_text(transcript)

    # iii-create embeddings and store in vector store
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_texts(chunks, embeddings)
    ids = vectorstore.index_to_docstore_id

    # create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        template="You are a helpful assistant. Provide reasonable and detailed answers only from the provided transcript context.If you do not know the answer just say I dont know. The context is \n {context} \n and the question is\n {question}",
        input_variables=['context', 'question']
    )
    parser = StrOutputParser()


    parallel_chain = RunnableParallel({
        'context' : retriever | RunnableLambda(format_docs),
        'question' : RunnablePassthrough()
    })
    main_chain = parallel_chain | prompt | model | parser
    return main_chain.invoke(question)





