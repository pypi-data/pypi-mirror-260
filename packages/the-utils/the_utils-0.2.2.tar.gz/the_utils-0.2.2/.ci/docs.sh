WORKSPACE=$(pwd)
echo current workspace: $WORKSPACE

cd docs
rm -rf rst_tmp _build
sphinx-apidoc -f --tocfile project -o $WORKSPACE/docs/tmp/ $WORKSPACE/the_utils ''
make clean
make html
