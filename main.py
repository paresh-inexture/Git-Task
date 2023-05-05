import csv
import subprocess

from github import Github
import os
from git import Repo


class GitClone:
    def __init__(self, user, clone_directory, cloc_output_file, repositories):
        self.user = user
        self.clone_directory = clone_directory
        self.cloc_output_file = cloc_output_file
        self.repositories = repositories

    def clone_project(self):
        # Loop through all the repositories owned by the user and clone them
        for repo in self.user.get_repos():
            if repo.name not in self.repositories.keys():
                continue
            repo_directory = os.path.join(self.clone_directory, repo.name)
            if not os.path.exists(repo_directory):
                repo_url_with_token = repo.clone_url.replace("https://", f"https://{GITHUB_ACCESS_TOKEN}@")
                print(f'Cloning {repo.full_name} to {repo_directory}')
                Repo.clone_from(url=repo_url_with_token, to_path=repo_directory)
                self.add_data_into_csv(repo_directory, repo)
            else:
                self.add_data_into_csv(repo_directory, repo)
                print(f'{repo.full_name} already exists in {repo_directory}')

    def add_data_into_csv(self, repo_directory, repo=None):
        cloc_output = subprocess.check_output(["cloc", "--csv", repo_directory])

        cloc_output_lines = cloc_output.decode().split("\n")
        for line in cloc_output_lines:
            if "files" in line.split(','):
                index = cloc_output_lines.index(line)
                break
        # Append results to output CSV file
        with open(self.cloc_output_file, "a") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                # Write the header row if the file is empty
                writer.writerow(["REPO_NAME", "URL", "LANGUAGE","FILES","BLANK","COMMENT","CODE"])
            for row in cloc_output_lines[index+1:-1]:
                writer.writerow([repo.name, repo.clone_url,row.split(',')[1],row.split(',')[0],row.split(',')[2],row.split(',')[3],row.split(',')[4]])

if __name__ == '__main__':
    USERNAME = 'paresh-inexture'

    # Replace with your GitHub access token
    GITHUB_ACCESS_TOKEN = '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'

    # Replace with the directory where you want to store the cloned repositories
    CLONE_DIRECTORY = '/home/root362/Documents/Test_Git_Clone'

    g = Github(login_or_token=GITHUB_ACCESS_TOKEN)

    # Get the user object
    USER = g.get_user()

    CLOC_OUTPUT_FILE = "lines_of_code.csv"
    REPOSITORIES = {
                    "test_CI-CD": "https://github.com/anujsahatpure/test_CI-CD.git"
                    }
    git_object = GitClone(USER, CLONE_DIRECTORY, CLOC_OUTPUT_FILE, REPOSITORIES)
    git_object.clone_project()
