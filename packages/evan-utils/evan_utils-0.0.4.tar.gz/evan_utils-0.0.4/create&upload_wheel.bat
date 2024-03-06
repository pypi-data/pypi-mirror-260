cd D:\Projects\create_whl
rmdir /s dist

python -m build
pip install --upgrade twine
python -m twine upload --repository pypi dist/*

pause