# This script allows us to download the images datasets (either the complete or the small version). It does so by using the `curl` command.

SMALL="https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb-small.zip"
COMPLETE="https://cdn.cs50.net/ai/2023/x/projects/5/gtsrb.zip"

if [ "$1" == "--small" ]; then
    curl -fsSLO $SMALL
else
    curl -fsSLO $COMPLETE
fi
