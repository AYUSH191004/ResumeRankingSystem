from preprocessing.dataextraction import JobMatcher

class ResumeRanker:
    def __init__(self):
        self.job_matcher = JobMatcher()

    def rank_resumes(self, job_description, resumes):
        required_skills_set = set(job_description.required_skills or [])
        scored_resumes = [
            {
                'resume': resume,
                'skill_score_percentage': self._calculate_skill_match(resume.skills, required_skills_set),
                'overall_score': 0.0  # placeholder
            }
            for resume in resumes
        ]

        for item in scored_resumes:
            skill_score = item['skill_score_percentage'] / 100.0
            exp_score = self._calculate_experience_match(item['resume'].total_experience, job_description.required_experience)
            edu_score = self._calculate_education_match(item['resume'].highest_qualification, job_description.required_education)
            item['overall_score'] = skill_score * 0.4 + exp_score * 0.3 + edu_score * 0.3

        return sorted(scored_resumes, key=lambda x: x['overall_score'], reverse=True)

    def _calculate_overall_score(self, resume, job_description):
        # Weighted scoring
        skill_score = self._calculate_skill_match(resume.skills, job_description.required_skills)
        exp_score = self._calculate_experience_match(resume.total_experience, job_description.required_experience)
        edu_score = self._calculate_education_match(resume.highest_qualification, job_description.required_education)
        return (skill_score * 0.4 + exp_score * 0.3 + edu_score * 0.3)

    def _calculate_skill_match(self, resume_skills, required_skills):
        # Simple skill match score: percentage of matched skills to required skills
        if not required_skills:
            return 0.0
        matched_skills = set(resume_skills).intersection(required_skills)
        return (len(matched_skills) / len(required_skills)) * 100.0

    def _calculate_experience_match(self, resume_experience, required_experience):
        # Simple experience match score: 1 if resume experience >= required, else ratio
        if not required_experience:
            return 0.0
        if resume_experience >= required_experience:
            return 1.0
        return resume_experience / required_experience

    def _calculate_education_match(self, resume_education, required_education):
        # Simple education match: 1 if equal or higher, else 0
        # For simplicity, assume education levels are comparable strings
        education_levels = ['High School', 'Associate', 'Bachelor', 'Master', 'PhD']
        try:
            resume_index = education_levels.index(resume_education)
            required_index = education_levels.index(required_education)
            return 1.0 if resume_index >= required_index else 0.0
        except ValueError:
            return 0.0
