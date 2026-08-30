import { copyFile, mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const source = fileURLToPath(
  new URL("../../plugins/tab/assets/toolbox.svg", import.meta.url),
);
const target = fileURLToPath(
  new URL("../public/generated/toolbox.svg", import.meta.url),
);
const darkTarget = fileURLToPath(
  new URL("../public/generated/toolbox-dark.svg", import.meta.url),
);

await mkdir(dirname(target), { recursive: true });
await copyFile(source, target);

const sourceContent = await readFile(source, "utf8");
const darkContent = sourceContent.replace('fill="#f5f5f5"', 'fill="#222222"');

if (darkContent === sourceContent) {
  throw new Error("Toolbox background color was not found");
}

await writeFile(darkTarget, darkContent);
