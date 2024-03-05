# Copyright (c) 2023 Artem Rozumenko
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import importlib

from typing import Optional

from langchain_core.documents import Document
from langchain.schema import HumanMessage
from json import dumps, loads

from .interfaces.loaders import loader
from .interfaces.kwextractor import KWextractor
from .interfaces.splitters import Splitter
from .interfaces.llm_processor import get_embeddings, summarize, get_model, get_vectorstore, add_documents, generateResponse
from .tools.utils import unpack_json, download_nltk, replace_source
from .tools.log import print_log
from .retrievers.AnalystaRetriever import AnalystaRetriever

download_nltk("./nltk_data", force=False)


def main(
        dataset: str,
        library:str,
        loader_name: str,
        loader_params: dict,
        load_params: Optional[dict],
        embedding_model: str,
        embedding_model_params: dict,
        kw_plan: Optional[str],
        kw_args: Optional[dict],
        splitter_name: Optional[str] = 'chunks',
        splitter_params: Optional[dict] = {},
        document_processing_prompt: Optional[str] = None,
        chunk_processing_prompt: Optional[str] = None,
        ai_model: Optional[str] = None,
        ai_model_params: Optional[dict] = {},
        vectorstore: Optional[str] = None,
        vectorstore_params: Optional[dict] = {},
        source_replacers: Optional[dict] = {},
        document_debug=False,
):
    #
    # Logic is the following:
    # 1. Loader and its params to get data
    # 2. Keyword extractor and its params to get keywords (for the whole file)
    # 3. Splitter and its params to split data (here we may need to use different ar)
    # 4. Keyword extractor and its params to get keywords (for the splitted data)
    # 5. Embedder and its params to get embeddings (for the splitted data)
    #
    embedding = get_embeddings(embedding_model, embedding_model_params)
    vectorstore = get_vectorstore(vectorstore, vectorstore_params, embedding_func=embedding)
    kw_extractor = KWextractor(kw_plan, kw_args)
    llmodel = get_model(ai_model, ai_model_params)
    #
    og_keywords_set_for_source = set()
    #
    for document in loader(loader_name, loader_params, load_params):
        replace_source(document, source_replacers)
        #
        # Add: two records/placeholders here - summary + keywords
        if document_processing_prompt:
            document = summarize(llmodel, document, document_processing_prompt)
            print_log("Summary: ", document.metadata.get('document_summary', ''))
            #
            try:
                document_summary = unpack_json(document.metadata.get('document_summary', ''))
                document.metadata['keywords'] = document_summary.get('keywords', [])
                document.metadata['document_summary'] = document_summary.get('description', '')
            except:
                print_log(
                    "Failed to unpack document summary",
                    document.metadata.get('document_summary', '')
                )
        #
        if kw_extractor.extractor:
            if len(document.metadata.get('keywords', [])) == 0 and \
                    len(document.page_content) > 1000:
                #
                document.metadata['keywords'] = kw_extractor.extract_keywords(
                    document.metadata.get('document_summary', '') + '\n' + document.page_content
                )
                print_log("Keywords: ", document.metadata['keywords'])
        #
        splitter = Splitter(**splitter_params)
        for index, document in enumerate(splitter.split(document, splitter_name)):
            print_log("Chunk: ", document.page_content)
            #
            if chunk_processing_prompt:
                document = summarize(
                    llmodel, document, chunk_processing_prompt,
                    metadata_key='chunk_summary',
                )
                if splitter_params.get('kw_for_chunks') and \
                        kw_extractor.extractor and document.metadata.get('chunk_summary'):
                    #
                    chunk_keywords = kw_extractor.extract_keywords(
                        document.metadata.get('chunk_summary', '') + '\n' + document.page_content
                    )
                    if chunk_keywords:
                        document.metadata['keywords'] = list(
                            set(document.metadata['keywords']).union(chunk_keywords)
                        )
                        # Change to: document.metadata['keywords'] = list(chunk_keywords)  # but not to metadata
            #
            _documents = []
            #
            if document.metadata.get('keywords'):
                _documents.append(
                    Document(
                        page_content=', '.join(document.metadata['keywords']),
                        metadata={
                            'source': document.metadata['source'],
                            'type': 'keywords',
                            'library': library,
                            'source_type': loader_name,
                            'dataset': dataset,
                        }
                    )
                )
            #
            if document.metadata.get('document_summary'):
                _documents.append(
                    Document(
                        page_content=document.metadata['document_summary'],
                        metadata={
                            'source': document.metadata['source'],
                            'type': 'document_summary',
                            'library': library,
                            'source_type': loader_name,
                            'dataset': dataset,
                        }
                    )
                )
            #
            # og_data is only set by TableLoader
            #
            if document.metadata.get('og_data'):
                _documents.append(
                    Document(
                        page_content=document.page_content,
                        metadata={
                            'source': document.metadata['source'],
                            'type': 'cleansed_data',
                            'library': library,
                            'source_type': loader_name,
                            'dataset': dataset,
                        }
                    )
                )
                _documents.append(
                    Document(
                        page_content=document.metadata['og_data'],
                        metadata={
                            'source': document.metadata['source'],
                            'type': 'data',
                            'library': library,
                            'source_type': loader_name,
                            'dataset': dataset,
                            'chunk_index': -1,
                        }
                    )
                )
                # Only save columns (=file keywords) once per source
                if document.metadata['table_source'] not in og_keywords_set_for_source:
                    og_keywords_set_for_source.add(document.metadata['table_source'])
                    _documents.append(
                        Document(
                            page_content=', '.join(document.metadata['columns']),
                            metadata={
                                'source': document.metadata['table_source'],
                                'type': 'keywords',
                                'library': library,
                                'source_type': loader_name,
                                'dataset': dataset,
                            }
                        )
                    )
            #
            elif document.metadata.get('chunk_summary'):
                _documents.append(
                    Document(
                        page_content=document.metadata['chunk_summary'] + '\n\n' + \
                                document.page_content,
                        metadata={
                            'source': document.metadata['source'],
                            'type': 'data',
                            'library': library,
                            'source_type': loader_name,
                            'dataset': dataset,
                            'chunk_index': index,
                        }
                    )
                )
            #
            else:
                _documents.append(
                    Document(
                        page_content=document.page_content,
                        metadata={
                            'source': document.metadata['source'],
                            'type': 'data',
                            'library': library,
                            'source_type': loader_name,
                            'dataset': dataset,
                            'chunk_index': index,
                        }
                    )
                )
            #
            if document_debug:
                print_log(_documents)
            #
            add_documents(vectorstore=vectorstore, documents=_documents)
        #
        vectorstore.persist()
    #
    return 0


