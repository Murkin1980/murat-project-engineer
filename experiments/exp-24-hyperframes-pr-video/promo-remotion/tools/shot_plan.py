#!/usr/bin/env python3
"""EXP-24 Phase 2 — shot plan (creative decomposition of the OWNER SCRIPT).

This file does NOT contain narration wording. Narration is read from
`SALAMAT_PROMO_SCRIPT.md`, which is the narrative source-of-truth.

What lives here is only the shot decomposition: how each approved script scene is
broken into filmable beats, which footage each beat needs, and where the approved
on-screen text appears. Shot durations sum to the script's own timecodes.

Rules encoded:
  * narration parts are *slices* of the approved narration — the builder proves
    concatenation is verbatim;
  * overlay text is copied from the script's "On-screen text" section — no extra
  on-screen labels are invented (the builder rejects any overlay string that is not
  in the approved script);
  * `media_authority` is REAL_FOOTAGE (Storyblocks first) for every ordinary beat;
  * `generative` is "none" except where the script explicitly allows motion
    graphics / logo reveal (scene 1 wordmark, scene 9 end card).
"""

from __future__ import annotations

# script_scene number -> {shots: [...]}
# beat duration is in seconds and must sum to the script scene's own duration.
SHOTS: dict[int, list[dict]] = {
    1: [
        {
            "id": "open-interior",
            "duration": 5.0,
            "narration_part": "Дом становится по-настоящему вашим тогда,",
            "visual_intent": "Premium contemporary interior in warm evening light; slow push-in "
                             "through the kitchen toward the cabinetry so material and finish read first.",
            "footage_queries": [
                "premium modern kitchen interior slow dolly warm evening light",
                "contemporary interior cabinetry slow push in",
            ],
            "fallback_queries": [
                "luxury kitchen dark wood surfaces slow pan",
                "modern apartment interior warm light slow move",
            ],
            "overlay": {"title": "SALAMAT MEBEL",
                        "subtitle": "Мебель, созданная под ваше пространство",
                        "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–5.0 s · hold on the strongest part of the clip; wordmark layer "
                             "fades in at 3.6 s and holds into the next beat",
            "framing_note": "interior first, brand second; no readable text inside the footage",
            "generative_allowance": "logo_reveal_overlay",
        },
        {
            "id": "open-detail",
            "duration": 3.0,
            "narration_part": "когда каждая вещь находится на своём месте.",
            "visual_intent": "Macro of cabinet fronts and a single hardware detail, matching the tone "
                             "of the opening shot — the film's promise shown as craft, not copy.",
            "footage_queries": [
                "cabinet front material texture macro brass handle detail",
                "furniture joinery detail macro slow motion",
            ],
            "fallback_queries": [
                "kitchen drawer handle closeup slow motion",
                "wood surface texture macro interior detail",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–3.0 s · short macro beat, continues the opening move without a cut",
            "framing_note": "macro only; no people, no readable branding",
            "generative_allowance": "none",
        },
    ],
    2: [
        {
            "id": "task-measure",
            "duration": 7.0,
            "narration_part": "Поэтому мы не просто изготавливаем мебель.",
            "visual_intent": "Room measurement: laser measure or tape against a wall, floor plan in "
                             "hand. Hands and instruments carry the shot.",
            "footage_queries": [
                "carpenter measuring wall laser distance meter interior",
                "hand holding tape measure wall renovation closeup",
            ],
            "fallback_queries": [
                "measuring room dimensions interior planning",
                "worker laser meter wall marking closeup",
            ],
            "overlay": {"title": "Замер → проект → производство → монтаж",
                        "subtitle": None, "label": None},
            "motion": "drift-left",
            "in_out_intent": "0.0–7.0 s · overlay enters at 0.8 s and holds for the whole beat",
            "framing_note": "hands/tools only, no faces",
            "generative_allowance": "none",
        },
        {
            "id": "task-habits",
            "duration": 7.0,
            "narration_part": "Мы начинаем с пространства, задачи и привычек человека, "
                              "который будет ею пользоваться.",
            "visual_intent": "Designer reviewing the project with the client: sketches, screen or "
                             "drawings on the table while the room's real geometry is discussed.",
            "footage_queries": [
                "designer reviewing plans with client interior table",
                "interior designer explaining drawings client consultation",
            ],
            "fallback_queries": [
                "two people looking at floor plan table interior design",
                "architect hands pointing at kitchen drawing",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "drift-left",
            "in_out_intent": "0.0–7.0 s · slow lateral move across the table",
            "framing_note": "avoid close faces so no real person is identifiable; drawings must not "
                            "be readable documents",
            "generative_allowance": "none",
        },
    ],
    3: [
        {
            "id": "project-drawings",
            "duration": 7.0,
            "narration_part": "Кухня, шкаф, гардеробная или мебель для бизнеса начинается с проекта.",
            "visual_intent": "Designer at work: drawings and technical plans, hands on paper, screen "
                             "with cabinet geometry.",
            "footage_queries": [
                "interior designer drawing furniture plan hands workshop",
                "technical furniture drawing cad screen designer closeup",
            ],
            "fallback_queries": [
                "architect sketching kitchen layout paper",
                "designer working on furniture project desk",
            ],
            "overlay": {"title": "Мебель под конкретное помещение",
                        "subtitle": None, "label": None},
            "motion": "drift-right",
            "in_out_intent": "0.0–7.0 s · push across the drawings; overlay enters at 0.8 s",
            "framing_note": "hands and drawings; no readable client data",
            "generative_allowance": "none",
        },
        {
            "id": "project-selection",
            "duration": 7.0,
            "narration_part": "Размеры, материалы, цвет, наполнение — всё собирается в одно решение.",
            "visual_intent": "Selection: material samples, boards and hardware laid out and compared; "
                             "hands moving pieces into a decision.",
            "footage_queries": [
                "material samples boards laminate veneer selection hands table",
                "cabinet hardware samples handles hinges comparison"
            ],
            "fallback_queries": [
                "wood and stone samples interior design selection",
                "choosing fabric and finish swatches showroom",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "drift-right",
            "in_out_intent": "0.0–7.0 s · glide across the samples, no cut inside the beat",
            "framing_note": "samples/hardware only, no supplier branding",
            "generative_allowance": "none",
        },
    ],
    4: [
        {
            "id": "prod-cutting",
            "duration": 6.0,
            "narration_part": "Затем проект переходит в производство.",
            "visual_intent": "Panel cutting on industrial equipment; the project becomes parts.",
            "footage_queries": [
                "panel saw cutting laminated board furniture factory",
                "cnc nesting machine cutting wood panel workshop",
            ],
            "fallback_queries": [
                "industrial cutting machine wood panel production",
                "furniture factory cutting line panels",
            ],
            "overlay": {"title": "Точность в каждой детали", "subtitle": None, "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–6.0 s · push toward the cut; overlay enters at 0.6 s",
            "framing_note": "no readable machine branding or software UI",
            "generative_allowance": "none",
        },
        {
            "id": "prod-processing",
            "duration": 6.0,
            "narration_part": "Детали раскраиваются, обрабатываются",
            "visual_intent": "Edgebanding and drilling: the processing step where the quality of the "
                             "future surface is decided.",
            "footage_queries": [
                "edge banding machine processing panel furniture factory closeup",
                "drilling machine cabinet parts workshop production"
            ],
            "fallback_queries": [
                "edgebander applying edge to panel closeup",
                "cnc drilling cabinet part holes workshop",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–6.0 s · macro push-in following the panel through the machine",
            "framing_note": "machine and panel must stay the subject; no faces required",
            "generative_allowance": "none",
        },
        {
            "id": "prod-assembly",
            "duration": 7.0,
            "narration_part": "и собираются с точностью, от которой зависит конечный результат.",
            "visual_intent": "Assembly and craft detail: parts coming together, clamps, checking the fit.",
            "footage_queries": [
                "cabinet assembly workshop clamps furniture carcase",
                "craftsman assembling cabinet frame workshop hands",
            ],
            "fallback_queries": [
                "furniture assembly bench worker hands closeup",
                "joining cabinet parts workshop detail",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–7.0 s · move along the assembly bench, hold on the hands at the end",
            "framing_note": "hands/gloved hands, no identifiable faces",
            "generative_allowance": "none",
        },
    ],
    5: [
        {
            "id": "tactile-hero",
            "duration": 7.0,
            "narration_part": "Хорошая мебель ощущается сразу — в фактуре поверхности,",
            "visual_intent": "MANDATORY HERO SHOT (owner note). Slow camera glide along a kitchen "
                             "countertop, close/medium-close; a hand runs across the surface and "
                             "visibly feels the texture; soft side light rakes the surface so texture, "
                             "edge and finish read clearly. Communicates tactile quality, craftsmanship "
                             "and the pleasure of touching good furniture — not a catalogue product shot.",
            "footage_queries": [
                "hand sliding across kitchen countertop surface texture slow glide",
                "touching countertop stone surface texture slow motion closeup",
            ],
            "fallback_queries": [
                "fingers running across wooden worktop surface",
                "hand feeling marble countertop texture kitchen",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–7.0 s · one uninterrupted glide; the hand crosses the surface once, "
                             "slowly, with no cut inside the beat",
            "framing_note": "REAL licensed footage only. If Storyblocks is unavailable, this beat stays "
                            "unresolved and the blocker is recorded — it is never replaced by generated "
                            "media (owner script, scene 5).",
            "generative_allowance": "none",
        },
        {
            "id": "materials-hardware",
            "duration": 6.0,
            "narration_part": "в точности деталей и в том, как ею пользуешься каждый день.",
            "visual_intent": "Supporting detail: facades, hardware, drawer runners and hinges, a smooth "
                             "closing movement, material edges and finishing.",
            "footage_queries": [
                "soft close drawer runner hinge mechanism closeup slow motion",
                "cabinet facade edge finishing detail kitchen closeup",
            ],
            "fallback_queries": [
                "drawer closing smoothly kitchen hardware detail",
                "handle and hinge macro furniture craftsmanship",
            ],
            "overlay": {"title": "Материалы • фасады • фурнитура", "subtitle": None, "label": None},
            "motion": "push-in",
            "in_out_intent": "0.0–6.0 s · two micro-beats inside one move; overlay enters at 0.8 s",
            "framing_note": "no hardware brand names visible",
            "generative_allowance": "none",
        },
    ],
    6: [
        {
            "id": "range-kitchen-storage",
            "duration": 6.0,
            "narration_part": "Salamat Mebel делает кухни, шкафы и системы хранения,",
            "visual_intent": "Calm sequence opens with a finished kitchen, then built-in storage or a "
                             "walk-in system — one idea per shot, no catalogue rush.",
            "footage_queries": [
                "finished modern kitchen interior slow pan cabinets",
                "built in wardrobe storage system interior opening",
            ],
            "fallback_queries": [
                "handleless kitchen interior premium",
                "walk in closet built in shelves interior",
            ],
            "overlay": {"title": "Для дома и бизнеса", "subtitle": None, "label": None},
            "motion": "drift-left",
            "in_out_intent": "0.0–6.0 s · two matched moves, kitchen then storage; overlay enters at 0.8 s",
            "framing_note": "no people; interiors must be finished and styled, not construction sites",
            "generative_allowance": "none",
        },
        {
            "id": "range-home-rooms",
            "duration": 6.0,
            "narration_part": "мебель для детских, ванных и гостиных,",
            "visual_intent": "Three short matched shots: children's room, bathroom furniture, TV zone / "
                             "living room.",
            "footage_queries": [
                "children room built in furniture interior daylight",
                "bathroom vanity cabinet modern interior",
                "tv wall unit living room built in furniture",
            ],
            "fallback_queries": [
                "kids bedroom storage furniture interior",
                "bathroom wood cabinet interior design",
                "media wall tv unit living room interior",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "drift-left",
            "in_out_intent": "0.0–6.0 s · three ~2 s matched shots in identical camera language",
            "framing_note": "same grade and framing logic across the three shots so the sequence reads "
                            "as one film",
            "generative_allowance": "none",
        },
        {
            "id": "range-commercial",
            "duration": 7.0,
            "narration_part": "а также решения для магазинов, офисов и других коммерческих пространств.",
            "visual_intent": "Commercial furniture: reception, retail or office millwork at work in a "
                             "finished space.",
            "footage_queries": [
                "reception desk millwork modern office interior",
                "retail store fit out wooden counter interior",
            ],
            "fallback_queries": [
                "modern office interior built in cabinetry",
                "shop counter furniture commercial interior",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "drift-left",
            "in_out_intent": "0.0–7.0 s · slow drift across the commercial interior; last shot of the "
                             "range sequence",
            "framing_note": "no readable company names or signage",
            "generative_allowance": "none",
        },
    ],
    7: [
        {
            "id": "install-fitting",
            "duration": 8.0,
            "narration_part": "Но хороший проект заканчивается не в цеху.",
            "visual_intent": "Installers fitting cabinetry on site: levelling, aligning facades, "
                             "protecting the floor.",
            "footage_queries": [
                "furniture installers fitting kitchen cabinets interior level",
                "workers installing cabinet units home alignment",
            ],
            "fallback_queries": [
                "kitchen installation worker mounting cabinet doors",
                "fitting countertop installers kitchen",
            ],
            "overlay": {"title": "От проекта до установки", "subtitle": None, "label": None},
            "motion": "drift-right",
            "in_out_intent": "0.0–8.0 s · follow the fitting work; overlay enters at 0.8 s",
            "framing_note": "hands, tools, tools-on-furniture; avoid identifiable faces",
            "generative_allowance": "none",
        },
        {
            "id": "install-adjust",
            "duration": 7.0,
            "narration_part": "Он заканчивается тогда, когда мебель установлена, всё отрегулировано "
                              "и пространство начинает работать так, как было задумано.",
            "visual_intent": "Adjustment and handover: hinges and hardware tuned, doors aligned, the "
                             "space finally working as designed.",
            "footage_queries": [
                "adjusting cabinet hinge door alignment closeup",
                "installer checking kitchen cabinet doors alignment",
            ],
            "fallback_queries": [
                "screwdriver adjusting furniture hinge detail",
                "final check kitchen installation cabinets",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "drift-right",
            "in_out_intent": "0.0–7.0 s · push in on the adjustment, end on the aligned facade",
            "framing_note": "detail level; the last beat before the result section",
            "generative_allowance": "none",
        },
    ],
    8: [
        {
            "id": "result-space",
            "duration": 11.0,
            "narration_part": "В результате получается не просто набор шкафов. Получается "
                              "пространство, сделанное именно для вас.",
            "visual_intent": "Strong finished-interior shots: light, details, cabinetry opening, real "
                             "interaction with the furniture. Quiet, confident, unhurried.",
            "footage_queries": [
                "finished interior kitchen built in furniture wide daylight",
                "opening cabinet doors modern kitchen slow motion interior",
            ],
            "fallback_queries": [
                "bright modern interior cabinetry wide shot",
                "person opening kitchen cabinet interior warm light",
            ],
            "overlay": {"title": None, "subtitle": None, "label": None},
            "motion": "push-out",
            "in_out_intent": "0.0–11.0 s · the film's longest hold: light, then detail, then the "
                             "cabinet opening; no overlay copy",
            "framing_note": "no overlay text in this beat — let the interior carry it",
            "generative_allowance": "none",
        },
    ],
    9: [
        {
            "id": "brand-close",
            "duration": 7.0,
            "narration_part": "Salamat Mebel. Мебель, созданная под ваше пространство.",
            "visual_intent": "Clean branded final frame: wordmark over a dark material surface with a "
                             "thin brass rule; neutral positioning line underneath. No contact data.",
            "footage_queries": [],
            "fallback_queries": [],
            "overlay": {"title": "SALAMAT MEBEL",
                        "subtitle": "Мебель, созданная под ваше пространство",
                        "label": None},
            "motion": "hold",
            "in_out_intent": "0.0–7.0 s · wordmark and rule animate in, tagline holds for the final 2 s",
            "framing_note": "generative allowed here by the script (motion graphics / logo reveal); "
                            "no phone, address, site or social handles — no verified contact data",
            "generative_allowance": "branded_motion_graphic",
        },
    ],
}

GENERATIVE_ALLOWLIST = {
    "logo_reveal": "logo reveal (wordmark layer over licensed footage)",
    "branded_motion_graphic": "branded end card / logo reveal",
}
