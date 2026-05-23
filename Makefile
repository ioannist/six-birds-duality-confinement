LATEXMK = latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build

DC_DIR = paper/duality_confinement
RH_DIR = paper/rh

PAPER_AUX_EXTS = aux log bbl blg toc out synctex.gz fdb_latexmk fls

.PHONY: help \
	paper-build-duality_confinement paper-build-rh paper-build \
	paper-preflight-duality_confinement paper-preflight-rh paper-preflight \
	paper-clean-duality_confinement paper-clean-rh paper-clean \
	audit-check audit-regenerate audit-regenerate-full \
	validate test

.NOTPARALLEL:

help:
	@echo "Paper targets:"
	@echo "  paper-build-duality_confinement     Build Duality Confinement paper PDF at $(DC_DIR)/build/main.pdf"
	@echo "  paper-build-rh                      Build RH paper PDF at $(RH_DIR)/build/main.pdf"
	@echo "  paper-build                         Build both paper PDFs"
	@echo "  paper-preflight-duality_confinement Build, lint, and log-check the Duality Confinement paper"
	@echo "  paper-preflight-rh                  Build, lint, and log-check the RH paper"
	@echo "  paper-preflight                     Preflight both papers and run registry/Lean validators"
	@echo "  paper-clean-duality_confinement     Remove Duality Confinement paper build artifacts"
	@echo "  paper-clean-rh                      Remove RH paper build artifacts"
	@echo "  paper-clean                         Remove build artifacts for both papers"
	@echo ""
	@echo "Foundations-audit targets (artifact mode must match check_lean.py's invocation):"
	@echo "  audit-check                         Verify committed audit artifacts (--check --skip-validation)"
	@echo "  audit-regenerate                    Regenerate audit artifacts in the safe mode (--skip-validation)"
	@echo "  audit-regenerate-full               Regenerate WITH upstream-validator side effects (no flags); use only if you intend to commit a validation_status=passed artifact shape and update check_lean.py to match"
	@echo ""
	@echo "Validator orchestration:"
	@echo "  validate                            Run the full validator chain (no Lean build)"
	@echo "  test                                Run pytest on the validator unit tests"
	@echo ""
	@echo "  help                                Show this target list"

paper-build-duality_confinement:
	cd $(DC_DIR) && $(LATEXMK) main.tex

paper-build-rh:
	cd $(RH_DIR) && $(LATEXMK) main.tex

paper-build: paper-build-duality_confinement paper-build-rh

paper-preflight-duality_confinement: paper-build-duality_confinement
	scripts/paper_lint.sh $(DC_DIR)
	@log="$(DC_DIR)/build/main.log"; \
	test -f "$$log" || { echo "error: missing build log $$log"; exit 1; }; \
	if grep -nE 'Underfull|Overfull|Float too large|undefined references|undefined citations|Reference .* undefined|Citation .* undefined|There were undefined|Cref Cref|\\\\Cref.*\\\\Cref' "$$log"; then \
	  echo "error: Duality Confinement paper build log contains layout/reference warnings"; \
	  exit 1; \
	fi

paper-preflight-rh: paper-build-rh
	scripts/paper_lint.sh $(RH_DIR)
	@log="$(RH_DIR)/build/main.log"; \
	test -f "$$log" || { echo "error: missing build log $$log"; exit 1; }; \
	if grep -nE 'Underfull|Overfull|Float too large|undefined references|undefined citations|Reference .* undefined|Citation .* undefined|There were undefined|Cref Cref|\\\\Cref.*\\\\Cref' "$$log"; then \
	  echo "error: RH paper build log contains layout/reference warnings"; \
	  exit 1; \
	fi

paper-preflight: paper-preflight-duality_confinement paper-preflight-rh
	python3 scripts/check_statements_of_record.py --check
	python3 scripts/check_manifests.py --check
	python3 scripts/check_lean.py --skip-build

paper-clean-duality_confinement:
	rm -rf $(DC_DIR)/build
	@for ext in $(PAPER_AUX_EXTS); do rm -f "$(DC_DIR)"/*.$$ext; done

paper-clean-rh:
	rm -rf $(RH_DIR)/build
	@for ext in $(PAPER_AUX_EXTS); do rm -f "$(RH_DIR)"/*.$$ext; done

paper-clean: paper-clean-duality_confinement paper-clean-rh

audit-check:
	python3 scripts/audit_foundations_dependencies.py --check --skip-validation

audit-regenerate:
	python3 scripts/audit_foundations_dependencies.py --skip-validation

audit-regenerate-full:
	@echo "WARNING: this regenerates with validation_status=passed; check_lean.py will then"
	@echo "flag the artifacts as stale unless its --skip-validation invocation is also changed."
	python3 scripts/audit_foundations_dependencies.py

validate:
	python3 scripts/check_lean.py --skip-build
	python3 scripts/check_manifests.py --check
	python3 scripts/check_statements_of_record.py --check
	python3 scripts/audit_foundations_dependencies.py --check --skip-validation
	python3 scripts/check_foundations_provenance.py --check
	python3 scripts/check_semantic_alignment.py --check

test:
	python3 -m pytest scripts/test_check_manifests.py