def index(
        dataset: str,
        library:str,
        loader_name: str,
        loader_params: dict,
        load_params: Optional[dict],
        embedding_model: str,
        embedding_model_params: dict,
        kw_plan: Optional[str],
        kw_args: Optional[dict],
        splitter_name: Optional[str] = 'chunks',
        splitter_params: Optional[dict] = {},
        document_processing_prompt: Optional[str] = None,
        chunk_processing_prompt: Optional[str] = None,
        ai_model: Optional[str] = None,
        ai_model_params: Optional[dict] = {},
        vectorstore: Optional[str] = None,
        vectorstore_params: Optional[dict] = {},
        source_replacers: Optional[dict] = {},
        document_debug=False,
):
    return main(
        dataset=dataset,
        library=library,
        loader_name=loader_name,
        loader_params=loader_params,
        load_params=load_params,
        embedding_model=embedding_model,
        embedding_model_params=embedding_model_params,
        kw_plan=kw_plan,
        kw_args=kw_args,
        splitter_name=splitter_name,
        splitter_params=splitter_params,
        document_processing_prompt=document_processing_prompt,
        chunk_processing_prompt=chunk_processing_prompt,
        ai_model=ai_model,
        ai_model_params=ai_model_params,
        vectorstore=vectorstore,
        vectorstore_params=vectorstore_params,
        source_replacers=source_replacers,
        document_debug=document_debug,
    )


