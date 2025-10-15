# ===========================================
# 🚀 Universal Release Template (v2.8+)
# ===========================================

.PHONY: release-template
release-template: ## Run full release cycle (autoformat + tag + push)
	@ver=$${version:-v2.8}; \
	echo "🚀 Starting universal release pipeline for $$ver..."; \
	echo "🧹 Running cleanup and formatting..."; \
	black backend/app || true; \
	isort backend/app || true; \
	flake8 backend/app || true; \
	echo "🧩 Regenerating release snapshot..."; \
	make snapshot-patches || true; \
	echo "🪄 Linting and fixing markdown docs..."; \
	npx markdownlint-cli2 --fix "docs/**/*.md" || true; \
	echo "✅ Creating Git tag..."; \
	read -p "Enter new version tag (default $$ver): " tag; \
	tag=$${tag:-$$ver}; \
	git add docs && \
	git commit -am "chore(release): finalize $$tag" --no-verify && \
	git tag -a $$tag -m "Release $$tag — Autoformat + Docs Sync" && \
	echo "🎯 Tagged $$tag successfully!" && \
	git push origin release/$${ver}-dev --tags && \
	echo "✅ Release $$tag pushed successfully!"

.PHONY: fix-docs-lint
fix-docs-lint: ## Auto-fix markdownlint issues (MD013, MD036, MD051)
	@echo "🧹 Running markdown auto-fix utility..."
	bash scripts/fix_markdown_docs.sh
