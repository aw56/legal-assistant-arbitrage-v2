#!/usr/bin/env bash
set -e

echo "🧹 Cleaning up unused imports and variables..."

# Удаляем неиспользуемые импорты и переменные во всём проекте
autoflake --in-place --recursive \
  --remove-all-unused-imports \
  --remove-unused-variables \
  backend scripts

# Дополнительно прогоняем isort и black для форматирования
isort backend scripts
black backend scripts

echo "✨ Cleanup complete!"
