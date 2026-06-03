from backend.app.ml.parser import pipeline
def test_skill_extractor():
    """Test skill extraction"""
    extractor = pipeline.SkillExtractor()
    
    test_text = """
    Proficient in Python, Java, and C++. Knowledge of machine learning and data analysis. Skilled in SQL and NoSQL databases. Expertise in cloud platforms like AWS and Azure.
    """
    
    result = extractor.extract(test_text)
    
    assert 'Python' in result['all_skills']
    assert 'Java' in result['all_skills']
    assert 'C++' in result['all_skills']
    assert 'machine learning' in result['all_skills']
    assert 'data analysis' in result['all_skills']
    assert 'SQL' in result['all_skills']
    assert 'NoSQL databases' in result['all_skills']
    assert 'AWS' in result['all_skills']
    assert 'Azure' in result['all_skills']
    
    assert 'Programming Languages' in result['by_category']
    assert 'Python' in result['by_category']['Programming Languages']
    
    assert 'Data Science & Analytics' in result['by_category']
    assert 'machine learning' in result['by_category']['Data Science & Analytics']
    
    assert 'Cloud Platforms' in result['by_category']
    assert 'AWS' in result['by_category']['Cloud Platforms']
    
    assert result['count'] == 9
    assert result['confidence'] > 0.8