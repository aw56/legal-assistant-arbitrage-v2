# ===========================================
# 🧩 Patch Verification Utility (Universal)
# Legal Assistant Arbitrage v2.8+
# ===========================================

.PHONY: patch-verify
patch-verify: ## Verify patch integrity and reversibility (usage: make patch-verify version=v2.8)
	@ver=$${version:-v2.8}; \
	patch_file="patches/$$ver/$${ver}_dev_base_state.patch"; \
	echo "🔍 Checking patch integrity for $$ver..."; \
	if [ ! -f "$$patch_file" ]; then \
		echo "❌ Patch file not found: $$patch_file"; exit 1; fi; \
	if git apply --check "$$patch_file" >/dev/null 2>&1; then \
		echo "✅ Patch can be applied cleanly."; \
	else \
		echo "⚠️  Patch already applied or conflicts detected."; \
	fi; \
	if git apply --reverse --check "$$patch_file" >/dev/null 2>&1; then \
		echo "✅ Reverse check passed (safe rollback possible)."; \
	else \
		echo "⚠️  Reverse check failed (already base or modified)."; \
	fi; \
	echo "📄 Patch summary:"; \
	if git rev-parse "$${ver}-base" >/dev/null 2>&1; then \
		git diff "$${ver}-base"..HEAD --stat; \
	else \
		echo "⚠️  Base tag $${ver}-base not found."; \
	fi
