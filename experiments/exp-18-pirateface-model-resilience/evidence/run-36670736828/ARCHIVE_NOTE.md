# Archived evidence — harness run 36670736828

This directory is a verbatim copy of the evidence produced by GitHub Actions run
[36670736828](https://github.com/Murkin1980/murat-project-engineer/actions/runs/36670736828)
(commit `bef8985`, 2026-09-30 04:51–05:08 UTC).

It is kept because the harness writes its evidence to the flat `evidence/`
directory, so a later run overwrites it. The flat directory holds the most recent
run; this directory preserves the first run of this session.

Both runs test the same pinned artifact and the same archive; see
`../../FINDINGS.md` for the comparison.

Notes specific to this run: the three torrent stages were stopped by the
harness's own stage budget (`exit=124`, `wall_seconds=331`) after the payload had
already been downloaded, because aria2c's RPC server keeps the process alive
after a transfer finishes. The payload itself is complete and hash-verified; see
`07_*_aria2c.log` ("Download complete", average speed) and the manifests in this
directory.
