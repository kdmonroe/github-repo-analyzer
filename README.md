# GitHub Repo Analyzer

GitHub Repo Analyzer is a tool that helps you manage and visualize your GitHub repositories efficiently. It offers two main interfaces:

1. A Streamlit-based web application
2. A command-line interface (CLI) using argparse

Both interfaces leverage the PyGithub library to interact with the GitHub API and provide various functionalities such as viewing repository statistics, recent activity, data visualization, and more.

### Prerequisites
- Python 3.7 or higher
- GitHub Personal Access Token

### GitHub Token Permissions

To use this application, you'll need a GitHub Personal Access Token with the following scopes:

1. **repo**: Full control of private repositories
   - Needed for accessing repository data, creating/deleting repositories, and managing repository settings.

2. **read:user**: Read access to user profile data
   - Required to fetch information about the authenticated user.

3. **user:email**: Access user email addresses (read-only)
   - Necessary for operations that require the user's email, such as commit author information.

4. **delete_repo**: Delete repositories
   - Essential for the repository deletion feature. Only include this if you want to use the delete functionality.

5. **workflow**: Update GitHub Action workflows
   - Required if you plan to manage or view GitHub Actions within the app.

To create a token with these permissions:

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Click "Generate new token"
3. Select the scopes listed above
4. Generate and securely store your token

As a best practice, emember to keep your token confidential and never share it publicly. 
The app will prompt you to enter this token when you run it and not store it out


## Features

- **Stats 📊**: Overview of your GitHub repositories, including total repositories, public/private repositories, forked/archived repositories, and more.
- **Activity 🕒**: View recent commits and repository updates. Filter commits by user and export commit data to CSV.
- **Data 📁**: Detailed information about your repositories, with options to format owned vs. non-owned repositories and export data to CSV.
- **Visualize 📈**: Graphs and charts of your GitHub data, including language distribution, stars vs. forks, and repository creation timeline.
- **Stars ⭐**: Information about your starred repositories, including language distribution and top 10 most starred repositories.
- **Create 🆕**: Create new repositories using the GitHub API.
- **Delete 🗑️**: Option to delete repositories (use with caution).

## Interfaces

### 1. Streamlit Web Application

The Streamlit web application provides a user-friendly, interactive interface for managing and visualizing your GitHub repositories.

#### Running the Streamlit App

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to view the app.

### 2. Command-Line Interface (CLI)

The CLI offers quick access to core functionalities through the command line, ideal for scripting and automation.

#### Using the CLI

Navigate to the project directory and use the following command structure:

```bash
python cli.py <command> [options]
```

Available commands:
- `stats`: Get repository statistics
- `list`: List all repositories
- `create`: Create a new repository
- `delete`: Delete a repository
- `export`: Export repository data to CSV or Excel
- `stars`: Export starred repositories to CSV or Excel
- `visualize`: Generate and save Plotly diagrams locally

Examples:
```bash
python cli.py stats
python cli.py list
python cli.py create --name "new-repo" --description "A new repository" --private
python cli.py delete --name "repo-to-delete"
python cli.py export --format csv --output repo_data.csv
python cli.py export --format xlsx --output repo_data.xlsx
python cli.py stars --format csv --output starred_repos.csv
python cli.py visualize --type language_distribution --output lang_dist.png
python cli.py visualize --type stars_vs_forks --output stars_vs_forks.png
python cli.py visualize --type creation_timeline --output timeline.png
```

For more information on CLI usage, run:
```bash
python cli.py --help
```

## Data Export

Both the Streamlit app and CLI support exporting data to CSV and Excel formats. You can export:
- Repository data
- Starred repositories

## Visualization

The tool generates various Plotly diagrams to visualize your GitHub data:
- Language distribution
- Stars vs. Forks
- Repository creation timeline

In the Streamlit app, these visualizations are displayed interactively. Using the CLI, you can save these diagrams as image files locally.

## Potential Use Cases

- **Developers**: Manage and visualize your GitHub repositories in a user-friendly interface.
- **Project Managers**: Get insights into repository statistics and recent activity to better manage development workflows.
- **Data Analysts**: Analyze GitHub repository data and visualize trends and patterns.
- **Educators**: Use the app as a teaching tool to demonstrate GitHub API interactions and data visualization techniques.

## Contributions

Contributions are welcome! If you have any ideas for new features or improvements, feel free to open an issue or submit a pull request.

### How to Contribute

Contributions are welcome! You can follow the instructions below to do so.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## Development Setup

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/github-repo-analyzer.git
    cd github-repo-analyzer
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your GitHub token:
    ```env
    GITHUB_TOKEN=your_github_token
    ```

### Running the App

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```

2. Open your web browser and go to `http://localhost:8501` to view the app.

### Using the CLI

You can also use the GitHub Repository Analyzer from the command line:

1. Navigate to the project directory:
    ```bash
    cd github-repo-analyzer
    ```

2. Run the CLI with the desired action:
    ```bash
    python cli.py stats  # Get repository statistics
    python cli.py list   # List all repositories
    python cli.py create --name "new-repo" --description "A new repository" --private  # Create a new private repository
    python cli.py delete --name "repo-to-delete"  # Delete a repository
    python cli.py export --format csv --output repo_data.csv  # Export repository data to CSV
    python cli.py export --format xlsx --output repo_data.xlsx  # Export repository data to Excel
    python cli.py stars --format csv --output starred_repos.csv  # Export starred repositories to CSV
    python cli.py visualize --type language_distribution --output lang_dist.png  # Generate and save language distribution diagram
    python cli.py visualize --type stars_vs_forks --output stars_vs_forks.png  # Generate and save stars vs. forks diagram
    python cli.py visualize --type creation_timeline --output timeline.png  # Generate and save repository creation timeline diagram
    ```

For more information on CLI usage, run:
```bash
python cli.py --help
```

## Setting up the environment

### Using Conda

1. Make sure you have [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system.

2. Clone this repository:
   ```
   git clone https://github.com/yourusername/github-repo-analyzer.git
   cd github-repo-analyzer
   ```

3. Create a new conda environment using the `environment.yml` file:
   ```
   conda env create -f environment.yml
   ```

4. Activate the new environment:
   ```
   conda activate gh-streamlit
   ```

5. You're now ready to run the application!

### Using pip

If you prefer to use pip instead of conda, you can install the required packages using the `requirements.txt` file:

1. Create a new virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. You're now ready to run the application!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [PyGithub](https://pygithub.readthedocs.io/en/latest/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)