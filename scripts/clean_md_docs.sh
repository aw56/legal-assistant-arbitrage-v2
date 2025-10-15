#!/usr/bin/env bash
set -e

FILES="docs/MAKE_PATCH_AND_RELEASE_GUIDE_v2.8.md docs/RELEASE_v2.8-dev_CHRONIK.md"

for f in $FILES; do
  echo "🧹 Cleaning $f..."
  # Удаляем мусорные строки от терминала/копирования
  sed -i '/Копировать код/d' "$f"
  sed -i '/pgsql/d' "$f"
  sed -i '/ini/d' "$f"
  sed -i '/yaml/d' "$f"
  sed -i '/bash/d' "$f"
  sed -i '/markdown/d' "$f"
  sed -i 's/\t/    /g' "$f"               # заменяем табы пробелами
  sed -i 's/^```makefile$/```make/g' "$f" # исправляем кодовые блоки
  sed -i 's/^```ini$/```/g' "$f"
  sed -i 's/^```yaml$/```/g' "$f"
  sed -i 's/^```bash$/```bash/g' "$f"
  sed -i 's/^```markdown$/```/g' "$f"
  # Добавляем пустую строку после фронтматтера
  awk 'NR==1{print; next} NR==2 && $0=="---"{print ""; print $0; next} {print}' "$f" > tmp && mv tmp "$f"
done

echo "✅ All Markdown files cleaned!"
