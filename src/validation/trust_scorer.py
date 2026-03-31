def compute_trust_score(dist, corr, util):

    score = 0.4*dist + 0.3*corr + 0.3*util

    level = "High Trust" if score>0.9 else "Moderate" if score>0.75 else "Low"

    return round(score,3), level