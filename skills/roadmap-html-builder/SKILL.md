---
name: roadmap-html-builder
description: |
  Takes a structured technology learning roadmap (stages, topics, resource links, time estimates) and renders it into a polished, self-contained HTML page using the bundled reusable template.html, so every generated roadmap shares the same consistent visual design.
  Use after roadmap content has been researched (typically via the ms-learn-research skill), when the user wants the roadmap rendered as an HTML page/visual roadmap, or asks things like "turn this into an HTML roadmap page", "make this a visual roadmap", "render this as a webpage", or "give me an HTML version of this roadmap".
license: MIT
metadata:
  author: MS Skill Mastery Demo
  version: "1.0"
---

# Roadmap HTML Builder Skill

## What This Skill Does

Converts a structured learning roadmap (skill name, summary, ordered stages, topics, resource links, time estimates — as produced by the `ms-learn-research` skill) into a finished, self-contained HTML file by filling in the bundled template:

```
skills/roadmap-html-builder/template.html
```

Always load and reuse this exact template file for every generation. **Never invent a new HTML layout from scratch** — the whole point of this skill is that every roadmap the user generates, regardless of topic, shares the same polished design. Only the content (skill name, stages, topics, links, time estimates) changes between generations.

## When to Use This Skill

Activate this skill when:
- The user has just received a structured roadmap (JSON block) from the `ms-learn-research` skill and now wants it turned into a page/site/HTML.
- The user directly asks for "an HTML roadmap", "a visual roadmap page", "render this as a webpage", etc., and roadmap content is available in the conversation.

If no structured roadmap content exists yet in the conversation, first run the `ms-learn-research` skill's workflow (or ask the user for the skill name) to obtain it before rendering.

## Workflow

### Step 1: Obtain Structured Roadmap Content

Use the structured JSON roadmap block from the `ms-learn-research` skill's output (shape: `skillName`, `summary`, `stages[]`, each stage with `title`, `estimatedTime`, `topics[]`, each topic with `name`, `description`, `resourceTitle`, `resourceUrl`).

### Step 2: Load the Template

Open `skills/roadmap-html-builder/template.html` (bundled in this skill folder). This file contains:
- Top-level placeholders: `{{SKILL_NAME}}`, `{{SUMMARY}}`, `{{GENERATED_DATE}}`
- A **STAGE BLOCK**, delimited by `<!-- STAGE_BLOCK_START -->` / `<!-- STAGE_BLOCK_END -->` HTML comments, with placeholders: `{{STAGE_INDEX}}`, `{{STAGE_LEVEL_CLASS}}` (`beginner` | `intermediate` | `advanced`), `{{STAGE_TITLE}}`, `{{STAGE_TIME}}`, `{{STAGE_TOPICS}}`
- A **TOPIC BLOCK** nested inside the stage block, delimited by `<!-- TOPIC_BLOCK_START -->` / `<!-- TOPIC_BLOCK_END -->`, with placeholders: `{{TOPIC_NAME}}`, `{{TOPIC_DESCRIPTION}}`, `{{RESOURCE_URL}}`, `{{RESOURCE_TITLE}}`

### Step 3: Fill the Template

1. Replace the top-level placeholders once (`{{SKILL_NAME}}`, `{{SUMMARY}}`, `{{GENERATED_DATE}}` — use today's date).
2. For each stage in the roadmap (in order), duplicate the STAGE BLOCK section and fill in its placeholders. Map stage order to `{{STAGE_LEVEL_CLASS}}`: 1st stage → `beginner`, 2nd → `intermediate`, 3rd+ → `advanced` (reuse `advanced` for any extra stages beyond three).
3. Within each stage's duplicated block, for every topic in that stage, duplicate the nested TOPIC BLOCK `<li>` and fill in its placeholders. Concatenate all topic `<li>` elements together to replace the topics area (remove the `{{STAGE_TOPICS}}` token and the topic block's own comment markers in the final output — they are authoring guides only, not meant to remain in the final file).
4. Remove the `STAGE_BLOCK_START` / `STAGE_BLOCK_END` comment markers from the final output as well — they exist only to show where to duplicate.

### Step 4: Produce the Final Output

Output one complete, self-contained HTML file (inline CSS, no external dependencies, opens directly in any browser) with all placeholders replaced and no leftover `{{...}}` tokens or authoring comments. Suggest a filename like `<skill-name>-roadmap.html` (kebab-case) and present the full HTML so the user can save it, or write it to disk if the environment supports file creation.

## Output Format

A single, complete HTML document, ready to open in a browser, that:
- Uses the exact visual design of `template.html` (do not alter colors, layout, or CSS — only fill content)
- Displays the skill name, summary, and generation date in the header
- Shows one styled stage card per roadmap stage, in order, each with its time-estimate badge and topic list
- Includes working links to the Microsoft Learn resources cited by `ms-learn-research`

## Notes

- The template is intentionally reused as-is for every topic — this is what keeps the visual design consistent across different skills/technologies. Do not redesign it per request.
- If a roadmap has more than 3 stages, all stages beyond the third should use the `advanced` color class unless the roadmap author specifies otherwise.
- Keep topic descriptions concise (1-2 sentences) so cards stay visually balanced, matching the density shown in the template.
