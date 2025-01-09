from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Final

class Specialization(StrEnum):
    PROGRAM_REQUIREMENTS = "Program Requirements"
    STRATEGIC_LEADERSHIP_AND_MANAGEMENT = "Strategic Leadership and Management"
    MANAGERIAL_ECONOMICS_AND_BUSINESS_ANALYTICS = "Managerial Economics and Business Analytics"
    VALUE_CHAIN_MANAGEMENT = "Value Chain Management"
    FINANCIAL_MANAGEMENT = "Financial Management"
    DIGITAL_MARKETING = "Digital Marketing"
    ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION = "Entrepreneurship and Strategic Innovation"
    GLOBAL_CHALLENGES_IN_BUSINESS = "Global Challenges in Business"
    BUSINESS_ANALYTICS = "Business Analytics"
    MERGERS_AND_ACQUISITIONS = "Mergers and Acquisitions"


class Term(StrEnum):
    FALL1 = "Fall 1"
    FALL2 = "Fall 2"
    SPRING1 = "Spring 1"
    SPRING2 = "Spring 2"
    SUMMER = "Summer"

    def __gt__(self, value):
        order = [Term.SPRING1, Term.SPRING2, Term.SUMMER, Term.FALL1, Term.FALL2]
        return order.index(self) > order.index(value)


class TermYear:
    def __init__(self, term: Term, year: int):
        self.term = term
        self.year = year

    def __str__(self):
        return f"{self.term} {self.year}"
    
    def __repr__(self):
        return str(self)
    
    def __gt__(self, other: TermYear):
        if self.year == other.year:
            return self.term > other.term
        return self.year > other.year
    
    def __hash__(self):
        return hash((self.term, self.year))
    
    def __eq__(self, other: TermYear):
        return self.term == other.term and self.year == other.year
    
    def next_term(self) -> TermYear:
        new_term = {
            Term.FALL1: Term.FALL2,
            Term.FALL2: Term.SPRING1,
            Term.SPRING1: Term.SPRING2,
            Term.SPRING2: Term.SUMMER,
            Term.SUMMER: Term.FALL1,
        }[self.term]
        new_year = self.year + 1 if self.term == Term.FALL2 else self.year
        return TermYear(new_term, new_year)


@dataclass
class Course:
    name: str
    code: str
    specialization: Specialization
    terms_offered: list[Term]
    prerequisites: list[Course] = field(default_factory=list)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.specialization})"

    def __repr__(self):
        return str(self)
    
    def __hash__(self):
        return hash(self.code)
    

# Program Requirements
MBA597 = Course(name="Program Foundations", code="MBA 597", specialization=Specialization.PROGRAM_REQUIREMENTS, terms_offered=[Term.FALL1, Term.FALL2, Term.SPRING1, Term.SPRING2])
MBA598 = Course(name="Program Capstone", code="MBA 598", specialization=Specialization.PROGRAM_REQUIREMENTS, terms_offered=[Term.FALL2, Term.SPRING2, Term.SUMMER])

# Strategic Leadership and Management
BADM508 = Course(name="Leadership and Teams", code="BADM 508", specialization=Specialization.STRATEGIC_LEADERSHIP_AND_MANAGEMENT, terms_offered=[Term.FALL1, Term.SPRING1])
BADM509 = Course(name="Managing Organizations", code="BADM 509", specialization=Specialization.STRATEGIC_LEADERSHIP_AND_MANAGEMENT, terms_offered=[Term.FALL2, Term.SPRING2])
BADM544 = Course(name="Strategic Management", code="BADM 544", specialization=Specialization.STRATEGIC_LEADERSHIP_AND_MANAGEMENT, terms_offered=[Term.SPRING1, Term.SUMMER])
CapstoneSLM = Course(name="Capstone: Strategic Leadership and Management", code="Capstone Core 1", specialization=Specialization.STRATEGIC_LEADERSHIP_AND_MANAGEMENT, terms_offered=[Term.SPRING2, Term.SUMMER], prerequisites=[BADM508, BADM509, BADM544])

# Managerial Economics and Business Analytics
BADM572 = Course(name="Statistics Management Decision Making", code="BADM 572", specialization=Specialization.MANAGERIAL_ECONOMICS_AND_BUSINESS_ANALYTICS, terms_offered=[Term.FALL1, Term.SPRING1])
FIN574 = Course(name="Microeconomics for Business", code="FIN 574", specialization=Specialization.MANAGERIAL_ECONOMICS_AND_BUSINESS_ANALYTICS, terms_offered=[Term.FALL2,Term.SPRING2])
FIN571 = Course(name="Money and Banking", code="FIN 571", specialization=Specialization.MANAGERIAL_ECONOMICS_AND_BUSINESS_ANALYTICS, terms_offered=[Term.SPRING1, Term.SUMMER])
CapstoneMEBA = Course(name="Capstone: Managerial Economics and Business Analytics", code="Capstone Core 2", specialization=Specialization.MANAGERIAL_ECONOMICS_AND_BUSINESS_ANALYTICS, terms_offered=[Term.SPRING2, Term.SUMMER], prerequisites=[BADM572, FIN574, FIN571])

# Value Chain Management
BADM520 = Course(name="Marketing Management", code="BADM 520", specialization=Specialization.VALUE_CHAIN_MANAGEMENT, terms_offered=[Term.FALL1, Term.SPRING1])
BADM567 = Course(name="Operations Management", code="BADM 567", specialization=Specialization.VALUE_CHAIN_MANAGEMENT, terms_offered=[Term.SPRING1, Term.SUMMER])
ACCY503 = Course(name="Managerial Accounting", code="ACCY 503", specialization=Specialization.VALUE_CHAIN_MANAGEMENT, terms_offered=[Term.FALL2, Term.SPRING2])
CapstoneVCM = Course(name="Capstone: Value Chain Management", code="Capstone Core 3", specialization=Specialization.VALUE_CHAIN_MANAGEMENT, terms_offered=[Term.SPRING2, Term.SUMMER], prerequisites=[BADM520, BADM567, ACCY503])

