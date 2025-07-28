# dev branch: push local to remote
git checkout dev
git status
git pull origin dev
git push origin dev

# merge dev branch into main branch
git checkout main
git status
git merge dev

# main branch: push local to remote
git status
git pull origin main
git push origin main

# dev branch: switch back to dev branch
git checkout dev
