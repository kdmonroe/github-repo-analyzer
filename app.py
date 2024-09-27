import streamlit as st
from streamlit_option_menu import option_menu
from github_repo_manager import GithubRepoManager
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from github import GithubException

COLORS = {
    'total': '#7C9EFF',  # Soft indigo
    'owned': '#80DEEA',  # Muted cyan
    'public': '#FFD54F',  # Soft amber
    'private': '#AED581',  # Muted light green
    'forked': '#FF8A65',  # Soft deep orange
    'archived': '#B39DDB'  # Muted deep purple
}

def load_token_from_env():
    env_path = os.path.join(os.path.dirname(__file__), 'token.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        return os.getenv('GITHUB_TOKEN')
    return None

def create_summary(repo_manager, stats):
    username = repo_manager.user.login
    return f"""
    Successfully authenticated as GitHub user: **{username}**
    
    Found a total of <span style='color:{COLORS['total']};font-weight:bold;'>{stats["Total Repositories"]}</span> repositories, of which <span style='color:{COLORS['owned']};font-weight:bold;'>{stats[f"Owned by {username}"]}</span> are owned by {username}.
    This includes <span style='color:{COLORS['public']};font-weight:bold;'>{stats['Public']}</span> public and <span style='color:{COLORS['private']};font-weight:bold;'>{stats['Private']}</span> private repositories.
    
    Among these, there are <span style='color:{COLORS['forked']};font-weight:bold;'>{stats['Forked']}</span> forked repositories and <span style='color:{COLORS['archived']};font-weight:bold;'>{stats['Archived']}</span> archived repositories.
    """

def format_dataframe(df, format_owned):
    def highlight_owned(row):
        if format_owned:
            color = '#e6f3ff' if row['is_owner'] else '#fff0e6'
            return [f'background-color: {color}' for _ in row]
        return ['' for _ in row]
    return df.style.apply(highlight_owned, axis=1)

def format_datetime(dt):
    return dt.strftime("%b %d, %Y %I:%M %p")

def delete_repository(repo_manager):
    st.header("Delete Repository")
    
    # Get list of repositories
    repos = repo_manager.all_repos
    repo_names = [repo.name for repo in repos if repo.permissions.admin]
    
    # Dropdown to select repository
    selected_repo = st.selectbox("Select a repository to delete:", repo_names)
    
    if selected_repo:
        st.warning(f"You are about to delete the repository: {selected_repo}")
        st.write("This action cannot be undone. Please type the repository name to confirm.")
        
        # Text input for confirmation
        confirmation = st.text_input("Type the repository name to confirm deletion:")
        
        if st.button("Delete Repository"):
            if confirmation == selected_repo:
                try:
                    repo_manager.delete_repo(selected_repo)
                    st.success(f"Repository {selected_repo} has been deleted successfully.")
                except GithubException as e:
                    st.error(f"An error occurred while deleting the repository: {str(e)}")
            else:
                st.error("Confirmation does not match the repository name. Deletion aborted.")

def export_to_csv(data, filename):
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename_with_date = f"{current_date}_{filename}"
    csv_file = data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv_file,
        file_name=filename_with_date,
        mime="text/csv"
    )

def get_all_commits(repo_manager, repos):
    all_commits = []
    for repo in repos:
        commits = repo_manager.get_repo_commits(repo)
        for commit in commits:
            all_commits.append({
                'repo': repo.name,
                'message': commit.commit.message,
                'date': commit.commit.author.date,
                'author': commit.commit.author.name,
                'url': commit.html_url
            })
    return pd.DataFrame(all_commits)

def create_repository(repo_manager):
    st.header("Create New Repository")
    
    st.write("""
    This section allows you to create a new GitHub repository directly from the app. 
    You can specify the repository name, description, visibility, and other options. 
    The app uses the GitHub API to create the repository based on your input.
    """)
    
    # Form for repository details
    with st.form("create_repo_form"):
        repo_name = st.text_input("Repository Name", help="Enter the name for your new repository")
        description = st.text_area("Description", value="This repo was created by Github Streamlit!", help="Provide a brief description of your repository")
        private = st.checkbox("Private Repository", help="Check this if you want the repository to be private")
        auto_init = st.checkbox("Initialize with README", help="Check this to initialize the repository with a README file")
        
        # Optional fields
        with st.expander("Advanced Options"):
            gitignore_template = st.text_input("Gitignore Template", help="Enter the name of a gitignore template (e.g., 'Python', 'Node')")
            license_template = st.text_input("License Template", help="Enter the name of a license template (e.g., 'mit', 'gpl-3.0')")
        
        submitted = st.form_submit_button("Create Repository")
        
    if submitted:
        try:
            new_repo = repo_manager.create_repo(
                name=repo_name,
                description=description,
                private=private,
                auto_init=auto_init,
                gitignore_template=gitignore_template if gitignore_template else None,
                license_template=license_template if license_template else None
            )
            st.success(f"Repository '{repo_name}' created successfully! URL: {new_repo.html_url}")
        except GithubException as e:
            st.error(f"An error occurred while creating the repository: {str(e)}")

