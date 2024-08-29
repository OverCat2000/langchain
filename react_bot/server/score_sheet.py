def calculate_extroversion(answers):
    """
    Calculate the Extroversion score based on the provided answers.
    
    Args:
    - answers (dict): Dictionary containing answers with question numbers as keys.
    
    Returns:
    - int: Calculated Extroversion score.
    """
    E = (20 + 
         answers[1] - 
         answers[6] + 
         answers[11] - 
         answers[16] + 
         answers[21] - 
         answers[26] + 
         answers[31] - 
         answers[36] + 
         answers[41] - 
         answers[46])
    return E

def calculate_agreeableness(answers):
    """
    Calculate the Agreeableness score based on the provided answers.
    
    Args:
    - answers (dict): Dictionary containing answers with question numbers as keys.
    
    Returns:
    - int: Calculated Agreeableness score.
    """
    A = (14 - 
         answers[2] + 
         answers[7] - 
         answers[12] + 
         answers[17] - 
         answers[22] + 
         answers[27] - 
         answers[32] + 
         answers[37] + 
         answers[42] + 
         answers[47])
    return A

def calculate_conscientiousness(answers):
    """
    Calculate the Conscientiousness score based on the provided answers.
    
    Args:
    - answers (dict): Dictionary containing answers with question numbers as keys.
    
    Returns:
    - int: Calculated Conscientiousness score.
    """
    C = (14 + 
         answers[3] - 
         answers[8] + 
         answers[13] - 
         answers[18] + 
         answers[23] - 
         answers[28] + 
         answers[33] - 
         answers[38] + 
         answers[43] + 
         answers[48])
    return C

def calculate_neuroticism(answers):
    """
    Calculate the Neuroticism score based on the provided answers.
    
    Args:
    - answers (dict): Dictionary containing answers with question numbers as keys.
    
    Returns:
    - int: Calculated Neuroticism score.
    """
    N = (38 - 
         answers[4] + 
         answers[9] - 
         answers[14] + 
         answers[19] - 
         answers[24] - 
         answers[29] - 
         answers[34] - 
         answers[39] - 
         answers[44] - 
         answers[49])
    return N

def calculate_openness(answers):
    """
    Calculate the Openness to Experience score based on the provided answers.
    
    Args:
    - answers (dict): Dictionary containing answers with question numbers as keys.
    
    Returns:
    - int: Calculated Openness to Experience score.
    """
    O = (8 + 
         answers[5] - 
         answers[10] + 
         answers[15] - 
         answers[20] + 
         answers[25] - 
         answers[30] + 
         answers[35] + 
         answers[40] + 
         answers[45] + 
         answers[50])
    return O

# Example usage
answers = {
    1: 1, 2: 1, 3: 5, 4: 4, 5: 5, 6: 4, 7: 4, 8: 1, 9: 2, 10: 1,
    11: 3, 12: 1, 13: 5, 14: 5, 15: 2, 16: 5, 17: 5, 18: 1, 19: 4, 20: 2,
    21: 4, 22: 3, 23: 4, 24: 2, 25: 5, 26: 1, 27: 5, 28: 2, 29: 4, 30: 1,
    31: 2, 32: 3, 33: 5, 34: 3, 35: 5, 36: 5, 37: 3, 38: 1, 39: 2, 40: 4,
    41: 1, 42: 5, 43: 5, 44: 3, 45: 5, 46: 4, 47: 4, 48: 5, 49: 2, 50: 5
}

print("Extroversion score:", calculate_extroversion(answers))
print("Agreeableness score:", calculate_agreeableness(answers))
print("Conscientiousness score:", calculate_conscientiousness(answers))
print("Neuroticism score:", calculate_neuroticism(answers))
print("Openness to Experience score:", calculate_openness(answers))
