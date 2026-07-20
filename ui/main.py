import streamlit as st

from app.data.embeddings.sentence_transformer import SentenceTransformerEmbedder
from app.models.domain.query import Query
from app.retrieval.search.semantic import SemanticRetriever
from app.retrieval.vectorstores.chroma import ChromaVectorStore
from app.ai.generation.groq import GroqGenerator
from app.ai.prompts.builder import PromptBuilder
from app.ai.generation.pipeline import RAGPipeline
from app.ai.generation.exception import InvalidLLMResponseError

st.set_page_config(

    page_title="Rishi AI",
    page_icon="🕉",
    layout="wide",

)

@st.cache_resource
def load_pipeline():

    embedder = SentenceTransformerEmbedder()
    vector_store = ChromaVectorStore()

    retriever = SemanticRetriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    generator = GroqGenerator()

    prompt_builder = PromptBuilder()

    corpus_registry = None

    return RAGPipeline(
        retriever=retriever,
        generator=generator,
        prompt_builder=prompt_builder,
        corpus_registry=corpus_registry,
    )

st.title("🕉 Rishi AI")
st.caption("Search the Vedic Knowledge Base")

query_text = st.text_input(
    "Ask a question",
    placeholder="What is Rishi?"
)

top_k = st.slider(
    "Top K Results",
    1,
    5,
    10,
)

pipeline = load_pipeline()

if st.button("Search"):

    if not query_text.strip():

        st.warning("Please write a question")
        st.stop()

    try:
        
        with st.spinner("Searching..."):

            answer = pipeline.answer(
                question=query_text,
                top_k=top_k,
            )
        
    except InvalidLLMResponseError as e:

        st.error(str(e))
        st.stop()

    except Exception as e:

        st.exception(e)
        st.stop()

    st.header("Answer")

    st.markdown(answer.direct_answer)

    with st.expander("Explanation"):

        st.write(answer.explanation)

    st.metric(
        "Confidence",
        f"{answer.confidence:.2%}",
    )

    st.divider()

    st.subheader("Sources")

    for result in answer.retrieved_results:

        with st.expander(

            f"{result.document_id} ({result.score:.4f})"
        
        ):
            
            st.write(result.text)