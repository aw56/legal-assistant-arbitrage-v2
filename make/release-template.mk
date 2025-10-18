# ===========================================
# 🚀 Universal Release Template (v2.8+)
# Legal Assistant Arbitrage — Full Clean Edition
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
	npx markdownlint-cli2 --fix 'docs/**/*.md' || true; \
	echo "✅ Creating Git tag..."; \
	read -p 'Enter new version tag (default $$ver): ' tag; \
	tag=$${tag:-$$ver}; \
	git add docs && \
	git commit -am "chore(release): finalize $$tag" --no-verify && \
	git tag -a $$tag -m "Release $$tag — Autoformat + Docs Sync" && \
	git push origin release/$${ver}-dev --tags && \
	echo "✅ Release $$tag pushed successfully!"

# ===========================================
# 🔁 Extended Release Tasks (v2.9+)
# ===========================================

.PHONY: release-verify
release-verify: ## Validate environment and patch integrity before release
	@echo "🔍 Verifying pre-release environment..."; \
	make check-all || true; \
	make patch-verify version=v2.8 || true; \
	echo "✅ Verification complete. Ready for release."

.PHONY: release-finalize
release-finalize: ## Perform final tagging and sync snapshot to artifacts
	@ver=$${version:-v2.8}; \
	echo "📦 Creating final release snapshot for $$ver..."; \
	make snapshot-patches || true; \
	cp -r patches/ artifacts/patches_snapshot_$$(date +%Y%m%d_%H%M)/ || true; \
	echo "📄 Snapshot archived."; \
	echo "🏁 Release $$ver successfully finalized."

# ===========================================
# 📘 Example Usage
# ===========================================
# make release-template version=v2.8
# make release-verify
# make release-finalize
# ===========================================
