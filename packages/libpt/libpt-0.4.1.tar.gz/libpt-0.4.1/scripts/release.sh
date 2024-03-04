#!/bin/bash
TOKEN=$(cat ~/.git-credentials | grep 'git.cscherr.de' | grep -P '(?:)[^:]*(?=@)' -o)
NEW_VERSION=$(cat Cargo.toml | rg '^\s*version\s*=\s*"([^"]*)"\s*$' -or '$1')
VERSION=$(git rev-parse HEAD)
GIT_COMMIT_SHA=$(git rev-parse HEAD)
BODY="
$(git log $(git describe --tags --abbrev=0)..HEAD --pretty="- %s" --oneline --decorate)
"
USER=PlexSheep
git tag "v$NEW_VERSION" || echo "could not tag"
curl -X 'POST' \
	'https://git.cscherr.de/api/v1/repos/PlexSheep/pt/releases' \
	-H 'accept: application/json' \
	-H "Authorization: token $TOKEN" \
	-H 'Content-Type: application/json' \
	-d '{
  "body": "'"$BODY"'",
  "draft": false,
  "name": "v'$NEW_VERSION'",
  "prerelease": true,
  "tag_name": "v'$NEW_VERSION'",
  "target_commitish": "'$GIT_COMMIT_SHA'"
}' | python -m json.tool
git push || echo "could not push"