def search(
        chat_history=[],
        str_content=True,
        embedding_model=None,
        embedding_model_params=None,
        vectorstore=None,
        vectorstore_params=None,
        collection=None,
        top_k=5,
        weights=None,
        page_top_k=1,
        fetch_k=10,
        lower_score_better=True,
        retriever=None,
        document_debug=False,
):
    """ Search for documents based on chat history

    Args:
        chat_history (list): List of chat messages [HumanMessage(content="What I want to search for")]
        str_content (bool): Return documents in response
        embedding_model (str): Embedding model name
        embedding_model_params (dict): Embedding model parameters
        vectorstore (str): Vectorstore name
        vectorstore_params (dict): Vectorstore parameters
        collection (str): Collection name
        top_k (int): Number of top documents to return
        weights (dict): Weights for RAG retriever

    Returns:
        str: Documents content
        set: References
    """
    vectorstore_params['collection_name'] = collection
    embedding = get_embeddings(embedding_model, embedding_model_params)
    vs = get_vectorstore(vectorstore, vectorstore_params, embedding_func=embedding)
    #
    if retriever is None:
        retriever_cls = AnalystaRetriever
    else:
        retriever_pkg, retriever_name = retriever.rsplit(".", 1)
        retriever_cls = getattr(
            importlib.import_module(retriever_pkg),
            retriever_name
        )
    #
    retriever_obj = retriever_cls(
        vectorstore=vs,
        doc_library=collection,
        top_k=top_k,
        page_top_k=page_top_k,
        fetch_k=fetch_k,
        lower_score_better=lower_score_better,
        document_debug=document_debug,
        weights=weights,
    )
    #
    docs = retriever_obj.invoke(chat_history[-1].content)
    #
    references = set()
    docs_content = ""
    #
    for doc in docs[:top_k]:
        docs_content += f'{doc.page_content}\n\n'
        references.add(doc.metadata["source"])
    #
    if str_content:
        return docs_content, references
    #
    return docs, references


def predict(
        chat_history=[],
        guidance_message=None,
        context_message=None,
        collection=None,
        top_k=5,
        ai_model=None,
        ai_model_params=None,
        embedding_model=None,
        embedding_model_params=None,
        vectorstore=None,
        vectorstore_params=None,
        weights=None,
        page_top_k=1,
        fetch_k=10,
        lower_score_better=True,
        retriever=None,
        document_debug=False,
        stream=False,
):
    """ Generate prediction based on chat history and results of RAG search

    Args:
        chat_history (list): List of chat messages (Langchain style messages)
        guidance_message (str): Guidance message (Optional message to be added as a divider for search results and context)
        context_message (str): Context message (Optional message to be added as a context of query, exaplaining the structure of message including results of search)
        collection (str): Collection name
        top_k (int): Number of top documents to return
        ai_model (str): AI model name
        ai_model_params (dict): AI model parameters
        embedding_model (str): Embedding model name
        embedding_model_params (dict): Embedding model parameters
        vectorstore (str): Vectorstore name
        vectorstore_params (dict): Vectorstore parameters
        weights (dict): Weights for RAG retriever
        stream (bool): Stream response

    Returns:
        str: Generated response
        set: References to documents
    """
    context, references = search(
        chat_history=chat_history,
        str_content=True,
        embedding_model=embedding_model,
        embedding_model_params=embedding_model_params,
        vectorstore=vectorstore,
        vectorstore_params=vectorstore_params,
        collection=collection,
        top_k=top_k,
        weights=weights,
        page_top_k=page_top_k,
        fetch_k=fetch_k,
        lower_score_better=lower_score_better,
        retriever=retriever,
        document_debug=document_debug,
    )
    #
    messages = []
    #
    if len(chat_history) > 1:
        for message in chat_history[:-1]:
            messages.append(message)
    #
    if context_message:
        messages.append(HumanMessage(content=context_message))
    #
    if guidance_message:
        context = f'{guidance_message}\n\n{context}'
    #
    messages.append(HumanMessage(content=context))
    messages.append(chat_history[-1])
    #
    ai = get_model(ai_model, ai_model_params)
    if stream:
        return {
            "response_iterator": ai.stream(messages),
            "references": references
        }
    #
    response_text = ai(messages).content
    return {
        "response": response_text,
        "references": references
    }
