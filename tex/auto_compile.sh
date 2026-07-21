#!/usr/bin/env bash
# Compile the CV variants into PDFs, keeping the working directory clean.
# Without arguments, builds all three variants:
#   shuaiqing_multimodal.tex, shuaiqing_embodied.tex, shuaiqing_agent.tex
# With arguments, only builds the given .tex files.
# Intermediate artifacts (aux/log/out/toc/...) are written into a build/
# subdirectory (one per job) and only the final PDF is copied back next to
# the .tex source.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR"

DEFAULT_TARGETS=(
    "shuaiqing_multimodal.tex"
    "shuaiqing_embodied.tex"
    "shuaiqing_agent.tex"
)

if [[ $# -gt 0 ]]; then
    TARGETS=("$@")
else
    TARGETS=("${DEFAULT_TARGETS[@]}")
fi

compile_one() {
    local tex_file="$1"
    local jobname build_dir

    if [[ ! -f "$tex_file" ]]; then
        echo "error: $tex_file not found in $SCRIPT_DIR" >&2
        return 1
    fi

    jobname="$(basename "$tex_file" .tex)"
    build_dir="build/$jobname"
    mkdir -p "$build_dir"

    echo "==> building $tex_file"

    if command -v latexmk >/dev/null 2>&1; then
        latexmk -pdf \
            -interaction=nonstopmode \
            -halt-on-error \
            -file-line-error \
            -output-directory="$build_dir" \
            "$tex_file"
    else
        for _ in 1 2; do
            pdflatex \
                -interaction=nonstopmode \
                -halt-on-error \
                -file-line-error \
                -output-directory="$build_dir" \
                "$tex_file"
        done
    fi

    if [[ -f "$build_dir/$jobname.pdf" ]]; then
        cp "$build_dir/$jobname.pdf" "./$jobname.pdf"
        echo "built: $SCRIPT_DIR/$jobname.pdf"
    else
        echo "error: expected $build_dir/$jobname.pdf was not produced" >&2
        return 1
    fi
}

status=0
for target in "${TARGETS[@]}"; do
    if ! compile_one "$target"; then
        status=1
    fi
done

exit "$status"
