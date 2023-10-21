# This script creates the OpenAPI spec files for the llama store API
# Specs are created in both JSON and YAML formats
# The read-only specs are created first, then the read/write specs

# Change to the llama store directory
cd /workspaces/llama-store

git diff --exit-code --no-patch read-only-spec.json
if [ $? -ne 0 ]; then
    echo "read-only-spec.json is out of date"
    exit 1
fi

git diff --exit-code --no-patch read-only-spec.yaml
if [ $? -ne 0 ]; then
    echo "read-only-spec.yaml is out of date"
    exit 1
fi

git diff --exit-code --no-patch spec.json
if [ $? -ne 0 ]; then
    echo "spec.json is out of date"
    exit 1
fi

git diff --exit-code --no-patch spec.yaml
if [ $? -ne 0 ]; then
    echo "spec.yaml is out of date"
    exit 1
fi

echo "All specs are up to date"
exit 0