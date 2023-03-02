import pandas as pd
import json


STATUS_LABELS = [
  "Not yet started",
  "In progress",
  "Looking for collaborators",
  "Meets FAIR criteria!",
]

FILE_PATH = "data/models.csv"


class Issue():
  def __init__(self, title=None, url="", status=STATUS_LABELS[0]):
    self.title = title
    self.url = url
    self.status = status


def get_issues():
  response = input()
  data = json.loads(response)
  issues = []
  for gh_issue in data:
    issue = Issue(title=gh_issue["title"], url=gh_issue["html_url"])
    for label in gh_issue["labels"]:
      if label["name"] in STATUS_LABELS:
        issue.status = label["name"]
    issues.append(issue)
  return issues


def update_csv(issues):
  df = pd.read_csv(FILE_PATH)
  for index, row in df.iterrows():
    for issue in issues:
      if row["name_short"] == issue.title:
        df.loc[index, "status"] = issue.status
        df.loc[index, "issue_link"] = issue.url
        break
    else:
      df.loc[index, "status"] = STATUS_LABELS[0]
      df.loc[index, "issue_link"] = ""
  df.to_csv(FILE_PATH, index=False)


def main():
  issues = get_issues()
  update_csv(issues)

if __name__ == "__main__":
  main()
