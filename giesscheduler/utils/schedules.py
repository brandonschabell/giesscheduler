from __future__ import annotations

import itertools
from typing import Self
from giesscheduler.utils import courses


########################################
### \/ \/ \/ UPDATE THESE \/ \/ \/ #####
########################################
REQUIRED = {
    courses.TermYear(courses.Term.SPRING1, 2025): {courses.MBA597, courses.ACCY500},
    courses.TermYear(courses.Term.SPRING2, 2025): {courses.MBA551},
    courses.TermYear(courses.Term.FALL2, 2025): {courses.ACCY532, courses.CapstoneESI},
}
SPECIALIZATIONS = [
    courses.Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION, 
    courses.Specialization.MERGERS_AND_ACQUISITIONS
]
CAPSTONES = [
    courses.CapstoneESI, 
    courses.CapstoneFM,
]
########################################
### /\ /\ /\ UPDATE THESE /\ /\ /\ #####
########################################


def get_courses(capstones: list[courses.Course], specializations: list[courses.Specialization]) -> list[courses.Course]:
    """Returns the list of courses that will be taken."""
    # Hardcoded for now, returning all courses.
    courses_ = [
        courses.MBA597, courses.MBA598,
        courses.BADM508, courses.BADM509, courses.BADM544,
        courses.BADM572, courses.FIN574, courses.FIN571,
        courses.BADM520, courses.BADM567, courses.ACCY503,
        courses.ACCY500, courses.FIN511, courses.FIN570,
    ]
    for specialization in specializations:
        if specialization == courses.Specialization.DIGITAL_MARKETING:
            courses_.extend([courses.MBA545, courses.MBA542, courses.MBA543])
        elif specialization == courses.Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION:
            courses_.extend([courses.MBA551, courses.MBA552, courses.MBA553])
        elif specialization == courses.Specialization.GLOBAL_CHALLENGES_IN_BUSINESS:
            courses_.extend([courses.MBA547, courses.MBA548, courses.MBA549])
        elif specialization == courses.Specialization.BUSINESS_ANALYTICS:
            courses_.extend([courses.MBA561, courses.MBA562, courses.MBA563, courses.MBA564])
        elif specialization == courses.Specialization.MERGERS_AND_ACQUISITIONS:
            courses_.extend([courses.FIN572, courses.ACCY532, courses.FIN573])
    return courses_ + capstones


class Schedule:
    def __init__(self, course_load: dict[courses.TermYear, set[courses.Course]], max_terms: int = 10, required: dict[courses.TermYear, set[courses.Course]] | None = None, max_non_capstones_per_term: int = 2) -> None:
        self.course_load = course_load
        self._max_terms = max_terms
        self._required = required
        self._max_non_capstones_per_term = max_non_capstones_per_term
        self._is_complete = False
        
    def __str__(self) -> str:
        value = ""
        for term_year, term_courses in self.course_load.items():
            value += f"{term_year}:\n"
            for term_course in term_courses:
                value += f"  {term_course}\n"
        return value
    
    def __repr__(self) -> str:
        return str(self)
    
    def mark_as_complete(self) -> None:
        self._is_complete = True
    
    def add_term(self, course_load: set[courses.Course]) -> Self:
        """Adds a term to the schedule."""
        term_year = max(self.course_load.keys()).next_term()
        self.course_load[term_year] = course_load
        return self
    
    def add_course(self, course: courses.Course, max_courses_per_term: int) -> Self:
        """Adds a course to the schedule."""
        term_year = max(self.course_load.keys())
        if len(self.course_load[term_year]) < max_courses_per_term and term_year.term in course.terms_offered:
            self.course_load[term_year].add(course)
        else:
            self.course_load[term_year.next_term()] = set()
            return self.add_course(course, max_courses_per_term)
        return self
    
    def copy(self) -> Schedule:
        """Creates a copy of the schedule."""
        return Schedule(self.course_load.copy(), self._max_terms, self._required, self._max_non_capstones_per_term)
    
    def is_valid(self) -> bool:
        """Checks if the schedule is valid."""
        ordered_terms = sorted(self.course_load.keys())

        if len(ordered_terms) > self._max_terms:
            return False

        # Check if MBA597 is in the first term
        if courses.MBA597 not in self.course_load[ordered_terms[0]]:
            return False
        
        # Check if MBA598 is in the last term
        if self._is_complete and courses.MBA598 not in self.course_load[ordered_terms[-1]]:
            return False

        # Check if all prerequisites are met and if courses are offered in the correct term
        courses_taken: list[courses.Course] = []
        for term_year in ordered_terms:
            term_courses = self.course_load[term_year]
            if self._required and term_year in self._required:
                if not self._required[term_year].issubset(term_courses):
                    return False
            
            # Limit non-capstone courses to 2 per term
            non_capstone_courses = [course for course in term_courses if not is_capstone(course)]
            if len(non_capstone_courses) > self._max_non_capstones_per_term:
                return False

            for course in term_courses:
                if not all(prereq in courses_taken for prereq in course.prerequisites):
                    return False
                if term_year.term not in course.terms_offered:
                    return False
                courses_taken.append(course)

        return True


