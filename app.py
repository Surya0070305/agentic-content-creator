import asyncio
import uuid

import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph.types import Command

MAX_REVISIONS = 5
FAITHFULNESS_THRESHOLD = 0.8
SERVICE_DOWN_MSG = (
    "Content service unavailable. No draft was produced. "
    "The content server might be down, so please try again in a moment."
)

st.set_page_config(page_title="Content Creator", page_icon="✍️", layout="wide")


@st.cache_resource
def load_graph():
    from LangGraph.routing_graph import graph
    return graph


graph = load_graph()


def run_graph(graph_input):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    return asyncio.run(graph.ainvoke(graph_input, config=config))


def handle_result(result):
    st.session_state.state = result
    interrupts = result.get("__interrupt__")
    if interrupts:
        st.session_state.stage = "review"
        st.session_state.payload = interrupts[0].value
    else:
        st.session_state.stage = "done"
        st.session_state.payload = None


def reset():
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.stage = "input"
    st.session_state.payload = None
    st.session_state.state = None


def safe_run(graph_input, spinner_text):
    with st.spinner(spinner_text):
        try:
            handle_result(run_graph(graph_input))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()
    st.rerun()


def new_request_button():
    if st.button("Start a new request", type="primary"):
        reset()
        st.rerun()


if "thread_id" not in st.session_state:
    reset()

st.title("Content Creator")
st.caption("Researched blog posts and LinkedIn posts, with you approving every draft.")

stage = st.session_state.stage

# Screen 1: the request
if stage == "input":
    request = st.text_area(
        "What should I write?",
        placeholder="Write a blog post about electric vehicles in Indian cities",
        height=120,
    )
    if st.button("Generate", type="primary"):
        if not request.strip():
            st.warning("Please type a request first.")
        else:
            safe_run(
                {"messages": [HumanMessage(content=request.strip())]},
                "Checking your request, researching and drafting…",
            )

# Screen 2: review the draft
elif stage == "review":
    payload = st.session_state.payload or {}
    state = st.session_state.state or {}

    draft = payload.get("draft") or state.get("output") or ""
    agent = payload.get("agent") or state.get("current_agent", "")
    warnings = state.get("eval_warning") or []
    score = state.get("faithfulness_score")
    revision = state.get("revision_counter") or 0

    if not draft.strip():
        st.error(SERVICE_DOWN_MSG)
        new_request_button()
        st.stop()

    left, right = st.columns([3, 1])

    with left:
        st.subheader(f"Draft from the {agent} agent")
        st.markdown(draft)
        with st.expander("Copy as plain text"):
            st.code(draft, language="markdown")

    with right:
        st.markdown(f"**Revision {revision + 1} of {MAX_REVISIONS}**")

        if score is None:
            st.metric("Faithfulness", "Not checked")
        else:
            st.metric("Faithfulness", f"{score:.2f}")
            if score < FAITHFULNESS_THRESHOLD:
                st.warning("Some claims may not be backed by the sources.")

        if warnings:
            st.warning(f"{len(warnings)} check(s) flagged")
            for w in warnings:
                with st.expander("See details"):
                    st.text(w)
        else:
            st.success("All output checks passed")

        st.divider()
        feedback = st.text_area("What should change?", height=120)

        if st.button("Approve", type="primary", use_container_width=True):
            safe_run(
                Command(resume={"decision": "Satisfied", "feedback": ""}),
                "Finishing up…",
            )

        if st.button("Request changes", use_container_width=True):
            if not feedback.strip():
                st.warning("Please say what should change first.")
            else:
                safe_run(
                    Command(resume={"decision": "Unsatisfied", "feedback": feedback.strip()}),
                    "Revising the draft…",
                )

# Screen 3: finished
elif stage == "done":
    state = st.session_state.state or {}
    output = state.get("output") or ""
    agent = state.get("current_agent") or "content"

    if state.get("error"):
        st.error(state["error"])
    elif state.get("route_decision") == "unclear":
        st.warning(
            "I couldn't tell whether you wanted a blog post or a LinkedIn post. "
            "Try naming one in your request."
        )
        if state.get("route_reason"):
            st.caption(state["route_reason"])
    elif not output.strip():
        st.error(SERVICE_DOWN_MSG)
    else:
        if state.get("user_satisfaction") == "Satisfied":
            st.success("Approved")
        else:
            st.info("Reached the revision limit. Here's the latest draft.")
        st.markdown(output)
        st.download_button(
            "Download as Markdown",
            data=output,
            file_name=f"{agent}_draft.md",
            mime="text/markdown",
        )

    new_request_button()