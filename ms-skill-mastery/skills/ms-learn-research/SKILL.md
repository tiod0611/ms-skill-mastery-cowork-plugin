---
name: ms-learn-research
description: |
  Researches a technology or skill (e.g. React, Azure Kubernetes Service, Python, Microsoft Fabric) using the Microsoft Learn MCP Server and produces a structured, staged learning roadmap with topics, resource links, and time estimates.
  Use when the user asks to learn/master a technology, asks for a learning path/roadmap for a skill, or says things like "I want to master React", "give me a roadmap for Azure Kubernetes Service", "how do I learn Python from scratch", "create a study plan for Microsoft Fabric", or "what should I learn to get good at Kubernetes".
license: MIT
metadata:
  author: MS Skill Mastery Demo
  version: "1.0"
---

# MS Learn Research Skill

## What This Skill Does

Given a technology or skill name, this skill:

1. **Confirms the target skill** the user wants to master (and, if useful, their current level or goal).
2. **Researches** the topic using the **Microsoft Learn MCP Server** connector (`microsoft-learn-mcp`), searching for official documentation, learning paths, and modules.
3. **Organizes** the findings into an ordered, staged learning roadmap (Beginner → Intermediate → Advanced).
4. **Outputs structured roadmap content** (see "Output Format" below) that is designed to be handed directly to the companion `roadmap-html-builder` skill so it can be rendered into a polished HTML page.

## When to Use This Skill

Activate this skill when the user:
- Names a technology/skill and asks to learn, master, or study it
- Asks for a "roadmap", "learning path", "study plan", or "curriculum" for a skill
- Asks "what do I need to learn to become good at X"

Examples: "I want to master React, give me a roadmap", "Azure Kubernetes Service 로드맵 만들어줘", "help me learn Microsoft Fabric from zero to advanced".

## Workflow

### Step 1: Clarify the Target Skill

If not already clear, confirm with the user:
- **Skill/technology name** (exact, e.g. "React", "Azure Kubernetes Service (AKS)")
- **Starting point**, if relevant (complete beginner vs. some experience)
- Any specific goal (e.g. "pass AZ-104", "build a production app")

If the user already stated the skill clearly in their message, do not block on this — proceed with reasonable defaults (assume a beginner-to-advanced full roadmap).

### Step 2: Research via Microsoft Learn MCP Server

Use the `microsoft-learn-mcp` connector (`https://learn.microsoft.com/api/mcp`) to search and fetch documentation for the target skill. Perform multiple searches to cover the full skill arc, for example:

1. Search: "[Skill] getting started introduction"
2. Search: "[Skill] core concepts fundamentals"
3. Search: "[Skill] intermediate patterns best practices"
4. Search: "[Skill] advanced architecture / production / certification"
5. Search: "[Skill] learning path" (Microsoft Learn often has dedicated learning paths — prefer linking directly to these)

Fetch the most relevant docs/module pages so you can extract real titles and URLs — every topic in the roadmap must cite an actual Microsoft Learn resource link returned by the MCP server (do not invent URLs).

### Step 3: Build the Staged Roadmap

Group findings into **ordered stages** — typically:
- **Beginner** (fundamentals, setup, core concepts)
- **Intermediate** (practical patterns, tooling, common workflows)
- **Advanced** (architecture, performance, security, production/certification)

You may use more or fewer stages if the technology naturally calls for it (e.g. add a "Expert / Certification" stage), but always keep them ordered and clearly labeled.

For each stage, produce:
- A short stage title
- An **estimated time** to complete the stage (e.g. "1-2 weeks", "10-15 hours")
- A list of **topics**, each with:
  - Topic name
  - A 1-2 sentence description
  - A Microsoft Learn resource link (title + URL) drawn from the MCP research

### Step 4: Produce Structured Output

Output the roadmap as clearly delimited, structured content (JSON-like) so the `roadmap-html-builder` skill can parse and reuse it directly. Use this exact shape:

```json
{
  "skillName": "React",
  "summary": "One or two sentence overview of what mastering this skill means.",
  "stages": [
    {
      "title": "Beginner",
      "estimatedTime": "2-3 weeks",
      "topics": [
        {
          "name": "JSX & Components",
          "description": "Learn how JSX compiles to React elements and how to compose components.",
          "resourceTitle": "Describe UI with JSX - Microsoft Learn",
          "resourceUrl": "https://learn.microsoft.com/..."
        }
      ]
    },
    {
      "title": "Intermediate",
      "estimatedTime": "3-4 weeks",
      "topics": [ /* ... */ ]
    },
    {
      "title": "Advanced",
      "estimatedTime": "4-6 weeks",
      "topics": [ /* ... */ ]
    }
  ]
}
```

Also present the same content as readable markdown (stage headers, bullet lists with links) directly above or below the JSON block so the user can review it in chat before it's turned into HTML.

## Output Format

The final chat response for this skill must contain:
1. A short intro line confirming the skill being researched.
2. The structured JSON roadmap block (fenced ```json code block, exact shape above).
3. A human-readable markdown summary of the same roadmap (stage → topics → links → time estimate).

This structured output is the hand-off contract for the `roadmap-html-builder` skill — do not skip the JSON block, and do not fabricate resource links; every `resourceUrl` must come from actual Microsoft Learn MCP search/fetch results.

## Notes

- All research must come from the Microsoft Learn MCP Server (`https://learn.microsoft.com/api/mcp`) connector — do not substitute generic web knowledge for resource links.
- If MCP search returns limited results for a niche technology, note this explicitly and use the best available official Microsoft Learn resources, or general Microsoft Learn search/landing pages as a fallback link.
- Keep stage count between 3 and 4 for readability unless the user asks for more granularity.
