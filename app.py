import re
import streamlit as st


# ==================================================
# CAMPUSONE — APPLICATION CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CampusOne | Student Support",
    page_icon="🎓",
    layout="wide"
)


# ==================================================
# AGENT CONFIGURATION
# ==================================================

ACADEMIC = "Academic Advisor Agent"
CAREER = "Career & Opportunity Agent"
SERVICES = "Student Services Agent"

AGENT_KEYWORDS = {
    ACADEMIC: [
        "course", "class", "degree", "academic", "credit",
        "graduat", "semester", "prerequisite", "gpa",
        "assignment", "enroll", "curriculum", "major",
        "grade", "study", "schedule", "subject"
    ],
    CAREER: [
        "career", "job", "intern", "resume", "interview",
        "linkedin", "employment", "recruit", "skill",
        "business analyst", "networking", "application",
        "cover letter", "portfolio", "profession"
    ],
    SERVICES: [
        "library", "campus", "tutoring", "tutor",
        "workshop", "student service", "student support",
        "housing", "financial aid", "appointment",
        "resource", "counseling", "office", "wellness",
        "transportation"
    ]
}


# ==================================================
# HUMAN REVIEW RULES
# ==================================================

HUMAN_REVIEW_PATTERNS = [
    r"\b(officially|official|guarantee|certify)\b.*\b(graduat|eligib|degree|complet)",
    r"\b(confirm|approve)\b.*\b(graduat|eligib|degree|complet)",
    r"\b(change|update|delete)\b.*\b(grade|record|transcript)",
    r"\b(visa|immigration|sevis|i-20|opt|cpt)\b",
    r"\b(enroll me|withdraw me|drop my course)\b"
]


# ==================================================
# SHARED HELPER FUNCTIONS
# ==================================================

def find_keywords(question, keywords):
    matches = []

    for keyword in keywords:
        pattern = r"(?<!\w)" + re.escape(keyword) + r"\w*"

        if re.search(pattern, question.lower()):
            matches.append(keyword)

    return matches


def contains_any(question, keywords):
    return bool(find_keywords(question, keywords))


def create_response(agent, topic, recommendation, steps, limitation):
    return {
        "agent": agent,
        "topic": topic,
        "recommendation": recommendation,
        "next_steps": steps,
        "limitation": limitation
    }


def is_business_analyst_question(question):
    return contains_any(
        question,
        ["business analyst", "business analysis"]
    )



def is_course_skills_question(question):
    has_learning_intent = contains_any(
        question,
        [
            "course", "class", "subject", "skill",
            "learn", "focus", "prepare", "training"
        ]
    )

    has_career_intent = contains_any(
        question,
        [
            "career", "job", "intern",
            "business analyst", "profession"
        ]
    )

    return has_learning_intent and has_career_intent


# ==================================================
# ACADEMIC ADVISOR AGENT
# ==================================================

