param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' })
)

$ErrorActionPreference = 'Stop'

$agentsPath = Join-Path $CodexHome 'AGENTS.md'
$startMarker = '<!-- MPE_GLOBAL_POLICY_START -->'
$endMarker = '<!-- MPE_GLOBAL_POLICY_END -->'

$managedBlock = @"
$startMarker
# Murat Project Engineer — Global Rule

Before implementing or recommending implementation of any new product, feature, service, agent, plugin, integration, automation, repository, or substantial technical idea for Murat projects, first apply the Murat Project Engineer New Idea Filter.

Required checks:
1. Existing active project overlap.
2. EXTEND_EXISTING / REUSE_COMPONENT / MERGE opportunities before new construction.
3. Duplicate functionality or infrastructure.
4. Measurable user/business outcome.
5. Smallest validation experiment or MVP.
6. Portfolio priority and opportunity cost.
7. Deep-change risk.

Record exactly one primary disposition before implementation:
- EXTEND_EXISTING
- REUSE_COMPONENT
- MERGE
- EXPERIMENT
- HOLD
- NEW_REPOSITORY
- REJECT

Do not start substantial implementation or create a new repository before the disposition is recorded.
If a proposal conflicts with current foundation, architecture, scope, or deep-change rules, stop and require explicit user approval before implementation.
Prefer strengthening existing active projects over creating parallel systems.

Canonical policy: Murkin1980/murat-project-engineer `docs/NEW_IDEA_FILTER_POLICY.md` and `docs/GLOBAL_MPE_ENFORCEMENT.md`.
$endMarker
"@

New-Item -ItemType Directory -Force -Path $CodexHome | Out-Null

if (Test-Path $agentsPath) {
    $existing = Get-Content -Raw -Path $agentsPath
    $pattern = [regex]::Escape($startMarker) + '.*?' + [regex]::Escape($endMarker)
    if ([regex]::IsMatch($existing, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)) {
        $updated = [regex]::Replace(
            $existing,
            $pattern,
            [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $managedBlock },
            [System.Text.RegularExpressions.RegexOptions]::Singleline
        )
    } else {
        $separator = if ($existing.EndsWith("`n")) { "`n" } else { "`n`n" }
        $updated = $existing + $separator + $managedBlock + "`n"
    }
} else {
    $updated = $managedBlock + "`n"
}

Set-Content -Path $agentsPath -Value $updated -Encoding UTF8

Write-Host "MPE global Codex policy installed: $agentsPath"
Write-Host "Restart Codex sessions so new instructions are loaded."
