from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter, NLTKTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP_SIZE = 200

class TextSplitterFactory:
    def __init__(self,text_splitter_type):
        self.text_splitter_type = text_splitter_type
    def get_text_splitter(self,CHUNK_SIZE=CHUNK_SIZE):
        print("chunk size ----",CHUNK_SIZE)
        if self.text_splitter_type=="character":
            return CharacterTextSplitter(
                separator='\n',
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP_SIZE,
            )
        elif self.text_splitter_type=="recursive":
            return RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP_SIZE,
            )
        elif self.text_splitter_type=="nltk":
            return NLTKTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP_SIZE)