# Financial Management
ACCY500 = Course(name="Accounting Measurement, Reporting, and Control (Financial Accounting)", code="ACCY 500", specialization=Specialization.FINANCIAL_MANAGEMENT, terms_offered=[Term.FALL1, Term.SPRING1])
FIN511 = Course(name="Investments", code="FIN 511", specialization=Specialization.FINANCIAL_MANAGEMENT, terms_offered=[Term.FALL2, Term.SPRING2], prerequisites=[ACCY500])
FIN570 = Course(name="Corporate Finance", code="FIN 570", specialization=Specialization.FINANCIAL_MANAGEMENT, terms_offered=[Term.SPRING1,Term.SUMMER], prerequisites=[ACCY500])
CapstoneFM = Course(name="Capstone: Financial Management", code="Capstone Core 4", specialization=Specialization.FINANCIAL_MANAGEMENT, terms_offered=[Term.SPRING2, Term.SUMMER], prerequisites=[ACCY500, FIN511, FIN570])

# Digital Marketing
MBA542 = Course(name="Digital Marketing Analytics", code="MBA 542", specialization=Specialization.DIGITAL_MARKETING, terms_offered=[Term.SUMMER])
MBA543 = Course(name="Digital Media and Marketing", code="MBA 543", specialization=Specialization.DIGITAL_MARKETING, terms_offered=[Term.FALL1, Term.SPRING1])
MBA545 = Course(name="Marketing in Our New Digital World", code="MBA 545", specialization=Specialization.DIGITAL_MARKETING, terms_offered=[Term.SPRING2])
CapstoneDM = Course(name="Capstone: Digital Marketing", code="Capstone Focus 1", specialization=Specialization.DIGITAL_MARKETING, terms_offered=[Term.FALL2], prerequisites=[MBA542, MBA543, MBA545])

# Entrepreneurship and Strategic Innovation
MBA551 = Course(name="Strategic Innovation", code="MBA 551", specialization=Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION, terms_offered=[Term.SPRING2])
MBA552 = Course(name="Fostering Creative Thinking", code="MBA 552", specialization=Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION, terms_offered=[Term.SUMMER], prerequisites=[MBA551])
MBA553 = Course(name="Entrepreneurship: From Startup to Growth", code="MBA 553", specialization=Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION, terms_offered=[Term.FALL1], prerequisites=[MBA551, MBA552])
CapstoneESI = Course(name="Capstone: Entrepreneurship and Strategic Innovation", code="Capstone Focus 2", specialization=Specialization.ENTREPRENEURSHIP_AND_STRATIGIC_INNOVATION, terms_offered=[Term.FALL2], prerequisites=[MBA551, MBA552, MBA553])

# Global Challenges in Business
MBA547 = Course(name="Global Marketing", code="MBA 547", specialization=Specialization.GLOBAL_CHALLENGES_IN_BUSINESS, terms_offered=[Term.SUMMER])
MBA548 = Course(name="Global Strategy", code="MBA 548", specialization=Specialization.GLOBAL_CHALLENGES_IN_BUSINESS, terms_offered=[Term.SPRING2])
MBA549 = Course(name="Multiculturalism in Management and the Marketplace", code="MBA 549", specialization=Specialization.GLOBAL_CHALLENGES_IN_BUSINESS, terms_offered=[Term.FALL1])
CapstoneGCB = Course(name="Capstone: Global Challenges in Business", code="Capstone Focus 3", specialization=Specialization.GLOBAL_CHALLENGES_IN_BUSINESS, terms_offered=[Term.FALL2], prerequisites=[MBA547, MBA548, MBA549])

# Business Analytics
MBA561 = Course(name="Introduction to Business Analytics with R", code="MBA 561", specialization=Specialization.BUSINESS_ANALYTICS, terms_offered=[Term.FALL1])
MBA562 = Course(name="Introduction to Business Analytics: Communicating with Data", code="MBA 562", specialization=Specialization.BUSINESS_ANALYTICS, terms_offered=[Term.FALL1])
MBA563 = Course(name="Data Toolkit: Business Data Modeling and Predictive Analytics", code="MBA 563", specialization=Specialization.BUSINESS_ANALYTICS, terms_offered=[Term.FALL2])
MBA564 = Course(name="Special Topics 1 & 2", code="MBA 564", specialization=Specialization.BUSINESS_ANALYTICS, terms_offered=[Term.SPRING1])

# Mergers and Acquisitions
FIN572 = Course(name="Finance of Mergers and Acquisitions", code="FIN 572", specialization=Specialization.MERGERS_AND_ACQUISITIONS, terms_offered=[Term.FALL1], prerequisites=[FIN570, ACCY500])
ACCY532 = Course(name="Mergers and Acquisitions and Other Complex Transactions", code="ACCY 532", specialization=Specialization.MERGERS_AND_ACQUISITIONS, terms_offered=[Term.FALL2], prerequisites=[FIN570, ACCY500])
FIN573 = Course(name="Investment Banking Concepts", code="FIN 573", specialization=Specialization.MERGERS_AND_ACQUISITIONS, terms_offered=[Term.SPRING1], prerequisites=[FIN570, ACCY500, FIN572, ACCY532])

# Capstones
CAPSTONES: Final = [CapstoneSLM, CapstoneMEBA, CapstoneVCM, CapstoneFM, CapstoneDM, CapstoneESI, CapstoneGCB]
