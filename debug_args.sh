#!/bin/bash
echo "Script appelé avec les arguments: $@" >&2
echo "Nombre d'arguments: $#" >&2
for i in "$@"; do
    echo "Arg: '$i'" >&2
done