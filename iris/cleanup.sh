
find . \( -name '*.pyc' -or -name '__pycache__' \) -delete
find . -name '*.so.*' -exec  strip {} \;

rm -rf _pytest*
rm -rf .pytest_cache

rm -f caa*.nc
