"""LLM prompt templates for workflow nodes.

Centralizes all prompts for easier maintenance and A/B testing.
Each template uses f-string formatting with named placeholders.
"""

KEYWORD_GENERATION_SYSTEM = """\
Generate 3-5 English search keywords for academic paper search.

Requirements:
- Each keyword: 2-4 words, specific enough to filter results
- Cover different angles: core concept, methodology, application domain
- Avoid overly broad single words (e.g. 'learning', 'analysis', 'model')\
"""

KEYWORD_GENERATION_CONTINUATION = """\


This is a follow-up request. Consider the conversation history \
when generating keywords to find additional relevant papers.
Conversation history:
{conversation_context}\
"""

CONTRIBUTION_EXTRACTION_SYSTEM = """\
Extract the paper's core contribution in ONE sentence (15-30 words).
Format: "[Novel method/key finding] that [achieves/enables] [specific outcome]"
If abstract is vague, infer from title. Output in English.
CRITICAL: You MUST return a non-empty string for core_contribution.\
"""

CONTRIBUTION_EXTRACTION_USER = """\
Title: {title}
Year: {year}
Abstract: {abstract}\
"""

DRAFT_GENERATION_SYSTEM = """\
Write a structured literature review with 4-6 thematic sections \
in formal academic {language_name}.

REQUIRED SECTIONS:
1. Introduction/Background - overview of the research area
2-4. Thematic sections - group papers by methodology, approach, or application
5. Methodology Comparison - compare and contrast the methods used across papers \
(include a comparison of strengths, limitations, datasets, and key findings)
6. Conclusion/Future Directions - summarize insights and identify research gaps

CITATION RULES:
- Use {{cite:N}} to reference papers, where N is the number shown \
in brackets in the paper list (1 to {num_papers}).
- Example: "Smith et al. {{cite:1}} proposed X, while Jones {{cite:3}} extended Y."
- You MUST cite ALL {num_papers} papers. Do NOT invent numbers outside 1-{num_papers}.\
"""

DRAFT_REVISION_ADDENDUM = """\


This is a REVISION request. The user wants to modify the existing draft.{existing_draft_summary}
User's modification request: {user_query}

Conversation history:
{conversation_context}

Please revise the draft according to the user's request while maintaining \
proper citations and academic quality.\
"""

DRAFT_RETRY_ADDENDUM = """\


PREVIOUS ATTEMPT FAILED ({error_count} errors). Fix these:
{error_list}
REMINDER: Valid citation numbers are 1 to {num_papers}. \
Use ONLY {{cite:1}} through {{cite:{num_papers}}}. \
Every paper (1-{num_papers}) MUST be cited at least once.\
"""

DRAFT_USER_PROMPT = """\
Research Topic: {user_query}

Papers for Review:
{paper_context}\
"""

OUTLINE_GENERATION_SYSTEM = """\
Create an outline for a literature review on the given topic.

Generate a title and 4-6 section titles that will structure the review.

REQUIRED STRUCTURE:
1. Introduction/Background
2-4. Thematic sections (group by methodology, approach, or application)
5. Methodology Comparison
6. Conclusion/Future Directions

Output section titles in {language_name}. Be specific to the research topic.\
"""

SECTION_GENERATION_SYSTEM = """\
Write the "{section_title}" section of a literature review in {language_name}.

CONTEXT:
- This is section {section_num} of {total_sections}
- Full outline: {outline_titles}

CITATION RULES:
- Use {{cite:N}} to reference papers (N = 1 to {num_papers})
- Cite relevant papers from the list below
- Do NOT invent citation numbers outside 1-{num_papers}

Write 2-4 paragraphs with proper academic tone and citations.\
"""
