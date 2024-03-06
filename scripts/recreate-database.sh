# Desc: Recreates the database and deletes all the pictures
cd /workspaces/llama-store/llama_store

# Delete the llama pictures
rm .appdata/llama_store_data/pictures/*

# Delete the database file
rm .appdata/sql_app.db

# Copy the llama pictures over
cp ./db_migrations/llama_pictures/* .appdata/llama_store_data/pictures/

# Create the database
alembic upgrade head