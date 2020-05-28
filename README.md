# GetFolderFromRepo
Download a specific folder or file from a GitHub repository

## Usage:
`getFolderFromRepo.py <GitHub URL of the folder/file>`  
**Example:**  
`getFolderFromRepo.py https://github.com/di0002ya/ESS/tree/master/data/GP_ICE`  
Will download the `GP_ICE` folder from the repo `https://github.com/di0002ya/ESS/`

## First Time Usage:
A few extra steps are required, in order to ensure smooth working
1. `[sudo] chmod +x getFolderFromRepo.py`
2. (Although this step is not entirely necessary, it is highly recommended, as the GitHub API gives very little[rate limited] access without a token)
   * Generate a new GitHub Personal Access Token from here: https://github.com/settings/tokens/new.  
   Select only 'repo' from the list of scopes. Enter a suitable note.
   * ***[Recommended way]***  
   Create a file `config.py` in the same folder as `getFolderFromRepo.py`, with the following contents:  
`USERNAME = '' # your GitHub username here`  
`TOKEN = '' # your token here`  
   ***OR***  
Set the `GITHUB_USERNAME` and `GITHUB_TOKEN` environment variables to appropriate values  
   ***OR [Not recommended]***  
Set the `USERNAME` and `TOKEN` in the `getFolderFromRepo.py` file itself  
(Then be sure never to share this file with anyone)

## Author:
[Aliabbas Merchant](https://github.com/AliabbasMerchant)

## Contributing:
All contributions and feedback are welcome!
