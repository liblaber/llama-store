# This script creates the OpenAPI spec files for the llama store API
# Specs are created in both JSON and YAML formats
# The read-only specs are created first, then the read/write specs

# Change to the llama store directory
cd ../llama_store

# Create the read-only specs in JSON and YAML
python3 export_openapi.py main:app --out ../read-only-spec.json
python3 export_openapi.py main:app --out ../read-only-spec.yaml

# Create the read/write specs
export ALLOW_WRITE=true
python3 export_openapi.py main:app --out ../spec.json
python3 export_openapi.py main:app --out ../spec.yaml

cd ..

# Check if the spec files were updated - if so we can add them to the commit
is_diff=false

git diff --exit-code --no-patch read-only-spec.json
if [ $? -ne 0 ]; then
    git add read-only-spec.json
    is_diff=true
fi

git diff --exit-code --no-patch read-only-spec.yaml
if [ $? -ne 0 ]; then
    git add read-only-spec.yaml
    is_diff=true
fi

git diff --exit-code --no-patch spec.json
if [ $? -ne 0 ]; then
    git add spec.json
    is_diff=true
fi

git diff --exit-code --no-patch spec.yaml
if [ $? -ne 0 ]; then
    git add spec.yaml
    is_diff=true
fi

git status
git pull

# Commit the changes if there were any, and push to the remote
if [ $is_diff = true ]; then
    echo "OpenAPI specs updated, committing and pushing to remote"
    git commit -m "Update OpenAPI specs"
    git push origin HEAD:$1
else
    echo "OpenAPI specs unchanged, no need to commit or push"
fi
