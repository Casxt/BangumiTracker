cd proto

PY_PKG=proto_py
OUT_DIR=../src/$PY_PKG
rm -r  $OUT_DIR
mkdir -p $OUT_DIR

for file in $(find . -name "*.proto"); do
  echo "processing ${file}"
  protoc --python_out=$OUT_DIR --pyi_out=$OUT_DIR "${file}"
done

for dir_path in $(find $OUT_DIR -mindepth 1 -maxdepth 1 -type d); do
    package=$(basename "$dir_path")
    echo "Found package ${package} Beginning replacement"
    find $OUT_DIR/. -name '*.py' -exec sed -i '.bak' -e "s#from ${package}#from ${PY_PKG}.${package}#g" {} \;
    find $OUT_DIR/. -name '*.pyi' -exec sed -i '.bak' -e "s#from ${package}#from ${PY_PKG}.${package}#g" {} \;
done

tree $OUT_DIR