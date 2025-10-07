#!/usr/bin/env bash
set -e

DOCS_DIR="docs"

echo "📝 Обновляем документацию в $DOCS_DIR..."

# --- README.md ---
cat > "$DOCS_DIR/README.md" <<'EOF'
# 📘 Legal Assistant Arbitrage API — v2
... здесь полный текст README.md из моей финальной версии ...
EOF

# --- DEPLOY.md ---
cat > "$DOCS_DIR/DEPLOY.md" <<'EOF'
# 🚀 Деплой Legal Assistant Arbitrage API
... полный текст DEPLOY.md ...
EOF

# --- LOCAL_DEV.md ---
cat > "$DOCS_DIR/LOCAL_DEV.md" <<'EOF'
# 🧑‍💻 Локальная разработка
... полный текст LOCAL_DEV.md ...
EOF

# --- TROUBLESHOOTING.md ---
cat > "$DOCS_DIR/TROUBLESHOOTING.md" <<'EOF'
# 🛠 Troubleshooting
... полный текст TROUBLESHOOTING.md ...
EOF

# --- GIT_SETUP.md ---
cat > "$DOCS_DIR/GIT_SETUP.md" <<'EOF'
# 🔧 Git Setup
... полный текст GIT_SETUP.md ...
EOF

echo "✅ Документация обновлена!"
