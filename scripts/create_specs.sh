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
