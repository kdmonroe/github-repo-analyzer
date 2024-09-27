import os
import argparse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from github_repo_manager import GithubRepoManager
from pathlib import Path


def export_data(repo_manager, format, output):
    df = repo_manager.get_repos_dataframe()
    if format == 'csv':
        df.to_csv(output, index=False)
    elif format == 'xlsx':
        df.to_excel(output, index=False)
    print(f"Data exported to {output}")

def export_stars(repo_manager, format, output):
    starred_df = repo_manager.get_starred_repos()
    if format == 'csv':
        starred_df.to_csv(output, index=False)
    elif format == 'xlsx':
        starred_df.to_excel(output, index=False)
    print(f"Starred repositories exported to {output}")

def visualize(repo_manager, type, output):
    df = repo_manager.get_repos_dataframe()
    if type == 'language_distribution':
        lang_counts = df['language'].value_counts()
        fig = px.pie(values=lang_counts.values, names=lang_counts.index, title="Language Distribution")
    elif type == 'stars_vs_forks':
        fig = px.scatter(df, x="stars", y="forks", hover_name="name", title="Stars vs. Forks")
    elif type == 'creation_timeline':
        fig = px.histogram(df, x="created_at", title="Repository Creation Timeline")
    else:
        print(f"Unknown visualization type: {type}")
        return

    fig.write_image(output)
    print(f"Visualization saved to {output}")

def load_token_from_env():
    current_dir = Path(__file__).resolve().parent
    # Set the path to the token.env file
    env_path = current_dir / 'token.env'
    if env_path.exists():
        load_dotenv(env_path)
        return os.getenv('GITHUB_TOKEN')
    return None

def main():
    token = load_token_from_env()
    if not token:
        print("GitHub token not found. Please set up your token in token.env file.")
        return

    parser = argparse.ArgumentParser(description="GitHub Repository Analyzer CLI")
    parser.add_argument('action', choices=['stats', 'list', 'create', 'delete', 'export', 'stars', 'visualize'])
    parser.add_argument('--name', help="Repository name for create/delete actions")
    parser.add_argument('--description', help="Repository description for create action")
    parser.add_argument('--private', action='store_true', help="Make repository private (for create action)")
    parser.add_argument('--format', choices=['csv', 'xlsx'], help="Export format for data/stars")
    parser.add_argument('--output', help="Output file name for export/visualize actions")
    parser.add_argument('--type', choices=['language_distribution', 'stars_vs_forks', 'creation_timeline'], help="Visualization type")

    args = parser.parse_args()

    repo_manager = GithubRepoManager(token)

    if args.action == 'stats':
        stats = repo_manager.get_repo_stats()
        for key, value in stats.items():
            print(f"{key}: {value}")
    elif args.action == 'list':
        repos = repo_manager.all_repos
        for repo in repos:
            print(f"{repo.name} - {repo.description}")
    elif args.action == 'create':
        if not args.name:
            print("Repository name is required for create action")
            return
        repo = repo_manager.create_repo(args.name, description=args.description, private=args.private)
        print(f"Repository created: {repo.html_url}")
    elif args.action == 'delete':
        if not args.name:
            print("Repository name is required for delete action")
            return
        repo_manager.delete_repo(args.name)
        print(f"Repository {args.name} deleted")
    elif args.action == 'export':
        if not args.format or not args.output:
            print("Format and output file name are required for export action")
            return
        export_data(repo_manager, args.format, args.output)
    elif args.action == 'stars':
        if not args.format or not args.output:
            print("Format and output file name are required for stars action")
            return
        export_stars(repo_manager, args.format, args.output)
    elif args.action == 'visualize':
        if not args.type or not args.output:
            print("Visualization type and output file name are required for visualize action")
            return
        visualize(repo_manager, args.type, args.output)

if __name__ == "__main__":
    main()