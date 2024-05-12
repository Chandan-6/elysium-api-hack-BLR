import pandas as pd
import numpy as np

inv = pd.read_csv("investors.csv")
project_df = pd.read_csv("projects.csv")


def get_investor_similarities(project_description, investor_descriptions):
    """
  This function calculates the cosine similarity between a project description and multiple investor descriptions,
  returning similarities in a nested array format.

  Args:
      project_description: The description of the project.
      investor_descriptions: A list of investor descriptions.

  Returns:
      A nested list containing cosine similarity scores for each investor description compared to the project description.
  """
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([project_description] + investor_descriptions)
    project_tfidf = tfidf[0]
    investor_similarities = project_tfidf.dot(tfidf.T).toarray()[0][1:]

    # Wrap investor_similarities in another list for nested structure
    return [[investor_similarities]]  # Outer list contains similarities for one project


# Example usage remains the same


def similarities(ID: int):
    for idx, project_row in project_df.iterrows():
        project_description = project_row["project_description"]
        investor_similarities = get_investor_similarities(project_description, investor_descriptions)

        # Access investor similarities for the current project: investor_similarities[0] (the first element in the outer list)
        print(f"Similarities for project description (index {idx}): {investor_similarities[0]}")

        # You can further iterate through investor_similarities[0] to access individual scores
        for i in range(len(investor_similarities[0])):
            print(f"Similarity for investor {i}: {investor_similarities[0][i]}")
        return investor_similarities[0][ID]
