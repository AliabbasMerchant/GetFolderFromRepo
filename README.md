# GetFolderFromRepo
Download a specific file or folder from a GitHub repository

## Usage:
```getFolderFromRepo.py <GitHub URL of the folder/file>```

## First Time Usage:
A few extra steps are required, in order to ensure smooth working
1. `[sudo] chmod +x getFolderFromRepo.py`
2. Generate a new GitHub Personal Access Token from here: https://github.com/settings/tokens/new. Select only 'repo' from the list of scopes. Enter a suitable note. (Although this step is not entirely necessary, it is highly recommended, as the GitHub API gives very little[rate limited] access without a token)
3. [Recommended way] Create a file `config.py` in the same folder as `getFolderFromRepo.py`, with the following contents:
```
USERNAME = '' # put your GitHub username here
TOKEN = '' # put your token here
``` 
4. OR (instead of step 3) [Not recommended]  
Set your USERNAME and TOKEN in the `getFolderFromRepo.py` file itself. (Then be sure never to upload this file anywhere)


## Author:
[Aliabbas Merchant](https://github.com/AliabbasMerchant)
