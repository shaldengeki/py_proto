#!/usr/bin/env bash
set -euo pipefail

function compare_proto() {
    # Takes one argument, the relative path to the proto to compare.
    echo $1
    ./src/util/parser_binary $1 > "${1}_serialized.proto"
    diff --side-by-side --ignore-all-space --ignore-blank-lines $1 "${1}_serialized.proto"
}

echo "Local protos:"
LOCAL_PROTOS=$(find ./test/resources -name "*.proto" | sort)
for f in $LOCAL_PROTOS; do
    compare_proto $f
done

echo "Google protos:"
GOOGLE_PROTOS=$(find ./external/com_google_protobuf/src/google/protobuf -name "*.proto" | xargs grep --files-without-match "proto2" | sort)
for f in $GOOGLE_PROTOS; do
    compare_proto $f
done
