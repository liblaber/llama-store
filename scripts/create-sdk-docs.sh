# Copy the README
cp README.md ./docs/docs/_readme.md

# Build the SDKs
liblab build --yes

# Create the snippets folder if it doesn't exist
mkdir -p ./docs/static/snippets

# Copy the snippets to the docs folder
cp ./output/csharp/Documentation/Snippets/snippets.json ./docs/static/snippets/csharp.json
cp ./output/go/documentation/Snippets/snippets.json ./docs/static/snippets/go.json
# cp ./output/java/Documentation/Snippets/snippets.json ./docs/static/snippets/java.json
# cp ./output/typescript/Documentation/Snippets/snippets.json ./docs/static/snippets/typescript.json
cp ./output/python/documentation/Snippets/snippets.json ./docs/static/snippets/python.json
cp ./output/php/documentation/Snippets/snippets.json ./docs/static/snippets/php.json

# Create the API docs
cd ./docs
npm run docusaurus clean-api-docs all
npm run docusaurus gen-api-docs all
