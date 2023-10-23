# CHANGELOG



## v0.1.1 (2023-10-23)

### Fix

* fix: update github workflow for releases ([`387b1be`](https://github.com/dskard/pytest-html-report-merger/commit/387b1be6964c632b6ec79e11398f7d1aa40c20b4))


## v0.1.0 (2023-10-23)

### Breaking

* fix: updating command to work with pytest-html version 4.0.0+

BREAKING CHANGE: this will not work with pytest-html reports generated
with versions below 4.0.0 ([`5d2f448`](https://github.com/dskard/pytest-html-report-merger/commit/5d2f44810eeaaa3af810eff5b2180cc20421b2f2))

### Chore

* chore: in Makefile, automatically install the projects dependencies ([`45ef763`](https://github.com/dskard/pytest-html-report-merger/commit/45ef76394dcf885a46f034f2261d921f0cd109de))

* chore: set up pre-commit, format files ([`c9138ac`](https://github.com/dskard/pytest-html-report-merger/commit/c9138ac1f084530d0d3920eb956aee6db0ead79c))

### Ci

* ci: bump versions of github actions ([`d30859a`](https://github.com/dskard/pytest-html-report-merger/commit/d30859a0dabc6b12e02c9a7b8badc6f3ed6c969c))

### Unknown

* Merge pull request #2 from dskard/dsk-pytest-html-4

fix: updating command to work with pytest-html version 4.0.0+ ([`16d6e39`](https://github.com/dskard/pytest-html-report-merger/commit/16d6e39a49817e402302838347046d9eae784cf2))


## v0.0.1 (2022-08-31)

### Fix

* fix: add github actions for versioning and publishing ([`c44af0a`](https://github.com/dskard/pytest-html-report-merger/commit/c44af0a2d708146aedf56c5f7c1ae3bc44295bd9))

### Unknown

* Merge pull request #1 from dskard/dsk-gha

fix: add github actions for versioning and publishing ([`632a569`](https://github.com/dskard/pytest-html-report-merger/commit/632a5695700c20cf738e7f9a0144f020c518684a))

* upload code to combine html reports from pytest-html

example usage:
pytest-html-report-merger --out merged.html report_*.html ([`a489d2b`](https://github.com/dskard/pytest-html-report-merger/commit/a489d2b389f14ef4d69d898445d87028adb18bc5))

* Update README.md ([`b47f5a7`](https://github.com/dskard/pytest-html-report-merger/commit/b47f5a77d7f0db317540b7c020d38b573d2d475b))

* Initial commit ([`e9b4a82`](https://github.com/dskard/pytest-html-report-merger/commit/e9b4a82e664480e5428e6968e3a40ccbcc9cd6eb))
