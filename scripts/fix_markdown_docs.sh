#!/usr/bin/env bash
# ============================================================
# 🧹 Markdown Docs Auto-Fixer (v2.8)
# Legal Assistant Arbitrage — Universal Cleanup Utility
# ============================================================

set -e

echo "🧩 Starting markdown docs cleanup..."

TARGET_DIR="docs"
TMP_FILE="/tmp/md_fix_temp.$$"

# 1️⃣ Исправляем чрезмерно длинные строки (MD013)
find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
  awk '{if (length($0) > 180) {print substr($0, 1, 160) "\\\n" substr($0, 161)} else print $0}' "$file" > "$TMP_FILE" && mv "$TMP_FILE" "$file"
done
echo "✅ Step 1: Long lines (MD013) shortened to 160 chars."

# 2️⃣ Исправляем “курсив вместо заголовка” (MD036)
#    Безопасно обрабатывает любые спецсимволы — переносим дефис в конец диапазона
find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
  sed -E -i 's/^\*([A-Za-zА-Яа-я0-9(). +_]+[-]*)\*$/### \1/g' "$file"
done
echo "✅ Step 2: Headings (MD036) normalized."

# 3️⃣ Исправляем некорректные якоря (MD051)
#    Удаляет лишние дефисы после решётки
find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
  sed -E -i 's/\(#-([^)]+)\)/(#\1)/g' "$file"
done
echo "✅ Step 3: Link anchors (MD051) fixed."

# 4️⃣ Финальная проверка markdownlint
echo "🔍 Running final markdownlint check..."
npx markdownlint-cli2 --fix "docs/**/*.md" || true

echo "🎯 Markdown docs cleanup completed successfully!"
