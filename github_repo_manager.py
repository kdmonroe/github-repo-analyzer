from github import Github, GithubException
import pandas as pd

class GithubRepoManager:
    def __init__(self, token):
        self.g = Github(token)
        self.user = self.g.get_user()
        self.all_repos = list(self.user.get_repos(type='all', sort='updated', direction='desc'))

    def count_and_print_repos(self):
        try:
            print(f"Authenticated as: {self.user.login}")
            
            # Detailed counts
            total_count = len(self.all_repos)
            fork_count = len([repo for repo in self.all_repos if repo.fork])
            non_fork_count = total_count - fork_count
            archived_count = len([repo for repo in self.all_repos if repo.archived])
            non_archived_count = total_count - archived_count
            public_count = len([repo for repo in self.all_repos if not repo.private])
            private_count = len([repo for repo in self.all_repos if repo.private])
            org_count = len([repo for repo in self.all_repos if repo.owner.login != self.user.login])
            owned_count = total_count - org_count

            print("Repository Statistics:")
            print(f"  1. Total repositories: {total_count}")
            print(f"  2. Repositories owned by {self.user.login}: {owned_count}")
            print(f"  3. Forked repositories: {fork_count}")
            print(f"  4. Non-fork repositories: {non_fork_count}")
            print(f"  5. Archived repositories: {archived_count}")
            print(f"  6. Non-archived repositories: {non_archived_count}")
            print(f"  7. Public repositories: {public_count}")
            print(f"  8. Private repositories: {private_count}")
            print(f"  9. Repositories from organizations: {org_count}")

            print("\nDetailed Repository Information:")
            for i, repo in enumerate(self.all_repos, 1):
                print(f"  {i}. Name: {repo.name}")
                print(f"     Owner: {repo.owner.login}")
                print(f"     Fork: {repo.fork}")
                print(f"     Archived: {repo.archived}")
                print(f"     Private: {repo.private}")
                print()  # Add an empty line between repos for better readability

        except GithubException as e:
            if e.status == 401:
                print("Authentication failed. Please check your GitHub token.")
                print("Make sure the token has the necessary permissions (repo scope).")
            else:
                print(f"An error occurred: {e}")

    def get_repo_stats(self):
        total_count = len(self.all_repos)
        fork_count = len([repo for repo in self.all_repos if repo.fork])
        non_fork_count = total_count - fork_count
        archived_count = len([repo for repo in self.all_repos if repo.archived])
        non_archived_count = total_count - archived_count
        public_count = len([repo for repo in self.all_repos if not repo.private])
        private_count = len([repo for repo in self.all_repos if repo.private])
        org_count = len([repo for repo in self.all_repos if repo.owner.login != self.user.login])
        owned_count = total_count - org_count

        return {
            "Total Repositories": total_count,
            f"Owned by {self.user.login}": owned_count,
            "Forked": fork_count,
            "Non-fork": non_fork_count,
            "Archived": archived_count,
            "Non-archived": non_archived_count,
            "Public": public_count,
            "Private": private_count,
            "From Organizations": org_count
        }

    def get_repos_dataframe(self):
        try:
            data = []
            for repo in self.all_repos:
                data.append({
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'language': repo.language,
                    'stars': repo.stargazers_count,
                    'forks': repo.forks_count,
                    'is_fork': repo.fork,
                    'is_archived': repo.archived,
                    'is_private': repo.private,
                    'created_at': repo.created_at,
                    'updated_at': repo.updated_at,
                    'url': repo.html_url,
                    'owner': repo.owner.login,
                    'is_owner': repo.owner.login == self.user.login
                })
            return pd.DataFrame(data)
        except GithubException as e:
            print(f"An error occurred: {e}")
            return None

    def get_recent_repos(self, limit=10):
        return sorted(self.all_repos, key=lambda r: r.updated_at, reverse=True)[:limit]

    def get_repo_commits(self, repo, limit=5):
        try:
            return list(repo.get_commits()[:limit])
        except GithubException as e:
            if e.status == 409:  # Empty repository
                return []
            else:
                raise e

    def delete_repo(self, repo_name):
        repo = self.user.get_repo(repo_name)
        repo.delete()
        self.refresh_repos()  # Refresh the list of repositories after deletion

    def refresh_repos(self):
        self.all_repos = list(self.user.get_repos(type='all', sort='updated', direction='desc'))


    def get_starred_repos(self):
        starred_repos = list(self.user.get_starred())
        starred_data = []
        for repo in starred_repos:
            starred_data.append({
                'name': repo.name,
                'owner': repo.owner.login,
                'language': repo.language or 'Unknown',
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'url': repo.html_url,
                'description': repo.description
            })
        return pd.DataFrame(starred_data)

    def create_repo(self, name, description=None, private=False, auto_init=False, gitignore_template=None, license_template=None):
        kwargs = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": auto_init,
        }
        
        if gitignore_template:
            kwargs["gitignore_template"] = gitignore_template
        
        if license_template:
            kwargs["license_template"] = license_template
        
        return self.g.get_user().create_repo(**kwargs)

    def __del__(self):
        if hasattr(self, 'g'):
            self.g.close()