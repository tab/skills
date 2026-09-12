interface DescriptionPart {
  text: string;
  href?: string;
}

interface Skill {
  name: string;
  plugin: "core" | "thinking" | "workflow";
  description: DescriptionPart[];
}

export const skills: Skill[] = [
  {
    name: "backlog",
    plugin: "workflow",
    description: [{ text: "Track deferred work and preserve closed decisions" }],
  },
  {
    name: "clarify",
    plugin: "core",
    description: [{ text: "Find out why something did not work as expected" }],
  },
  {
    name: "cmt",
    plugin: "core",
    description: [
      { text: "Draft a " },
      {
        text: "Conventional Commit",
        href: "https://www.conventionalcommits.org/en/v1.0.0/",
      },
      { text: " message from the current changes" },
    ],
  },
  {
    name: "council",
    plugin: "thinking",
    description: [{ text: "Stress-test an engineering decision with five independent views" }],
  },
  {
    name: "feature",
    plugin: "workflow",
    description: [{ text: "Plan and deliver a feature with clear scope and durable context" }],
  },
  {
    name: "feature-backfill",
    plugin: "workflow",
    description: [{ text: "Restore feature artifacts from repository history" }],
  },
  {
    name: "feature-review",
    plugin: "workflow",
    description: [{ text: "Review a feature plan, implementation or PR against its contract" }],
  },
  {
    name: "humanify",
    plugin: "core",
    description: [{ text: "Make prose, Markdown and code comments clear and natural" }],
  },
];
