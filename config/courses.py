from static import colors
from util.dataclasses import CourseCategory, CourseConcentration

CORE_CS = CourseCategory(
    name="Core CS",
    color=colors.CORE_CS,
    subjects=("CS",),
    numbers=frozenset(
        {
            "111",
            "141",
            "151",
            "211",
            "251",
            "261",
            "277",
            "301",
            "341",
            "342",
            "361",
            "362",
            "377",
            "401",
            "499",
        }
    ),
)
CS_ELECTIVE = CourseCategory(
    name="CS Elective", color=colors.CS_ELECTIVE, subjects=("CS",)
)
MATH = CourseCategory(name="Math", color=colors.MATH, subjects=("MATH",))
STAT = CourseCategory(name="Stat", color=colors.STAT, subjects=("STAT", "IE"))

CATEGORIES = [CORE_CS, CS_ELECTIVE, MATH, STAT]

AI_ML = CourseConcentration(name="AI/ML", color=colors.AI_ML)
DATA_SCIENCE = CourseConcentration(name="Data Science", color=colors.DATA_SCIENCE)
DSA = CourseConcentration(name="DSA", color=colors.DSA)
HCI = CourseConcentration(name="HCI", color=colors.HCI)
LANGUAGES = CourseConcentration(name="Languages", color=colors.LANGUAGES)
SECURITY = CourseConcentration(name="Security", color=colors.SECURITY)
SPECIAL_TOPICS = CourseConcentration(name="Special Topics", color=colors.SPECIAL_TOPICS)
SWE = CourseConcentration(name="SWE", color=colors.SWE)
SYSTEMS = CourseConcentration(name="Systems", color=colors.SYSTEMS)

CONCENTRATIONS = {
    **dict.fromkeys(
        (CORE_CS, CS_ELECTIVE),
        [
            AI_ML,
            DATA_SCIENCE,
            DSA,
            HCI,
            LANGUAGES,
            SECURITY,
            SPECIAL_TOPICS,
            SWE,
            SYSTEMS,
        ],
    )
}
