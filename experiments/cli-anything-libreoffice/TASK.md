# Frozen task

Create `mpe-cli-anything-test.xlsx` through the existing CLI-Anything
LibreOffice harness, not through a spreadsheet library or hand-generated OOXML.
The workbook must contain an `Order` sheet with:

| Product | Qty | Unit Price | Total |
|---|---:|---:|---:|
| Panel A | 12 | 8500 | `=B2*C2` |
| Panel B | 5 | 12500 | `=B3*C3` |
| Hardware | 30 | 1800 | `=B4*C4` |
| GRAND TOTAL |  |  | `=SUM(D2:D4)` |

The expected calculated values are 102000, 62500, 54000, and a grand total of
218500. The experiment requires independent OOXML verification, a real
LibreOffice headless round-trip where possible, and a second clean semantic run.

The task was not executed because the sandbox could not provide a real
LibreOffice dependency. No XLSX artifact was created.
