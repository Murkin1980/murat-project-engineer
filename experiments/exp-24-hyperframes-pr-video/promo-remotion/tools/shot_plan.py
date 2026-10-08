#!/usr/bin/env python3
"""EXP-24 Phase 2 — CP-06 shot plan.

Compact decomposition of the OWNER SCRIPT (`SALAMAT_PROMO_SCRIPT.md`).
No narration wording is authored here: each beat carries only the slice of the approved
narration it covers, and the builder proves the slices rejoin verbatim.

Row = (id, seconds, narration slice, Storyblocks query, fallback query, motion,
       on-screen title, on-screen subtitle, intent)
Overlay columns may only repeat text from the script's own "On-screen text" section.
"""

from __future__ import annotations

PLAN: dict[int, list[tuple]] = {
    1: [
        ("open-interior", 5, "Дом становится по-настоящему вашим тогда,",
         "premium modern kitchen interior slow dolly warm evening light",
         "luxury kitchen dark wood surfaces slow pan", "push-in",
         "SALAMAT MEBEL", "Мебель, созданная под ваше пространство",
         "Premium interior, slow push-in through the kitchen; material and finish read first, "
         "wordmark appears at 3.6 s and holds."),
        ("open-detail", 3, "когда каждая вещь находится на своём месте.",
         "cabinet front material texture macro brass handle detail",
         "wood surface texture macro interior detail", "push-in", None, None,
         "Macro of fronts and one hardware detail — the promise shown as craft, not copy."),
    ],
    2: [
        ("task-measure", 7, "Поэтому мы не просто изготавливаем мебель.",
         "carpenter measuring wall laser distance meter interior",
         "hand holding tape measure wall renovation closeup", "drift-left",
         "Замер → проект → производство → монтаж", None,
         "Room measurement with laser measure or tape; hands and instruments carry the shot."),
        ("task-habits", 7,
         "Мы начинаем с пространства, задачи и привычек человека, который будет ею пользоваться.",
         "designer reviewing plans with client interior table",
         "architect hands pointing at kitchen drawing", "drift-left", None, None,
         "Designer and client over plans and drawings; room geometry is discussed, faces avoidable."),
    ],
    3: [
        ("project-drawings", 7,
         "Кухня, шкаф, гардеробная или мебель для бизнеса начинается с проекта.",
         "interior designer drawing furniture plan hands workshop",
         "architect sketching kitchen layout paper", "drift-right",
         "Мебель под конкретное помещение", None,
         "Designer at work: drawings, technical plans, hands on paper."),
        ("project-selection", 7,
         "Размеры, материалы, цвет, наполнение — всё собирается в одно решение.",
         "material samples boards laminate veneer selection hands table",
         "wood and stone samples interior design selection", "drift-right", None, None,
         "Samples, boards and hardware compared on the table; hands make the decision."),
    ],
    4: [
        ("prod-cutting", 6, "Затем проект переходит в производство.",
         "panel saw cutting laminated board furniture factory",
         "industrial cutting machine wood panel production", "push-in",
         "Точность в каждой детали", None,
         "Panel cutting on industrial equipment; the project becomes parts."),
        ("prod-processing", 6, "Детали раскраиваются, обрабатываются",
         "edge banding machine processing panel furniture factory closeup",
         "edgebander applying edge to panel closeup", "push-in", None, None,
         "Edgebanding and drilling: where the quality of the future surface is decided."),
        ("prod-assembly", 7, "и собираются с точностью, от которой зависит конечный результат.",
         "cabinet assembly workshop clamps furniture carcase",
         "furniture assembly bench worker hands closeup", "push-in", None, None,
         "Assembly and craft detail: parts coming together, clamps, fit checked."),
    ],
    5: [
        ("tactile-hero", 7, "Хорошая мебель ощущается сразу — в фактуре поверхности,",
         "hand sliding across kitchen countertop surface texture slow glide",
         "touching countertop stone surface texture slow motion closeup", "push-in", None, None,
         "MANDATORY HERO SHOT (owner note). Slow glide along a kitchen countertop, close framing; a "
         "hand runs across the surface and visibly feels the texture; soft side light rakes texture, "
         "edge and finish. Tactile quality, not a catalogue shot. REAL footage only — never replaced "
         "by generated media."),
        ("materials-hardware", 6,
         "в точности деталей и в том, как ею пользуешься каждый день.",
         "soft close drawer runner hinge mechanism closeup slow motion",
         "drawer closing smoothly kitchen hardware detail", "push-in",
         "Материалы • фасады • фурнитура", None,
         "Supporting details: facades, hardware, runners, a smooth closing movement, edges."),
    ],
    6: [
        ("range-kitchen-storage", 6,
         "Salamat Mebel делает кухни, шкафы и системы хранения,",
         "finished modern kitchen interior slow pan cabinets",
         "walk in closet built in shelves interior", "drift-left",
         "Для дома и бизнеса", None,
         "Kitchen, then built-in storage or walk-in system — one idea per shot, no rush."),
        ("range-home-rooms", 6, "мебель для детских, ванных и гостиных,",
         "children room built in furniture interior daylight",
         "kids bedroom storage furniture interior", "drift-left", None, None,
         "Three matched ~2 s shots: children's room, bathroom furniture, TV zone."),
        ("range-commercial", 7,
         "а также решения для магазинов, офисов и других коммерческих пространств.",
         "reception desk millwork modern office interior",
         "shop counter furniture commercial interior", "drift-left", None, None,
         "Commercial millwork in a finished space; no readable signage."),
    ],
    7: [
        ("install-fitting", 8, "Но хороший проект заканчивается не в цеху.",
         "furniture installers fitting kitchen cabinets interior level",
         "kitchen installation worker mounting cabinet doors", "drift-right",
         "От проекта до установки", None,
         "Installers fitting cabinetry on site: levelling, aligning facades, floor protected."),
        ("install-adjust", 7,
         "Он заканчивается тогда, когда мебель установлена, всё отрегулировано "
         "и пространство начинает работать так, как было задумано.",
         "adjusting cabinet hinge door alignment closeup",
         "final check kitchen installation cabinets", "drift-right", None, None,
         "Hinges and hardware tuned, doors aligned; end on the aligned facade."),
    ],
    8: [
        ("result-space", 11,
         "В результате получается не просто набор шкафов. Получается "
         "пространство, сделанное именно для вас.",
         "finished interior kitchen built in furniture wide daylight",
         "bright modern interior cabinetry wide shot", "push-out", None, None,
         "The film's longest hold: light, detail, cabinetry opening, real interaction — no overlay "
         "copy, the interior carries it."),
    ],
    9: [
        ("brand-close", 7, "Salamat Mebel. Мебель, созданная под ваше пространство.",
         None, None, "hold", "SALAMAT MEBEL", "Мебель, созданная под ваше пространство",
         "Clean branded final frame: wordmark over a dark material surface with a thin brass rule and "
         "the neutral positioning line. No contact data."),
    ],
}

FIELDS = ("id", "seconds", "narration", "query", "fallback", "motion", "title", "subtitle", "intent")
# Beats whose on-screen text the script explicitly allows to carry a branded graphic.
GENERATIVE_ALLOWLIST = {1: "logo reveal", 9: "branded end card"}


def beats_of(scene_number: int) -> list[dict]:
    return [dict(zip(FIELDS, row), owner_directed=row[0] == "tactile-hero")
            for row in PLAN.get(scene_number, [])]
