interface DescriptionPart {
  text: string;
  href?: string;
}

interface Skill {
  name: string;
  description: DescriptionPart[];
}

export const skills: Skill[] = [
  {
    name: "clarify",
    description: [{ text: "Find out why something did not work as expected" }],
  },
  {
    name: "cmt",
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
    description: [{ text: "Stress-test an engineering decision with five independent views" }],
  },
  {
    name: "humanify",
    description: [{ text: "Make prose, Markdown and code comments clear and natural" }],
  },
];
