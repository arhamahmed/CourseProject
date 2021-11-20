REPO_NAME_PLACEHOLDER = '<REPO_NAME>'
REPO_OWNER_PLACEHOLDER = '<REPO_OWNER>'
LOGIN_PLACEHOLDER = '<LOGIN>'
README_IDENTIFER = 'parseReadmeAttempt'
github_readme_only = \
"""
    query {
        repo: repository(name: "<REPO_NAME>", owner: "<REPO_OWNER>") {
            ...RepoFragment
        }
    }

    fragment RepoFragment on Repository {
        parseReadmeAttempt1: object(expression: "master:README.md") {
            ...ReadmeText
        }
        parseReadmeAttempt2: object(expression: "master:README.MD") {
            ...ReadmeText
        }
        parseReadmeAttempt3: object(expression: "master:readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt4: object(expression: "master:Readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt5: object(expression: "master:README") {
            ...ReadmeText
        }
        parseReadmeAttempt6: object(expression: "main:README.md") {
            ...ReadmeText
        }
        parseReadmeAttempt7: object(expression: "main:README.MD") {
            ...ReadmeText
        }
        parseReadmeAttempt8: object(expression: "main:readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt9: object(expression: "main:Readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt10: object(expression: "main:README") {
            ...ReadmeText
        }
        parseReadmeAttempt11: object(expression: "develop:README.md") {
            ...ReadmeText
        }
        parseReadmeAttempt12: object(expression: "develop:README.MD") {
            ...ReadmeText
        }
        parseReadmeAttempt13: object(expression: "develop:readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt14: object(expression: "develop:Readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt15: object(expression: "develop:README") {
            ...ReadmeText
        }
    }

    fragment ReadmeText on GitObject {
        ... on Blob {
            text
        }
    }
"""

full_github_repo_data = \
"""
    query {
        repo: repository(name: "<REPO_NAME>", owner: "<REPO_OWNER>") {
            ...RepoFragment
        }
    }

    fragment RepoFragment on Repository {
        owner {
            login
        }
        name
        description
        stargazerCount
        url
        updatedAt
        languages(first: 1) {
            nodes {
                name
            }
        }
        repositoryTopics(first: 15) {
            nodes {
                topic {
                    name
                }
            }
        }
        parseReadmeAttempt1: object(expression: "master:README.md") {
            ...ReadmeText
        }
        parseReadmeAttempt2: object(expression: "master:README.MD") {
            ...ReadmeText
        }
        parseReadmeAttempt3: object(expression: "master:readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt4: object(expression: "master:Readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt5: object(expression: "master:README") {
            ...ReadmeText
        }
        parseReadmeAttempt6: object(expression: "main:README.md") {
            ...ReadmeText
        }
        parseReadmeAttempt7: object(expression: "main:README.MD") {
            ...ReadmeText
        }
        parseReadmeAttempt8: object(expression: "main:readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt9: object(expression: "main:Readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt10: object(expression: "main:README") {
            ...ReadmeText
        }
        parseReadmeAttempt11: object(expression: "develop:README.md") {
            ...ReadmeText
        }
        parseReadmeAttempt12: object(expression: "develop:README.MD") {
            ...ReadmeText
        }
        parseReadmeAttempt13: object(expression: "develop:readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt14: object(expression: "develop:Readme.md") {
            ...ReadmeText
        }
        parseReadmeAttempt15: object(expression: "develop:README") {
            ...ReadmeText
        }
    }

    fragment ReadmeText on GitObject {
        ... on Blob {
            text
        }
    }
"""

get_starred_repos = \
"""
query {
  user: user(login: "<LOGIN>") {
    starredRepositories(first: 100) {
      nodes {
        nameWithOwner
      }
    }
  }
}
"""