def is_capstone(course: courses.Course) -> bool:
    return course in courses.CAPSTONES or course in [courses.MBA597, courses.MBA598]


def generate_schedules(
        specializations: list[courses.Specialization], 
        capstones: list[courses.Course],
        required: dict[courses.TermYear, set[courses.Course]], 
        starting_term: courses.TermYear = courses.TermYear(courses.Term.SPRING1, 2025), 
        n_courses_per_semester: int = 3, 
        max_non_capstones_per_term: int = 2, 
        max_terms: int = 10
    ) -> list[Schedule]:
    """Generates all possible schedules."""
    schedules: list[Schedule] = []
    
    all_courses = get_courses(specializations=specializations, capstones=capstones)
    all_courses.remove(courses.MBA597)
    all_courses.remove(courses.MBA598)
    for first_courses in itertools.combinations(all_courses, n_courses_per_semester - 1):
        first_term_courses = {courses.MBA597}.union(first_courses)

        remaining_courses = set(all_courses).difference(first_courses)

        orig_schedule = Schedule({starting_term: first_term_courses}, max_terms=max_terms, required=required, max_non_capstones_per_term=max_non_capstones_per_term)
        if not orig_schedule.is_valid():
            continue

        future_schedules = get_schedules(remaining_courses, n_courses_per_semester, running_schedule=orig_schedule)

        for future_schedule in future_schedules:
            future_schedule.add_course(courses.MBA598, n_courses_per_semester)
            future_schedule.mark_as_complete()
            if future_schedule.is_valid():
                schedules.append(future_schedule)
    return schedules


def get_schedules(remaining_courses: set[courses.Course], n_courses_per_semester: int, running_schedule: Schedule) -> list[Schedule]:
    if len(remaining_courses) <= n_courses_per_semester:
        new_schedule = running_schedule.copy().add_term(remaining_courses)
        return [new_schedule]
    
    results = []
    # for first_result in itertools.combinations(remaining_courses, n_courses_per_semester):
    for first_result in itertools.chain.from_iterable(itertools.combinations(remaining_courses, r) for r in range(2, n_courses_per_semester + 1)):
        new_schedule = running_schedule.copy().add_term(first_result)
        if not new_schedule.is_valid():
            continue
        future_results = get_schedules(remaining_courses.difference(first_result), n_courses_per_semester, new_schedule)
        results.extend([schedule for schedule in future_results if schedule.is_valid()])
    return results


if __name__ == "__main__":
    # Generate all possible schedules

    schedules = generate_schedules(
        specializations=SPECIALIZATIONS, 
        capstones=CAPSTONES, 
        required=REQUIRED, 
        starting_term=courses.TermYear(courses.Term.SPRING1, 2025), 
        n_courses_per_semester=3, 
        max_non_capstones_per_term=2, 
        max_terms=10
    )
    print("Number of valid schedules:", len(schedules))
    print("Schedule 1:")
    print(schedules[0])
