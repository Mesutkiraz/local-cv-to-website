"""
CV Data Models
==============
Structured data models for CV information.
Single Responsibility: Define data structures only.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PersonalInfo:
    """Personal information section of CV."""
    name: str = ""
    title: str = ""
    tagline: str = ""
    bio: str = ""
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None


@dataclass
class Links:
    """Social and professional links."""
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    other: list[str] = field(default_factory=list)


@dataclass
class Experience:
    """Work experience entry."""
    company: str = ""
    role: str = ""
    period: str = ""
    description: str = ""
    highlights: list[str] = field(default_factory=list)


@dataclass
class Project:
    """Project entry."""
    name: str = ""
    description: str = ""
    tech_stack: list[str] = field(default_factory=list)
    link: Optional[str] = None
    type: str = ""


@dataclass
class Education:
    """Education entry."""
    institution: str = ""
    degree: str = ""
    period: str = ""


@dataclass
class Skills:
    """Skills categorized by type."""
    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    specialties: list[str] = field(default_factory=list)


@dataclass
class CVData:
    """
    Complete CV data structure.
    Contains all extracted information from a CV document.
    """
    personal: PersonalInfo = field(default_factory=PersonalInfo)
    links: Links = field(default_factory=Links)
    experience: list[Experience] = field(default_factory=list)
    projects: list[Project] = field(default_factory=list)
    education: list[Education] = field(default_factory=list)
    skills: Skills = field(default_factory=Skills)
    certifications: list[str] = field(default_factory=list)
    languages_spoken: list[str] = field(default_factory=list)
    raw_analysis: Optional[str] = None
    original_cv_text: str = ""
    
    def to_dict(self) -> dict:
        """Convert CVData to dictionary for JSON serialization."""
        return {
            "personal": {
                "name": self.personal.name,
                "title": self.personal.title,
                "tagline": self.personal.tagline,
                "bio": self.personal.bio,
                "email": self.personal.email,
                "phone": self.personal.phone,
                "location": self.personal.location,
            },
            "links": {
                "linkedin": self.links.linkedin,
                "github": self.links.github,
                "website": self.links.website,
                "other": self.links.other,
            },
            "experience": [
                {
                    "company": exp.company,
                    "role": exp.role,
                    "period": exp.period,
                    "description": exp.description,
                    "highlights": exp.highlights,
                }
                for exp in self.experience
            ],
            "projects": [
                {
                    "name": proj.name,
                    "description": proj.description,
                    "tech_stack": proj.tech_stack,
                    "link": proj.link,
                    "type": proj.type,
                }
                for proj in self.projects
            ],
            "education": [
                {
                    "institution": edu.institution,
                    "degree": edu.degree,
                    "period": edu.period,
                }
                for edu in self.education
            ],
            "skills": {
                "languages": self.skills.languages,
                "frameworks": self.skills.frameworks,
                "tools": self.skills.tools,
                "specialties": self.skills.specialties,
            },
            "certifications": self.certifications,
            "languages_spoken": self.languages_spoken,
        }
    
    @classmethod
    def from_dict(cls, data: dict, cv_text: str = "") -> "CVData":
        """Create CVData from dictionary (parsed JSON)."""
        cv = cls()
        cv.original_cv_text = cv_text
        
        # Parse personal info
        if "personal" in data:
            p = data["personal"]
            cv.personal = PersonalInfo(
                name=p.get("name", ""),
                title=p.get("title", ""),
                tagline=p.get("tagline", ""),
                bio=p.get("bio", ""),
                email=p.get("email"),
                phone=p.get("phone"),
                location=p.get("location"),
            )
        
        # Parse links
        if "links" in data:
            l = data["links"]
            cv.links = Links(
                linkedin=l.get("linkedin"),
                github=l.get("github"),
                website=l.get("website"),
                other=l.get("other", []),
            )
        
        # Parse experience
        if "experience" in data:
            cv.experience = [
                Experience(
                    company=exp.get("company", ""),
                    role=exp.get("role", ""),
                    period=exp.get("period", ""),
                    description=exp.get("description", ""),
                    highlights=exp.get("highlights", []),
                )
                for exp in data["experience"]
            ]
        
        # Parse projects
        if "projects" in data:
            cv.projects = [
                Project(
                    name=proj.get("name", ""),
                    description=proj.get("description", ""),
                    tech_stack=proj.get("tech_stack", []),
                    link=proj.get("link"),
                    type=proj.get("type", ""),
                )
                for proj in data["projects"]
            ]
        
        # Parse education
        if "education" in data:
            cv.education = [
                Education(
                    institution=edu.get("institution", ""),
                    degree=edu.get("degree", ""),
                    period=edu.get("period", ""),
                )
                for edu in data["education"]
            ]
        
        # Parse skills
        if "skills" in data:
            s = data["skills"]
            cv.skills = Skills(
                languages=s.get("languages", []),
                frameworks=s.get("frameworks", []),
                tools=s.get("tools", []),
                specialties=s.get("specialties", []),
            )
        
        # Parse lists
        cv.certifications = data.get("certifications", [])
        cv.languages_spoken = data.get("languages_spoken", [])
        
        # Handle raw analysis fallback
        if "raw_analysis" in data:
            cv.raw_analysis = data["raw_analysis"]
        
        return cv
