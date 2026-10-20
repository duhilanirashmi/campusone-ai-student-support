
import re
import streamlit as st

st.set_page_config(
    page_title="CampusOne | Student Support",
    page_icon="🎓",
    layout="wide"
)

# --------------------------------------------------
# CAMPUSONE — COORDINATOR AGENT VERSION 1.1
# Week 1 working prototype
# --------------------------------------------------

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


# --------------------------------------------------
# SPECIALIZED PROTOTYPE AGENTS
# These return controlled guidance, not official advice.
# --------------------------------------------------

def academic_advisor_agent(question):
    return {
        "agent": "Academic Advisor Agent",
        "response": (
            "Review your degree requirements, completed credits, "
            "course prerequisites, and upcoming semester options. "
            "For a confirmed graduation plan or official eligibility "
            "decision, consult your university academic advisor."
        )
    }


def career_opportunity_agent(question):
    return {
        "agent": "Career & Opportunity Agent",
        "response": (
            "Identify the skills required for your target roles, "
            "review relevant internship or job descriptions, "
            "and prepare your resume and interview examples. "
            "Consider discussing opportunities with your "
            "university career services team."
        )
    }


def student_services_agent(question):
    return {
        "agent": "Student Services Agent",
        "response": (
            "Check your university's official student services "
            "directory for tutoring, library support, workshops, "
            "and appointments. CampusOne does not yet have "
            "verified university service locations or schedules."
        )
    }


AGENT_FUNCTIONS = {
    "Academic Advisor Agent": academic_advisor_agent,
    "Career & Opportunity Agent": career_opportunity_agent,
    "Student Services Agent": student_services_agent
}


# --------------------------------------------------
# COORDINATOR AGENT
# Routes requests and collects agent responses.
# --------------------------------------------------

def route_question(question):
    normalized_question = question.lower().strip()

    if not normalized_question:
        return None

    selected_agents = {}

    for agent, keywords in AGENT_KEYWORDS.items():
        matches = find_keywords(normalized_question, keywords)

        if matches:
            selected_agents[agent] = matches

    human_review = any(
        re.search(pattern, normalized_question)
        for pattern in HUMAN_REVIEW_PATTERNS
    )

    return {
        "question": question.strip(),
        "agents": selected_agents,
        "human_review": human_review
    }


def coordinate_agents(routing_result):
    responses = []

    # Do not generate automated guidance for
    # requests requiring an official human decision.
    if routing_result["human_review"]:
        return responses

    for agent_name in routing_result["agents"]:
        agent_function = AGENT_FUNCTIONS[agent_name]
        agent_result = agent_function(routing_result["question"])
        responses.append(agent_result)

    return responses


def analyze_question(question):
    routing_result = route_question(question)

    if routing_result is None:
        return None

    routing_result["agent_responses"] = coordinate_agents(
        routing_result
    )

    return routing_result


# --------------------------------------------------
# SESSION STATE
# Keeps the latest analysis visible across reruns.
# --------------------------------------------------

if "latest_analysis" not in st.session_state:
    st.session_state.latest_analysis = None


# --------------------------------------------------
# STREAMLIT USER INTERFACE
# --------------------------------------------------

st.title("🎓 CampusOne")
st.caption("AI Student Success & Career Support System")

st.subheader("CampusOne Student Support Assistant")

st.write(
    "Ask a question about academics, career opportunities, "
    "or university services. CampusOne will identify the "
    "appropriate specialized agents and coordinate their "
    "prototype responses."
)

with st.form("campusone_question_form"):
    question = st.text_area(
        "How can CampusOne help you?",
        placeholder=(
            "Example: I'm graduating next semester and "
            "want to apply for a Business Analyst internship."
        ),
        height=120
    )

    submitted = st.form_submit_button(
        "Analyze Question",
        type="primary"
    )

if submitted:
    st.session_state.latest_analysis = analyze_question(question)


# --------------------------------------------------
# DISPLAY LATEST ANALYSIS
# --------------------------------------------------

result = st.session_state.latest_analysis

if submitted and result is None:
    st.warning("Please enter a question.")

elif result is not None:
    st.divider()
    st.subheader("Coordinator's Decision")

    st.write("**Student Question:**")
    st.write(result["question"])

    if result["agents"]:
        st.write("**Selected Agents:**")

        for agent, matches in result["agents"].items():
            st.success(agent)
            st.caption(
                "Routing reason: Detected "
                + ", ".join(matches)
            )

        if len(result["agents"]) > 1:
            st.info(
                "Multiple agents selected. The Coordinator "
                "will collect their individual responses."
            )

    else:
        st.warning(
            "The Coordinator could not identify a suitable "
            "specialized agent. Please rephrase your question."
        )

    # Human review takes priority over automated responses.
    if result["human_review"]:
        st.error("Human Advisor Review Required")

        st.write(
            "I cannot make this determination; "
            "a human advisor is required."
        )

        st.caption(
            "No specialized agent response was generated "
            "because this request requires human oversight."
        )

    else:
        st.write(
            "**Human Review:** Not automatically required "
            "by the current routing rules."
        )

        if result["agent_responses"]:
            st.divider()
            st.subheader("Specialized Agent Responses")

            for agent_result in result["agent_responses"]:
                with st.container(border=True):
                    st.markdown(
                        "**" + agent_result["agent"] + "**"
                    )

                    st.write(agent_result["response"])

            st.divider()
            st.subheader("Coordinator's Combined Guidance")

            st.write(
                "The Coordinator has gathered the following "
                "guidance from the selected agents:"
            )

            for agent_result in result["agent_responses"]:
                st.markdown(
                    "- **"
                    + agent_result["agent"]
                    + ":** "
                    + agent_result["response"]
                )

            if len(result["agent_responses"]) > 1:
                st.success(
                    "Agent coordination completed: responses "
                    "were collected from multiple specialized "
                    "agents and combined into one result."
                )

    st.caption(
        "Week 1 prototype: routing and agent responses use "
        "predefined rules and controlled sample guidance. "
        "LLM reasoning, RAG, MCP tools, and the Quality & "
        "Policy Review Agent are planned for later stages."
    )


# --------------------------------------------------
# PROJECT INFORMATION
# --------------------------------------------------

st.divider()

with st.expander("About the CampusOne Project"):
    st.write(
        "CampusOne is an approved five-agent student support "
        "project. This prototype demonstrates Coordinator "
        "routing and communication with three specialized "
        "rule-based agent components."
    )

    st.write(
        "The complete system will include the Coordinator "
        "Agent, Academic Advisor Agent, Career & Opportunity "
        "Agent, Student Services Agent, and Quality & "
        "Policy Review Agent."
    )

    st.write(
        "This application currently uses controlled sample "
        "guidance only. It does not access private student "
        "records or make official university decisions."
    )
