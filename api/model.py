import pandas as pd
import numpy as np

from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import issparse

inv = pd.read_csv("./investors.csv")
project_df = pd.read_csv("./projects.csv")


def get_investor_similarities(project_description, investor_descriptions):
    """
  This function calculates the cosine similarity between a project description and multiple investor descriptions,
  returning a nested dictionary where outer keys are investor indices, and inner dictionaries contain all project indices
  with corresponding similarity scores sorted in descending order.

  Args:
      project_description: The description of the project.
      investor_descriptions: A list of investor descriptions.

  Returns:
      A nested dictionary with outer keys as investor indices and inner dictionaries containing project indices
      (sorted by descending similarity) as keys and corresponding similarity scores as values.
  """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([project_description] + investor_descriptions)
    project_tfidf = tfidf_matrix[0]

    # Create a defaultdict to store similarities for each investor
    all_similarities = defaultdict(dict)

    # Calculate similarity for each investor
    for investor_idx, investor_description in enumerate(investor_descriptions):
        investor_tfidf = tfidf_matrix[investor_idx + 1]  # Skip project description (index 0)
        investor_similarity = project_tfidf.dot(investor_tfidf.T)[0]
        all_similarities[investor_idx][
            investor_idx] = investor_similarity  # Add similarity for own project (may be non-zero)

        # Calculate similarities for other projects
        for project_idx in range(1, len(investor_descriptions)):
            other_project_tfidf = tfidf_matrix[project_idx + 1]  # Skip project and own investor description
            other_similarity = project_tfidf.dot(other_project_tfidf.T)[0]
            all_similarities[investor_idx][project_idx] = other_similarity

    # Sort similarities for each investor in descending order (based on similarity)
    for investor_idx, project_similarities in all_similarities.items():
        sorted_similarities = dict(sorted(project_similarities.items(), key=lambda item: item[1], reverse=True))
        all_similarities[investor_idx] = sorted_similarities

    return all_similarities  # Return nested dictionary containing sorted similarities for all investors


# Example usage (assuming project_df and investor_descriptions are available)
all_project_similarities = {}
for idx, project_row in project_df.iterrows():
    project_description = project_row["project_description"]
    investor_similarities = get_investor_similarities(project_description, investor_descriptions)
    all_project_similarities.update(investor_similarities)  # Update with similarities for all projects

# Print the nested dictionary (sorted similarities)
print("Nested Dictionary with Sorted Similarities:")
for investor_idx, project_similarities in all_project_similarities.items():
    print(f"\nInvestor {investor_idx + 1} Similarities (Descending Order):")
    for project_idx, score in project_similarities.items():
        print(f"  Project {project_idx + 1}: {score}")  # Adjust for 1-based indexing


def best_match_for_investor(investor_id: int):
    temp: dict = all_project_similarities[investor_id]
    for temporary in temp:
        project_list = temp[temporary]
