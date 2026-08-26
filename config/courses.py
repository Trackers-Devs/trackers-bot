from static import colors
from util.dataclasses import CourseCategory, CourseConcentration

SUBJECTS = ["CS", "MATH", "IE", "STAT"]

CORE_CS = CourseCategory(name="Core CS", color=colors.CORE_CS)
TECHNICAL_ELECTIVE = CourseCategory(
    name="Technical Elective", color=colors.TECH_ELECTIVE
)
MATH = CourseCategory(name="Math", color=colors.MATH)
STAT = CourseCategory(name="Stat", color=colors.STAT)

CATEGORIES = [CORE_CS, TECHNICAL_ELECTIVE, MATH, STAT]

AI_ML = CourseConcentration(name="AI/ML", color=colors.AI_ML)
DATA_SCIENCE = CourseConcentration(name="Data Science", color=colors.DATA_SCIENCE)
DSA = CourseConcentration(name="DSA", color=colors.DSA)
HCI = CourseConcentration(name="HCI", color=colors.HCI)
LANGUAGES = CourseConcentration(name="Languages", color=colors.LANGUAGES)
SECURITY = CourseConcentration(name="Security", color=colors.SECURITY)
SWE = CourseConcentration(name="SWE", color=colors.SWE)
SYSTEMS = CourseConcentration(name="Systems", color=colors.SYSTEMS)

SPECIAL_TOPICS = CourseConcentration(name="Special Topics", color=colors.SPECIAL_TOPICS)

CONCENTRATIONS = [
    AI_ML,
    DATA_SCIENCE,
    DSA,
    HCI,
    LANGUAGES,
    SECURITY,
    SWE,
    SYSTEMS,
    SPECIAL_TOPICS,
]
