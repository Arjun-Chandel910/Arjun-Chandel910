import os
import requests
import jinja2

# Your GitHub username
USERNAME = "arjun-chandel910"

# --- Function to fetch the latest open-source contributions ---
# This uses the GitHub API to find your recent public contributions
def get_contributions(username):
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    query = """
    query($username: String!) {
      user(login: $username) {
        repositories(
          first: 5, 
          orderBy: {field: PUSHED_AT, direction: DESC},
          isFork: false,
          ownerAffiliations: COLLABORATOR,
          privacy: PUBLIC
        ) {
          nodes {
            name
            description
            url
            stargazerCount
            forkCount
            primaryLanguage {
              name
              color
            }
          }
        }
      }
    }
    """
    variables = {"username": username}
    response = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables},
        headers=headers
    )
    return response.json().get("data", {}).get("user", {}).get("repositories", {}).get("nodes", [])

# --- Function to generate the animated SVG file ---
def generate_svg(template_data):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("contribution_template.svg.j2")
    
    # Render the template with the fetched data
    output = template.render(repos=template_data)
    
    with open("contribution_card.svg", "w") as f:
        f.write(output)

# --- Main script execution ---
if __name__ == "__main__":
    contributions = get_contributions(USERNAME)
    generate_svg(contributions)

    print("Successfully updated contribution_card.svg")