
import re
import streamlit as st

st.set_page_config(
    page_title="CampusOne | Student Support",
    page_icon="🎓",
    layout="wide"
)

AGENT_KEYWORDS = {
    "Academic Advisor Agent": [
        "course", "class", "degree", "academic", "credit",
        "graduat", "semester", "prerequisite", "gpa",
        "assignment", "enroll", "curriculum"
    ],
    "Career & Opportunity Agent": [
        "career", "job", "intern", "resume", "interview",
        "linkedin", "employment", "recruit", "skill",
        "business analyst", "networking"
    ],
    "Student Services Agent": [
        "library", "campus", "tutoring", "workshop",
        "student service", "student support", "housing",
        "financial aid", "appointment", "resource",
        "counseling", "office"
    ]
}

HUMAN_REVIEW_PATTERNS = [
    r"\b(officially|official|guarantee|certify)\b.*\b(graduat|eligib|degree|complet)",
    r"\b(confirm|approve)\b.*\b(graduat|eligib|degree|complet)",
    r"\b(change|update|delete)\b.*\b(grade|record|transcript)",
    r"\b(visa|immigration|sevis|i-20|opt|cpt)\b",
    r"\b(enroll me|withdraw me|drop my course)\b"
]


def find_keywords(question, keywords):
    matches = []
    for keyword in keywords:
        pattern = r"(?<!\w)" + re.escape(keyword) + r"\w*"
        if re.search(pattern, question):
            matches.append(keyword)
    return matches


def route_question(question):
    question = question.lower().strip()

    if not question:
        return None

    selected_agents = {}
    for agent, keywords in AGENT_KEYWORDS.items():
        matches = find_keywords(question, keywords)
        if matches:
            selected_agents[agent] = matches

    human_review = any(
        re.search(pattern, question)
        for pattern in HUMAN_REVIEW_PATTERNS
    )

    return {
        "agents": selected_agents,
        "human_review": human_review
    }


st.title("🎓 CampusOne")
st.caption("AI Student Success & Career Support System")

st.subheader("Coordinator Agent — Version 1")

st.write(
    "Ask a question about academics, career opportunities, "
    "or university services. CampusOne will identify which "
    "specialized agents should handle your request."
)

question = st.text_area(
    "How can CampusOne help you?",
    placeholder=(
        "Example: I'm graduating next semester. "
        "How can I prepare for a Business Analyst job?"
    ),
    height=120
)

if st.button("Analyze Question", type="primary"):
    result = route_question(question)

    if result is None:
        st.warning("Please enter a question.")

    else:
        st.divider()
        st.subheader("Coordinator's Decision")

        if result["agents"]:
            st.write("**Selected Agents:**")

            for agent, matches in result["agents"].items():
                st.success(agent)
                st.caption(
                    "Reason: Detected " + ", ".join(matches)
                )

            if len(result["agents"]) > 1:
                st.info(
                    "This question requires coordination "
                    "between multiple specialized agents."
                )

        else:
            st.warning(
                "The Coordinator needs more information "
                "to identify the appropriate agent."
            )

        if result["human_review"]:
            st.error("Human Advisor Review Required")
            st.write(
                "I cannot make this determination; "
                "a human advisor is required."
            )
        else:
            st.write(
                "**Human Review:** Not automatically required "
                "by the current routing rules."
            )

        st.caption(
            "Week 1 prototype: routing decisions are based "
            "on predefined rules. Specialized agents, RAG, "
            "and external tools will be added later."
        )

st.divider()

with st.expander("About the CampusOne Project"):
    st.write(
        "CampusOne is an approved five-agent student support "
        "project. This first version demonstrates the "
        "Coordinator Agent's question-routing functionality."
    )

    st.write(
        "The complete system will include an Academic Advisor "
        "Agent, Career & Opportunity Agent, Student Services "
        "Agent, and Quality & Policy Review Agent."
    )
