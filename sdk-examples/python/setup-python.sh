rm -rf /workspaces/llama-store/sdk-examples/python/pics
cd /workspaces/llama-store/output/python
pip install build
python -m build --outdir dist .
pip install dist/llamastore-0.0.2-py3-none-any.whl