def initialize_repo_manager():
    token = load_token_from_env()
    if not token:
        return None, "GitHub token not found. Please set up your token."
    try:
        repo_manager = GithubRepoManager(token)
        return repo_manager, None
    except Exception as e:
        return None, f"Error initializing GitHub connection: {str(e)}"

def main():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #f3e7e9, #e3eeff);
    }
    </style>
    """, unsafe_allow_html=True)

    repo_manager, error = initialize_repo_manager()
    if error:
        st.error(error)
        st.info("See the 'Need help?' section above for instructions on how to create and set up your GitHub token.")
        return

    user = repo_manager.user
    
    # Help tooltip
    with st.expander("❓ Need help?"):
        st.write("""
        This app allows you to manage and visualize your GitHub repositories efficiently using [PytGithub](https://pygithub.readthedocs.io/en/latest/) and [Streamlit](https://streamlit.io/). It's designed to help you manage your GitHub repositories, track your activity, and visualize your data in a user-friendly way. Here's what each section does:
        - **Stats 📊**: Overview of your GitHub repositories.
        - **Activity 🕒**: Recent commits and repository updates.
        - **Data 📁**: Detailed information about your repositories.
        - **Visualize 📈**: Graphs and charts of your GitHub data.
        - **Stars ⭐**: Information about your starred repositories.
        - **Create 🆕**: Create new repositories using the GitHub API.
        - **Delete 🗑️**: Option to delete repositories (use with caution).
        
        To use this app, you need to set up a GitHub Personal Access Token. Here's how:
        1. Go to your GitHub account settings.
        2. Click on "Developer settings" in the left sidebar.
        3. Select "Personal access tokens" and then "Tokens (classic)".
        4. Click "Generate new token" and select "Generate new token (classic)".
        5. Give your token a descriptive name.
        6. Select the following scopes:
           - `repo` (Full control of private repositories)
           - `delete_repo` (Delete repositories)
           - `read:user` (Read all user profile data)
           - `user:email` (Access user email addresses (read-only))
        7. Click "Generate token" at the bottom of the page.
        8. Copy the generated token and store it securely.
        9. If using this app through the web, provide the token in the input field above. If using the CLI, the token should be in the `.env` file in the root directory. Your file should look like this:
        ```env
        GITHUB_TOKEN=your_github_token
        ```
        
        Remember to keep your token secret and never share it publicly!
        """)

    # Sidebar with user info
    with st.sidebar:
        st.image(user.avatar_url, width=100)
        st.write(f"Welcome, **{user.name}**!")
        
        selected = option_menu(
            menu_title="Main Menu",
            options=["Stats 📊", "Activity 🕒", "Data 📁", "Visualize 📈", "Stars ⭐", "Create 🆕", "Delete 🗑️"],
            icons=["graph-up", "clock-history", "folder", "bar-chart", "star", "plus-circle", "trash"],
            # menu_icon="cast",
            default_index=0,
        )

    # Main content
    if selected == "Stats 📊":
        st.header("Repository Statistics 📊")
        stats = repo_manager.get_repo_stats()
        summary = create_summary(repo_manager, stats)
        st.markdown(summary, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        metrics = [
            ("Total Repositories", stats["Total Repositories"], COLORS['total']),
            (f"Owned by {repo_manager.user.login}", stats[f"Owned by {repo_manager.user.login}"], COLORS['owned']),
            ("Public", stats["Public"], COLORS['public']),
            ("Private", stats["Private"], COLORS['private']),
            ("Forked", stats["Forked"], COLORS['forked']),
            ("Archived", stats["Archived"], COLORS['archived'])
        ]
        for i, (key, value, color) in enumerate(metrics):
            if i % 3 == 0:
                col1.markdown(f"<p style='color:{color};font-weight:bold;font-size:18px;text-align:center;'>{key}</p>", unsafe_allow_html=True)
                col1.markdown(f"<h2 style='color:{color};font-weight:bold;text-align:center;'>{value}</h2>", unsafe_allow_html=True)
            elif i % 3 == 1:
                col2.markdown(f"<p style='color:{color};font-weight:bold;font-size:18px;text-align:center;'>{key}</p>", unsafe_allow_html=True)
                col2.markdown(f"<h2 style='color:{color};font-weight:bold;text-align:center;'>{value}</h2>", unsafe_allow_html=True)
            else:
                col3.markdown(f"<p style='color:{color};font-weight:bold;font-size:18px;text-align:center;'>{key}</p>", unsafe_allow_html=True)
                col3.markdown(f"<h2 style='color:{color};font-weight:bold;text-align:center;'>{value}</h2>", unsafe_allow_html=True)

    elif selected == "Activity 🕒":
        st.header("Recent Activity 🕒")
        st.subheader("Recently Active Repositories")
        
        # New component to accept user input
        num_recent_repos = st.number_input("Number of recent repositories to fetch", min_value=1, max_value=50, value=10, step=1)
        
        recent_repos = repo_manager.get_recent_repos(num_recent_repos)
        show_all_commits = st.checkbox("Show all recent commits", value=True)

        all_commits = []
        
        for i, repo in enumerate(recent_repos, 1):
            st.write(f"{i}. **{repo.name}** - Last updated: {format_datetime(repo.updated_at)}")
            commits = repo_manager.get_repo_commits(repo)
            
            if commits:
                if show_all_commits:
                    for commit in commits:
                        all_commits.append({
                            'repo': repo.name,
                            'message': commit.commit.message,
                            'date': commit.commit.author.date,
                            'author': commit.commit.author.name,
                            'url': commit.html_url
                        })
                else:
                    with st.expander(f"Show commits for {repo.name}"):
                        for commit in commits:
                            st.write(f"- {commit.commit.message} ({format_datetime(commit.commit.author.date)})")
            else:
                st.write("No commits found in this repository.")
        
        if show_all_commits and all_commits:
            st.subheader("All Recent Commits")
            filter_user_commits = st.checkbox("Show only my commits", value=True)
            df_commits = pd.DataFrame(all_commits)
            df_commits['date'] = pd.to_datetime(df_commits['date']).dt.strftime("%b %d, %Y %I:%M %p")
            
            if filter_user_commits:
                user_login = repo_manager.user.login
                user_name = repo_manager.user.name
                st.write(f"Filtering commits by {user_login} (username) and {user_name} (full name)")
                
                # Create summary for owned repos
                owned_repos = df_commits[df_commits['author'].isin([user_login, user_name])]
                owned_summary = f"""
                You have made <span style='color:#4CAF50;font-weight:bold;'>{len(owned_repos)}</span> commits 
                across <span style='color:#4CAF50;font-weight:bold;'>{owned_repos['repo'].nunique()}</span> repositories.
                """
                
                # Create summary for other repos
                other_repos = df_commits[~df_commits['author'].isin([user_login, user_name])]
                other_summary = f"""
                There are <span style='color:#2196F3;font-weight:bold;'>{len(other_repos)}</span> commits 
                by other authors across <span style='color:#2196F3;font-weight:bold;'>{other_repos['repo'].nunique()}</span> repositories.
                """
                
                st.markdown(owned_summary, unsafe_allow_html=True)
                st.markdown(other_summary, unsafe_allow_html=True)
                
                # Display unique authors
                st.write("Unique authors in the dataset:")
                authors = df_commits['author'].unique()
                for author in authors:
                    color = '#4CAF50' if author in [user_login, user_name] else '#2196F3'
                    st.markdown(f"<span style='color:{color};'>{author}</span>", unsafe_allow_html=True)
                
                df_filtered = owned_repos
                st.write(f"Showing {len(df_filtered)} commits for {user_login}/{user_name}")
                if len(df_filtered) == 0:
                    st.warning("No commits found for the current user. This might be due to a mismatch between your GitHub username/name and the commit author name.")
                df_commits = df_filtered
            
            st.dataframe(df_commits, use_container_width=True)
        elif show_all_commits:
            st.write("No commits found in any of the recent repositories.")
        
        # Export All Commits
        st.subheader("Export All Commits")
        if st.button("Prepare Commits for Export"):
            with st.spinner("Fetching all commits... This may take a while."):
                all_commits_df = get_all_commits(repo_manager, recent_repos)
            st.success("Commits fetched successfully!")
            export_to_csv(all_commits_df, f"{repo_manager.user.login}_all_commits.csv")
        
        # Activity Timeline
        activity_data = [{'repo': repo.name, 'date': repo.updated_at} for repo in recent_repos]
        activity_df = pd.DataFrame(activity_data)
        fig = px.scatter(activity_df, x="date", y="repo", title="Recent Repository Activity",
                         labels={"date": "Last Update", "repo": "Repository"},
                         hover_data=["date"])
        fig.update_traces(marker=dict(size=10))
        fig.update_layout(xaxis_title="Last Update", yaxis_title="Repository")
        st.plotly_chart(fig, use_container_width=True)

    elif selected == "Data 📁":
        st.header("Repository Data 📁")
        # Checkbox for formatting owned vs. non-owned repos
        format_owned = st.checkbox("Format Owned vs. Non-Owned", value=True)

        df = repo_manager.get_repos_dataframe()
        
        if format_owned:
            owned_count = df['is_owner'].sum()
            non_owned_count = len(df) - owned_count
            st.markdown(f"You own <span style='color:red;font-weight:bold;'>{owned_count}</span> repositories and have access to <span style='color:red;font-weight:bold;'>{non_owned_count}</span> repositories owned by others.", unsafe_allow_html=True)

        st.dataframe(format_dataframe(df, format_owned), use_container_width=True)
        
        # Add export button for repository data
        export_to_csv(df, f"{repo_manager.user.login}_repository_data.csv")

    elif selected == "Visualize 📈":
        st.header("Visualizations 📈")
        
        st.write("""
        This section provides visual insights into your GitHub repositories using Plotly charts. 
        """)
        
        df = repo_manager.get_repos_dataframe()
        
        col1, col2 = st.columns(2)

        with col1:
            # Language distribution
            lang_counts = df['language'].value_counts()
            fig = px.pie(values=lang_counts.values, names=lang_counts.index, title="Language Distribution")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Stars vs. Forks scatter plot
            fig = px.scatter(df, x="stars", y="forks", hover_name="name", title="Stars vs. Forks")
            st.plotly_chart(fig, use_container_width=True)

        # Repository creation timeline
        fig = px.histogram(df, x="created_at", title="Repository Creation Timeline")
        st.plotly_chart(fig, use_container_width=True)

    elif selected == "Stars ⭐":
        st.header("Starred Repositories ⭐")
        
        st.write("""
        This section analyzes and visualizes your starred repositories on GitHub. 
        """)
        
        starred_df = repo_manager.get_starred_repos()
        
        # Ensure starred_df is a DataFrame
        if not isinstance(starred_df, pd.DataFrame):
            starred_df = pd.DataFrame(starred_df)

        # Display total number of starred repositories
        st.subheader(f"Total Starred Repositories: {len(starred_df)}")
        
        # Display table of starred repositories
        st.dataframe(starred_df, use_container_width=True)
        
        # Language breakdown pie chart
        lang_counts = starred_df['language'].value_counts()
        fig = px.pie(values=lang_counts.values, names=lang_counts.index, title="Language Distribution of Starred Repositories")
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 10 most starred repositories
        top_10_starred = starred_df.nlargest(10, 'stars')
        fig = go.Figure(data=[go.Bar(x=top_10_starred['name'], y=top_10_starred['stars'])])
        fig.update_layout(title="Top 10 Most Starred Repositories", xaxis_title="Repository", yaxis_title="Stars")
        st.plotly_chart(fig, use_container_width=True)
        
        # Export to CSV
        st.subheader("Export Starred Repositories Data")
        export_to_csv(starred_df, f"{repo_manager.user.login}_starred_repositories.csv")

    elif selected == "Create 🆕":
        create_repository(repo_manager)

    elif selected == "Delete 🗑️":
        delete_repository(repo_manager)

    st.sidebar.markdown("""
    ---
    ### About this app
    
    This GitHub Repository Analyzer helps you manage and visualize your GitHub repositories efficiently using [PyGithub](https://pygithub.readthedocs.io/en/latest/) and [Streamlit](https://streamlit.io/). See more at [GitHub Repository Analyzer](https://github.com/keonmonroe/github-repo-analyzer) including CLI usage and potential use cases.
                        
    """)

if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="GitHub Repository Analyzer")
    main()
