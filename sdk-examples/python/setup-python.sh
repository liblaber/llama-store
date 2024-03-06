rm -rf /workspaces/llama-store/sdk-examples/python/pics
cd /workspaces/llama-store/output/python
pip install -r requirements.txt
pip install build
python -m build --outdir dist .
pip install dist/llamastore-0.0.3-py3-none-any.whl --upgrade --no-deps --force-reinstall