def academic_advisor_agent(question):

    normalized = question.lower()

    limitation = (
        "Academic subject areas are illustrative. "
        "CampusOne does not verify actual university course "
        "offerings, prerequisites, or degree requirements."
    )

    if is_course_skills_question(normalized):

        if is_business_analyst_question(normalized):

            return create_response(
                ACADEMIC,
                "Academic Preparation for Business Analysis",
                (
                    "Consider academic subject areas such as "
                    "business analytics, statistics, database "
                    "management, data visualization, and business "
                    "process analysis. These subjects can support "
                    "preparation for Business Analyst internships."
                ),
                [
                    "Review courses covering statistics and data analysis.",
                    "Explore database management and SQL-related coursework.",
                    "Consider business analytics and data visualization subjects.",
                    "Check actual course availability and prerequisites with an academic advisor."
                ],
                limitation
            )

        return create_response(
            ACADEMIC,
            "Career-Aligned Academic Planning",
            (
                "Choose academic subjects that develop the knowledge "
                "and analytical skills needed for your intended career."
            ),
            [
                "Identify the academic subjects most relevant to your target role.",
                "Compare those subjects with available university courses.",
                "Prioritize coursework that includes practical projects.",
                "Confirm prerequisites and degree applicability with an academic advisor."
            ],
            limitation
        )

    if contains_any(normalized, ["prerequisite"]):

        return create_response(
            ACADEMIC,
            "Course Prerequisite Planning",
            (
                "Plan your upcoming courses by reviewing prerequisite "
                "requirements and the sequence of courses in your program."
            ),
            [
                "Identify courses you want to take next semester.",
                "Review the published prerequisites for each course.",
                "Check whether prerequisite courses have been completed.",
                "Discuss your proposed schedule with an academic advisor."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["gpa", "grade", "academic performance"]
    ):

        return create_response(
            ACADEMIC,
            "Academic Performance",
            (
                "Review your academic progress and identify subjects "
                "where additional study or academic support may help."
            ),
            [
                "Review course grading criteria.",
                "Identify topics requiring additional practice.",
                "Discuss improvement strategies with instructors.",
                "Explore tutoring and academic support resources."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["graduat", "degree", "credit"]
    ):

        return create_response(
            ACADEMIC,
            "Graduation Planning",
            (
                "Review your published degree requirements and compare "
                "them with your completed coursework to prepare for "
                "a discussion with your academic advisor."
            ),
            [
                "Review the official degree requirements.",
                "Identify potentially remaining courses and credits.",
                "Prepare questions about your graduation timeline.",
                "Request official confirmation from an academic advisor."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["course", "class", "semester", "enroll", "schedule"]
    ):

        return create_response(
            ACADEMIC,
            "Course Planning",
            (
                "Plan your upcoming courses around academic goals, "
                "published prerequisites, and program requirements."
            ),
            [
                "Review course descriptions.",
                "Identify relevant prerequisites.",
                "Consider your academic workload.",
                "Discuss your proposed schedule with an advisor."
            ],
            limitation
        )

    return create_response(
        ACADEMIC,
        "General Academic Guidance",
        (
            "Review your academic goals and identify the university "
            "resources or academic guidance most relevant to your question."
        ),
        [
            "Clarify your main academic concern.",
            "Review official university academic information.",
            "Contact an academic advisor when confirmation is needed."
        ],
        limitation
    )


# ==================================================
# CAREER & OPPORTUNITY AGENT
# ==================================================

def career_opportunity_agent(question):

    normalized = question.lower()

    limitation = (
        "Career guidance is based on predefined examples. "
        "CampusOne does not retrieve live job postings "
        "or verify employment eligibility."
    )

    if is_course_skills_question(normalized):

        if is_business_analyst_question(normalized):

            return create_response(
                CAREER,
                "Business Analyst Skills Development",
                (
                    "For Business Analyst internships, consider developing "
                    "skills in Excel, SQL, Power BI, requirements gathering, "
                    "business process analysis, problem-solving, and "
                    "stakeholder communication."
                ),
                [
                    "Practice Excel for data cleaning, analysis, and reporting.",
                    "Build foundational SQL querying skills.",
                    "Create a sample dashboard using Power BI or a similar tool.",
                    "Practice documenting business requirements and process improvements.",
                    "Review internship descriptions to identify frequently requested skills."
                ],
                limitation
            )

        return create_response(
            CAREER,
            "Career Skills Development",
            (
                "Identify the technical and professional skills commonly "
                "requested for your target role and build practical "
                "experience demonstrating those skills."
            ),
            [
                "Review several descriptions for your target role.",
                "Identify recurring technical and communication skills.",
                "Select projects or learning activities that build those skills.",
                "Document your progress for future applications."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["resume", "cover letter", "portfolio"]
    ):

        if is_business_analyst_question(normalized):

            return create_response(
                CAREER,
                "Business Analyst Application Preparation",
                (
                    "Tailor your resume to highlight analytical projects, "
                    "business problem-solving, relevant tools, and "
                    "measurable accomplishments."
                ),
                [
                    "Review the Business Analyst internship description.",
                    "Highlight relevant Excel, SQL, or reporting experience.",
                    "Describe projects using clear outcomes and measurable results.",
                    "Request feedback before submitting your application."
                ],
                limitation
            )

        return create_response(
            CAREER,
            "Application Preparation",
            (
                "Tailor your resume and application materials "
                "to the requirements of your target position."
            ),
            [
                "Review the job description.",
                "Highlight relevant experience and skills.",
                "Use specific examples of accomplishments.",
                "Request feedback on your application materials."
            ],
            limitation
        )

    if contains_any(normalized, ["interview"]):

        return create_response(
            CAREER,
            "Interview Preparation",
            (
                "Prepare examples that demonstrate your skills, "
                "problem-solving abilities, and relevant experience."
            ),
            [
                "Research the organization and position.",
                "Practice common interview questions.",
                "Prepare examples using the STAR method.",
                "Develop thoughtful questions for the interviewer."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["intern", "job", "employment", "application"]
    ):

        return create_response(
            CAREER,
            "Internship and Job Search",
            (
                "Identify opportunities aligned with your "
                "academic background, interests, and career goals."
            ),
            [
                "Review relevant internship or job descriptions.",
                "Identify recurring qualifications and skills.",
                "Prepare targeted application materials.",
                "Track applications and follow-up activities."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["linkedin", "networking", "recruit"]
    ):

        return create_response(
            CAREER,
            "Professional Networking",
            (
                "Develop professional connections and communicate "
                "your career interests clearly."
            ),
            [
                "Update your professional profile.",
                "Identify relevant professionals and organizations.",
                "Prepare personalized connection messages.",
                "Follow up professionally when appropriate."
            ],
            limitation
        )

    return create_response(
        CAREER,
        "General Career Development",
        (
            "Explore career opportunities that align with your "
            "interests, strengths, and academic background."
        ),
        [
            "Identify your preferred career direction.",
            "Research relevant roles and qualifications.",
            "Develop a practical learning plan.",
            "Explore available career support resources."
        ],
        limitation
    )


# ==================================================
# STUDENT SERVICES AGENT
# ==================================================

def student_services_agent(question):

    normalized = question.lower()

    limitation = (
        "CampusOne does not currently verify university "
        "service availability, office locations, schedules, "
        "or appointment information."
    )

    if contains_any(normalized, ["tutoring", "tutor"]):

        return create_response(
            SERVICES,
            "Tutoring and Academic Support",
            (
                "Explore university tutoring resources or academic "
                "support options related to the subject where "
                "you need assistance."
            ),
            [
                "Identify the course or topic requiring support.",
                "Review the official university student support directory.",
                "Check whether tutoring or instructor office hours are available.",
                "Confirm service availability with the university."
            ],
            limitation
        )

    if contains_any(normalized, ["workshop"]):

        return create_response(
            SERVICES,
            "Student Workshops",
            (
                "Explore academic or professional development "
                "workshops relevant to your learning goals."
            ),
            [
                "Review university workshop announcements.",
                "Identify workshops related to your interests.",
                "Check published registration information.",
                "Confirm event details with the organizer."
            ],
            limitation
        )

    if contains_any(normalized, ["library"]):

        return create_response(
            SERVICES,
            "Library Resources",
            (
                "Explore library resources that may support "
                "your research and academic work."
            ),
            [
                "Visit the official university library website.",
                "Review available databases and research resources.",
                "Identify relevant materials for your topic.",
                "Contact library staff for additional assistance."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["housing", "transportation"]
    ):

        return create_response(
            SERVICES,
            "Campus Living Resources",
            (
                "Review official university information about "
                "housing and transportation support options."
            ),
            [
                "Review available university information.",
                "Identify the type of support needed.",
                "Compare published resources.",
                "Contact the appropriate university office."
            ],
            limitation
        )

    if contains_any(
        normalized,
        ["counseling", "wellness"]
    ):

        return create_response(
            SERVICES,
            "Student Wellbeing Resources",
            (
                "Explore official student wellbeing resources "
                "and available university support channels."
            ),
            [
                "Review the official student services website.",
                "Identify an appropriate support resource.",
                "Check available contact information.",
                "Reach out to the relevant university office."
            ],
            limitation
        )

    if contains_any(normalized, ["financial aid"]):

        return create_response(
            SERVICES,
            "Financial Aid Information",
            (
                "Review official university financial aid "
                "information and support channels."
            ),
            [
                "Review published financial aid guidance.",
                "Prepare questions about your situation.",
                "Identify the appropriate financial aid contact.",
                "Request official clarification when needed."
            ],
            limitation
        )

    return create_response(
        SERVICES,
        "General Student Services",
        (
            "Explore official university services "
            "and resources relevant to your needs."
        ),
        [
            "Identify the type of support required.",
            "Review the official student services directory.",
            "Contact the appropriate university office."
        ],
        limitation
    )
    
# ==================================================
# WEEK 3 — QUALITY & POLICY REVIEW AGENT
# ==================================================

def quality_policy_review_agent(routing_result, agent_responses):
    issues = []

    if routing_result.get("human_review", False):
        return {
            "agent": "Quality & Policy Review Agent",
            "status": "human_review_required",
            "approved": False,
            "issues": [
                "Official university decisions require human review."
            ]
        }

    required_fields = [
        "agent",
        "topic",
        "recommendation",
        "next_steps",
        "limitation"
    ]

    if not agent_responses:
        issues.append("No specialized agent responses available.")

    for response in agent_responses:
        agent_name = response.get("agent", "Unknown Agent")

        for field in required_fields:
            if not response.get(field):
                issues.append(
                    f"{agent_name}: Missing or empty field '{field}'."
                )

        if not isinstance(response.get("next_steps"), list):
            issues.append(
                f"{agent_name}: Next steps must be a list."
            )

        metadata = response.get("message", {})

        if metadata.get("status") != "completed":
            issues.append(
                f"{agent_name}: Communication not completed."
            )

    return {
        "agent": "Quality & Policy Review Agent",
        "status": "passed" if not issues else "flagged",
        "approved": not issues,
        "issues": issues
    }

AGENT_FUNCTIONS = {
    ACADEMIC: academic_advisor_agent,
    CAREER: career_opportunity_agent,
    SERVICES: student_services_agent
}


# ==================================================
# COORDINATOR — QUESTION ROUTING
# ==================================================

def route_question(question):

    normalized = question.lower().strip()

    if not normalized:
        return None

    selected_agents = {}

    for agent, keywords in AGENT_KEYWORDS.items():

        matches = find_keywords(normalized, keywords)

        if matches:
            selected_agents[agent] = matches

    tutoring_intent = contains_any(
        normalized,
        ["tutoring", "tutor"]
    )

    academic_planning_intent = contains_any(
        normalized,
        [
            "prerequisite", "course planning",
            "degree requirement", "graduat",
            "which course", "which class",
            "semester schedule"
        ]
    )

    if tutoring_intent and not academic_planning_intent:

        selected_agents = {
            SERVICES: find_keywords(
                normalized,
                AGENT_KEYWORDS[SERVICES]
            )
        }

    elif is_course_skills_question(normalized):

        if contains_any(
            normalized,
            ["course", "class", "subject"]
        ):

            selected_agents[ACADEMIC] = find_keywords(
                normalized,
                AGENT_KEYWORDS[ACADEMIC]
            )

        selected_agents[CAREER] = find_keywords(
            normalized,
            AGENT_KEYWORDS[CAREER]
        )

    human_review = any(
        re.search(pattern, normalized)
        for pattern in HUMAN_REVIEW_PATTERNS
    )

    return {
        "question": question.strip(),
        "agents": selected_agents,
        "human_review": human_review
    }


# ==================================================
# WEEK 3 — STRUCTURED AGENT MESSAGES
# ==================================================

def create_agent_message(agent_name, question):
    return {
        "sender": "Coordinator Agent",
        "recipient": agent_name,
        "student_question": question,
        "purpose": "Provide relevant student support guidance",
        "status": "dispatched"
    }

# ==================================================
# COORDINATOR — AGENT COMMUNICATION
# ==================================================

def coordinate_agents(routing_result):

    if routing_result["human_review"]:
        return []

    responses = []

    for agent_name in routing_result["agents"]:

        # Coordinator prepares a structured request.
        message = create_agent_message(
            agent_name,
            routing_result["question"]
        )

        # Deliver the question to the selected agent.
        agent_function = AGENT_FUNCTIONS[agent_name]

        response = agent_function(
            message["student_question"]
        )

        # Attach communication metadata to the response.
        response["message"] = {
            "sender": agent_name,
            "recipient": "Coordinator Agent",
            "status": "completed",
            "request_purpose": message["purpose"]
        }

        responses.append(response)

    return responses


# ==================================================
# COORDINATOR — MULTI-AGENT ACTION PLAN
# ==================================================

def create_combined_guidance(question, responses):

    # A combined plan is only useful when multiple
    # specialized agents contribute.

    if len(responses) < 2:
        return None

    agent_names = {
        response["agent"]
        for response in responses
    }

    if (
        ACADEMIC in agent_names
        and CAREER in agent_names
        and is_course_skills_question(question)
    ):

        if is_business_analyst_question(question):

            return {
                "title": "Recommended Academic and Career Preparation",
                "summary": (
                    "Consider coursework in business analytics, "
                    "statistics, database management, and data "
                    "visualization. Alongside your coursework, "
                    "develop practical skills in Excel, SQL, "
                    "Power BI, requirements gathering, and "
                    "stakeholder communication."
                ),
                "steps": [
                    "Review relevant university course descriptions and prerequisites.",
                    "Prioritize practical analytical and business-focused projects.",
                    "Build a small portfolio demonstrating Excel, SQL, or dashboard skills.",
                    "Compare your skills with Business Analyst internship descriptions.",
                    "Confirm your academic plan with a university advisor."
                ]
            }

        return {
            "title": "Academic and Career Development Plan",
            "summary": (
                "Align your academic learning with the technical "
                "and professional skills required for your "
                "preferred career direction."
            ),
            "steps": [
                "Identify relevant academic subjects.",
                "Review the skills requested in target job descriptions.",
                "Select projects that develop those skills.",
                "Review your academic plan with an advisor."
            ]
        }

    # General multi-agent coordination:
    # combine unique next steps.

    combined_steps = []
    seen_steps = set()

    for response in responses:

        for step in response["next_steps"]:

            normalized_step = step.lower().strip()

            if normalized_step not in seen_steps:

                combined_steps.append(step)
                seen_steps.add(normalized_step)

    return {
        "title": "Coordinated Student Support Plan",
        "summary": (
            "Your question involves more than one area of student "
            "support. The following action plan brings together "
            "the recommendations from the relevant agents."
        ),
        "steps": combined_steps[:6]
    }


# ==================================================
# MAIN ANALYSIS
# ==================================================

def analyze_question(question):
    routing_result = route_question(question)

    if routing_result is None:
        return None

    # Step 1: Collect responses from specialized agents.
    responses = coordinate_agents(routing_result)

    # Step 2: Review responses before approving guidance.
    quality_review = quality_policy_review_agent(
        routing_result,
        responses
    )

    routing_result["quality_review"] = quality_review

    # Step 3: Prevent unapproved guidance from being displayed.
    if not quality_review["approved"]:
        routing_result["agent_responses"] = []
        routing_result["combined_guidance"] = None
        return routing_result

    # Step 4: Store approved responses.
    routing_result["agent_responses"] = responses

    # Step 5: Generate combined guidance only after approval.
    routing_result["combined_guidance"] = (
        create_combined_guidance(
            routing_result["question"],
            responses
        )
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

st.caption(
    "AI Student Success & Career Support System"
)

st.subheader(
    "CampusOne Student Support Assistant"
)

# WEEK 3 — STUDENT / DEVELOPER DEMO VIEW
developer_view = st.toggle(
    "Developer Demo View",
    value=False,
    help="Show agent routing, communication, and review details."
)

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

    st.session_state.latest_analysis = (
        analyze_question(question)
    )


# ==================================================
# DISPLAY RESULTS
# ==================================================

result = st.session_state.latest_analysis


if submitted and result is None:

    st.warning(
        "Please enter a question."
    )


elif result is not None:

    st.divider()

    st.subheader(
        "Coordinator's Decision"
    )

    st.write(
        "**Student Question:**"
    )

    st.write(
        result["question"]
    )

    # Display selected agents

    if result["agents"]:

        st.write(
            "**Selected Agents:**"
        )

        for agent, matches in result["agents"].items():

            st.success(agent)

            
            if developer_view:
                if matches:
                    st.caption(
                        "Routing reason: Detected "
                        + ", ".join(matches)
                    )
                else:
                    st.caption(
                        "Routing reason: Question intent "
                        "requires this specialized agent."
                    )
               
        if len(result["agents"]) > 1 and developer_view:
            st.info(
                "Multiple agents selected. The Coordinator "
                "will collect their individual responses."
            )

            
        if not result["agents"] and not result["human_review"]:
            st.warning(
                "The Coordinator could not identify a suitable "
                "specialized agent. Please rephrase your question."
            )

        # WEEK 3 — QUALITY & POLICY REVIEW RESULTS
        quality_review = result.get("quality_review", {})

        if developer_view and quality_review:
            st.subheader("Quality & Policy Review Agent")

            review_status = quality_review.get(
                "status", "unknown"
            )

            st.write(
                f"**Review Status:** {review_status.title().replace('_', ' ')}"
            )

            if quality_review.get("approved", False):
                st.success(
                    "Structural quality checks passed. "
                    "Response approved for display."
                )
            else:
                st.warning(
                    "Response not approved for automated guidance."
                )

            issues = quality_review.get("issues", [])

            if issues:
                st.write("**Issues Identified:**")
                for issue in issues:
                    st.write("- " + issue)
            else:
                st.caption(
                    "No structural validation issues detected."
                )


    # Human escalation

    if result["human_review"]:

        st.error(
            "Human Advisor Review Required"
        )

        st.write(
            "I cannot make this determination; "
            "a human advisor is required."
        )

        st.info(
            "This request involves an official university "
            "decision or an area requiring human review. "
            "Please contact the appropriate university "
            "advisor for confirmation."
        )

    
                
        if developer_view and not result["human_review"]:
            st.write(
                "**Human Review:** Not automatically required "
                "by the current routing rules."
            )


        # Specialized agent responses

        if result["agent_responses"]:

            st.divider()

            st.subheader(
                "Specialized Agent Responses"
            )

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

                    st.write(
                        "**Suggested Next Steps:**"
                    )

                    for step in agent_result["next_steps"]:

                        st.markdown(
                            "- " + step
                        )

                    st.caption(
                        "Limitation: "
                        + agent_result["limitation"]
                    )
                    
        
        # WEEK 3 — AGENT COMMUNICATION TRACE
        if developer_view:
            with st.expander("Agent Communication Trace", expanded=False):
                st.caption(
                    "Structured in-process communication between "
                    "the Coordinator and specialized agents."
                )

                for agent_result in result["agent_responses"]:
                    metadata = agent_result.get("message", {})
                    agent_name = agent_result["agent"]

                    st.write(
                        f"**Coordinator Agent → {agent_name}**"
                    )

                    st.caption(
                        "Request dispatched with student question "
                        "and guidance purpose."
                    )

                    st.write(
                        f"**{metadata.get('sender', agent_name)} → "
                        f"{metadata.get('recipient', 'Coordinator Agent')}**"
                    )

                    st.caption(
                        f"Response status: "
                        f"{metadata.get('status', 'unknown')}"
                    )

                    st.divider()


        # Only display combined guidance for multi-agent requests.

        if (
            len(result["agent_responses"]) > 1
            and result["combined_guidance"] is not None
        ):

            combined = result["combined_guidance"]

            st.divider()

            st.subheader(
                "Coordinator's Combined Guidance"
            )

            st.markdown(
                "### " + combined["title"]
            )

            st.write(
                combined["summary"]
            )

            st.write(
                "**Recommended Next Steps:**"
            )

            for step in combined["steps"]:

                st.markdown(
                    "- " + step
                )

            
        if developer_view:
            st.success(
                "Agent coordination completed: "
                "recommendations from multiple "
                "specialized agents were combined "
                "into one action plan."
            )


# ==================================================
# PROJECT INFORMATION
# ==================================================

st.divider()

with st.expander(
    "About the CampusOne Project"
):

    st.write(
        "CampusOne is an approved five-agent student support "
        "project. The current prototype demonstrates "
        "Coordinator routing and communication with three "
        "specialized rule-based agent components."
    )

    st.write(
        "The planned system includes the Coordinator Agent, "
        "Academic Advisor Agent, Career & Opportunity Agent, "
        "Student Services Agent, and Quality & Policy Review Agent."
    )

    st.write(
        "The current application uses controlled sample "
        "guidance and predefined routing rules. "
        "It does not access private student records "
        "or make official university decisions."
    )

    st.write(
        "The Coordinator identifies relevant agents, "
        "collects their responses, and generates a combined "
        "action plan when multiple specialized agents contribute."
    )

    st.write(
        "For single-agent questions, CampusOne displays "
        "the specialized agent's guidance directly without "
        "duplicating the response."
    )

    st.write(
        "Future development may include LLM reasoning, "
        "retrieval-augmented generation (RAG), "
        "MCP tools, and a dedicated Quality & "
        "Policy Review Agent."
    )
