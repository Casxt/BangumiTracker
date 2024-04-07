#!/bin/bash

cd proto

OUT_DIR=../app/src/proto
rm -r  $OUT_DIR
mkdir -p $OUT_DIR

plugin_path=`readlink -f ../app/node_modules/.bin`

for file in $(find . -name "*.proto"); do
  echo "processing ${file}"
  protoc \
    --plugin="protoc-gen-ts=$plugin_path/protoc-gen-ts" \
    --ts_out=no_namespace:$OUT_DIR "$file"

#   protoc \
#     --plugin=protoc-gen-js=$plugin_path/protoc-gen-js \
#     --js_out=import_style=commonjs,binary:$OUT_DIR "${file}"
done

tree $OUT_DIR