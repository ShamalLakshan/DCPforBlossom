Blossom Theme Stats

This script generates statistics for the Blossom Theme, a popular theme for various code editors and IDEs. The script collects data from various sources, including GitHub, Visual Studio Code Marketplace, and Package Control.

## This is only a development version of the script. Script successfully deployed and running privately at [@BlossomThemeAdmin](https://github.com/BlossomThemeAdmin) 

TODO

    Add Web skin download statistics

Requirements

    Python 3.x
    requests library
    BeautifulSoup library
    tabulate library
    os library

Usage

    Run the script using Python: python blossom_stats.py
    The script will generate a markdown file named YYYY-MM-DD.md in the current directory, where YYYY-MM-DD is the current date.
    The markdown file will contain statistics for the Blossom Theme, including organization information, VS Code downloads, Sublime Package downloads, and repository clones.

Note

    You need to set an environment variable SOME_SECRET with your GitHub token to access the clone count statistics.
    The script uses a hard-coded URL and div ID for the Sublime Package stats. If these change, you will need to update the script accordingly.
    The script assumes that the VS Code extension ID is blossomtheme.blossomtheme. If this changes, you will need to update the script accordingly.

License

This script is licensed under the MIT License.
