from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class WebRAG:
    def __init__(self):
        self.vectorstore = None
        self.rag_chain = None
        
    def load_website(self, url):
        # Load and process website
        loader = WebBaseLoader(web_path=url)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        splits = text_splitter.split_documents(docs)
        
        # Create vector store
        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=OpenAIEmbeddings()
        )
        
        # Build RAG chain
        retriever = self.vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")
        llm = ChatOpenAI()
        
        self.rag_chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()} 
            | prompt
            | llm
            | StrOutputParser()
        )
        
    def _format_docs(self, docs):
        return "\n".join(doc.page_content for doc in docs)
    
    def ask(self, question):
        if not self.rag_chain:
            return "Please load a website first!"
        return self.rag_chain.invoke(question)