import re

def extract_keywords_from_jd(jd_text):
    jd_text = jd_text.lower()
    
    # Simple list of expected skills/keywords
    keywords = [
        'python', 'java', 'c++', 'html', 'css', 'javascript',
        'react', 'node.js', 'aws', 'azure', 'git', 'sql', 'mongodb',
        'docker', 'kubernetes', 'tensorflow', 'pandas', 'numpy',
        'linux', 'rest', 'graphql', 'agile', 'scrum', 'figma'
    ]
    
    found_keywords = set()

    for word in keywords:
        if re.search(r'\b' + re.escape(word) + r'\b', jd_text):
            found_keywords.add(word)

    return list(found_keywords)
