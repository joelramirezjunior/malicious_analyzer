for file in *; do
    mv "$file" "$(echo "$file" | tr -d ' ')"
done
