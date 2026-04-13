import glob
import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader

from utils.constants import ACCEPTED_FILE_PATH


def load_files(file_dir_path, accepted_extensions=ACCEPTED_FILE_PATH):
    folders = glob.glob(str(file_dir_path / "*"))

    documents = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder, glob=accepted_extensions, loader_cls=TextLoader,
                                 loader_kwargs={'encoding': 'utf-8'})
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)

    print(f"Loaded {len(documents)} documents")
    return documents
