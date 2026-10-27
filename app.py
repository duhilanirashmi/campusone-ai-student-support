import re
import streamlit as st

st.set_page_config(
    page_title="CampusOne | Student Support",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# CAMPUSONE — WEEK 2
# Question-specific specialized agent guidance
# ==================================================

AGENT_KEYWORDS = {
    "Academic Advisor Agent": [
        "course", "class", "degree", "academic", "credit",
        "graduat", "semester", "prerequisite", "gpa",
        "assignment", "enroll", "curriculum", "major",
        "grade", "study", "schedule"
    ],
    "Career & Opportunity Agent": [
        "career", "job", "intern", "resume", "interview",
        "linkedin", "employment", "recruit", "skill",
        "business analyst", "networking", "application",
        "cover letter", "portfolio"
    ],
    "Student Services Agent": [
        "library", "campus", "tutoring", "workshop",
        "student service", "student support", "housing",
        "financial aid", "appointment", "resource",
        "counseling", "office", "wellness", "transportation"
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


def select_guidance(question, guidance_rules, default_guidance):
    normalized = question.lower()

    for keywords, guidance in guidance_rules:
        if find_keywords(normalized, keywords):
            return guidance

    return default_guidance


# ==================================================
# ACADEMIC ADVISOR AGENT
# ==================================================

def academic_advisor_agent(question):

    guidance_rules = [
        (
            ["gpa", "grade", "academic performance"],
            {
                "topic": "Academic Performance",
                "recommendation": (
                    "Review your course grades and identify subjects "
                    "where additional academic support may be helpful."
                ),
                "next_steps": [
                    "Review course grading criteria.",
                    "Discuss improvement strategies with instructors.",
                    "Explore tutoring or academic support resources."
                ]
            }
        ),
        (
            ["graduat", "degree", "credit"],
            {
                "topic": "Graduation Planning",
                "recommendation": (
                    "Review your degree requirements and compare them "
                    "with your completed coursework."
                ),
                "next_steps": [
                    "Review the official degree requirements.",
                    "Identify remaining required courses and credits.",
                    "Consult an academic advisor for confirmation."
                ]
            }
        ),
        (
            ["prerequisite", "course", "class", "semester", "enroll"],
            {
                "topic": "Course Planning",
                "recommendation": (
                    "Plan upcoming courses based on degree requirements, "
                    "prerequisites, and academic goals."
                ),
                "next_steps": [
                    "Review available course descriptions.",
                    "Check prerequisite requirements.",
                    "Discuss your proposed schedule with an advisor."
                ]
            }
        )
    ]

    default_guidance = {
        "topic": "General Academic Guidance",
        "recommendation": (
            "Review your academic goals and available university "
            "resources to identify appropriate next steps."
        ),
        "next_steps": [
            "Identify your main academic concern.",
            "Review relevant university guidance.",
            "Contact an academic advisor when needed."
        ]
    }

    result = select_guidance(
        question,
        guidance_rules,
        default_guidance
    )

    return {
        "agent": "Academic Advisor Agent",
        **result,
        "limitation": (
            "This is general guidance based on controlled sample rules. "
            "Official academic decisions require university confirmation."
        )
    }


# ==================================================
# CAREER & OPPORTUNITY AGENT
# ==================================================

def career_opportunity_agent(question):

    guidance_rules = [
        (
            ["resume", "cover letter", "portfolio"],
            {
                "topic": "Application Preparation",
                "recommendation": (
                    "Tailor your application materials to the "
                    "requirements of your target position."
                ),
                "next_steps": [
                    "Review the job description.",
                    "Highlight relevant experience and skills.",
                    "Request feedback on your application materials."
                ]
            }
        ),
        (
            ["interview"],
            {
                "topic": "Interview Preparation",
                "recommendation": (
                    "Prepare examples that demonstrate your experience, "
                    "problem-solving skills, and professional strengths."
                ),
                "next_steps": [
                    "Research the organization and position.",
                    "Practice common interview questions.",
                    "Prepare examples using the STAR method."
                ]
            }
        ),
        (
            ["intern", "job", "employment", "application"],
            {
                "topic": "Internship and Job Search",
                "recommendation": (
                    "Identify opportunities aligned with your "
                    "academic background and career interests."
                ),
                "next_steps": [
                    "Review relevant internship or job descriptions.",
                    "Identify required qualifications and skills.",
                    "Prepare targeted applications and track progress."
                ]
            }
        ),
        (
            ["linkedin", "networking", "recruit"],
            {
                "topic": "Professional Networking",
                "recommendation": (
                    "Build professional connections and communicate "
                    "your interests clearly."
                ),
                "next_steps": [
                    "Update your professional profile.",
                    "Identify relevant industry professionals.",
                    "Prepare personalized connection messages."
                ]
            }
        ),
        (
            ["career", "skill", "business analyst"],
            {
                "topic": "Career Development",
                "recommendation": (
                    "Identify skills and experiences relevant to "
                    "your preferred career path."
                ),
                "next_steps": [
                    "Research target career roles.",
                    "Identify relevant technical and professional skills.",
                    "Develop a practical learning plan."
                ]
            }
        )
    ]

    default_guidance = {
        "topic": "General Career Guidance",
        "recommendation": (
            "Explore career options that align with your "
            "interests, skills, and academic background."
        ),
        "next_steps": [
            "Identify career interests.",
            "Research relevant opportunities.",
            "Consult university career services."
        ]
    }

    result = select_guidance(
        question,
        guidance_rules,
        default_guidance
    )

    return {
        "agent": "Career & Opportunity Agent",
        **result,
        "limitation": (
            "CampusOne does not currently retrieve live job postings "
            "or verify employment eligibility."
        )
    }


# ==================================================
# STUDENT SERVICES AGENT
# ==================================================

def student_services_agent(question):

    guidance_rules = [
        (
            ["tutoring", "workshop"],
            {
                "topic": "Academic Support Services",
                "recommendation": (
                    "Explore university tutoring programs and "
                    "academic workshops relevant to your needs."
                ),
                "next_steps": [
                    "Review the official student support directory.",
                    "Identify relevant tutoring or workshop options.",
                    "Confirm availability with the university."
                ]
            }
        ),
        (
            ["library"],
            {
                "topic": "Library Resources",
                "recommendation": (
                    "Explore university library services for "
                    "research materials and academic support."
                ),
                "next_steps": [
                    "Visit the university library website.",
                    "Review available research resources.",
                    "Contact library staff for assistance."
                ]
            }
        ),
        (
            ["housing", "transportation"],
            {
                "topic": "Campus Living Resources",
                "recommendation": (
                    "Review university-provided information about "
                    "housing and transportation resources."
                ),
                "next_steps": [
                    "Check official university resources.",
                    "Compare available support options.",
                    "Contact the relevant university office."
                ]
            }
        ),
        (
            ["counseling", "wellness"],
            {
                "topic": "Student Wellbeing Resources",
                "recommendation": (
                    "Explore university wellbeing and student "
                    "support services."
                ),
                "next_steps": [
                    "Review the official student services website.",
                    "Identify the appropriate support office.",
                    "Contact university staff for assistance."
                ]
            }
        ),
        (
            ["financial aid"],
            {
                "topic": "Financial Aid Information",
                "recommendation": (
                    "Review official university financial aid "
                    "information and available support channels."
                ),
                "next_steps": [
                    "Review published financial aid guidance.",
                    "Prepare questions about your situation.",
                    "Contact the financial aid office."
                ]
            }
        )
    ]

    default_guidance = {
        "topic": "General Student Services",
        "recommendation": (
            "Explore official university student services "
            "and support resources."
        ),
        "next_steps": [
            "Identify the type of support needed.",
            "Review the official student services directory.",
            "Contact the appropriate university office."
        ]
    }

    result = select_guidance(
        question,
        guidance_rules,
        default_guidance
    )

    return {
        "agent": "Student Services Agent",
        **result,
        "limitation": (
            "CampusOne does not yet have verified university "
            "service locations, schedules, or appointment availability."
        )
    }


AGENT_FUNCTIONS = {
    "Academic Advisor Agent": academic_advisor_agent,
    "Career & Opportunity Agent": career_opportunity_agent,
    "Student Services Agent": student_services_agent
}


# ==================================================
# COORDINATOR AGENT
# ==================================================

def route_question(question):

    normalized_question = question.lower().strip()

    if not normalized_question:
        return None

    selected_agents = {}

    for agent, keywords in AGENT_KEYWORDS.items():

        matches = find_keywords(
            normalized_question,
            keywords
        )

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

    if routing_result["human_review"]:
        return responses

    for agent_name in routing_result["agents"]:

        agent_function = AGENT_FUNCTIONS[agent_name]

        agent_result = agent_function(
            routing_result["question"]
        )

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


# ==================================================
# SESSION STATE
# ==================================================

if "latest_analysis" not in st.session_state:
    st.session_state.latest_analysis = None


# ==================================================
# USER INTERFACE
# ==================================================

st.title("🎓 CampusOne")
st.caption("AI Student Success & Career Support System")

st.subheader("CampusOne Student Support Assistant")

st.write(
    "Ask a question about academics, career opportunities, "
    "or university services. CampusOne will identify the "
    "appropriate specialized agents and coordinate their "
    "responses."
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


# ==================================================
# DISPLAY RESULTS
# ==================================================

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

    if result["human_review"]:

        st.error("Human Advisor Review Required")

        st.write(
            "I cannot make this determination; "
            "a human advisor is required."
        )

        st.info(
            "This request involves an official university decision. "
            "Please contact the appropriate university advisor "
            "for confirmation."
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
                        "### " + agent_result["agent"]
                    )

                    st.write(
                        "**Topic:** "
                        + agent_result["topic"]
                    )

                    st.write(
                        "**Recommendation:** "
                        + agent_result["recommendation"]
                    )

                    st.write("**Suggested Next Steps:**")

                    for step in agent_result["next_steps"]:
                        st.markdown("- " + step)

                    st.caption(
                        "Limitation: "
                        + agent_result["limitation"]
                    )

            st.divider()

            st.subheader("Coordinator's Combined Guidance")

            for agent_result in result["agent_responses"]:

                st.markdown(
                    "**" + agent_result["agent"] + "**"
                )

                st.write(
                    agent_result["recommendation"]
                )

            if len(result["agent_responses"]) > 1:

                st.success(
                    "Agent coordination completed: responses "
                    "were collected from multiple specialized "
                    "agents and combined into one result."
                )


# ==================================================
# PROJECT INFORMATION
# ==================================================

st.divider()

with st.expander("About the CampusOne Project"):

    st.write(
        "CampusOne is an approved five-agent student support "
        "project. The current prototype demonstrates "
        "Coordinator routing and communication with three "
        "specialized rule-based agent components."
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

    st.write(
        "Development status: The specialized agents currently provide "
        "question-specific guidance using predefined rules. "
        "LLM reasoning, RAG, MCP tools, and the Quality & "
        "Policy Review Agent are planned for later stages."
    )
