export interface Paper {
  key: string;
  type: string;
  year: number;
  title: string;
  authors: string[];
  venue: string;
  venueHref?: string;
  preview?: string;
  links: { label: string; href: string }[];
  bibtex: string;
}

const readField = (body: string, name: string): string | undefined => {
  const re = new RegExp(`\\b${name}\\s*=\\s*`, "i");
  const m = body.match(re);
  if (!m) return undefined;
  const start = m.index! + m[0].length;
  const opener = body[start];
  if (opener !== "{" && opener !== '"') return undefined;
  const close = opener === "{" ? "}" : '"';
  let depth = 0;
  for (let i = start; i < body.length; i++) {
    const c = body[i];
    if (opener === "{") {
      if (c === "{") depth++;
      else if (c === "}") {
        depth--;
        if (depth === 0) return body.slice(start + 1, i).replace(/\s+/g, " ").trim();
      }
    } else {
      if (c === '"' && body[i - 1] !== "\\" && i > start) {
        return body.slice(start + 1, i).replace(/\s+/g, " ").trim();
      }
    }
  }
  return undefined;
};

const splitAuthors = (raw: string): string[] =>
  raw.split(/\s+and\s+/i).map((a) => a.trim()).filter(Boolean);

const shortenVenue = (entry: {
  type: string;
  booktitle?: string;
  journal?: string;
}): string => {
  const src = (entry.journal || entry.booktitle || "").replace(/\\&/g, "&");
  const s = src.toLowerCase();
  if (s.includes("arxiv")) return "arXiv";
  if (s.includes("acm transactions on graphics") || s.includes("siggraph asia")) {
    if (s.includes("asia")) return "SIGGRAPH Asia";
    if (s.includes("acm transactions on graphics")) return "SIGGRAPH Asia";
  }
  if (s.includes("siggraph")) return "SIGGRAPH";
  if (s.includes("pattern analysis and machine intelligence")) return "TPAMI";
  if (s.includes("visualization and computer graphics")) return "TVCG";
  if (s.includes("conference on computer vision and pattern recognition")) return "CVPR";
  if (s.includes("international conference on computer vision")) return "ICCV";
  if (s.includes("european conference on computer vision")) return "ECCV";
  if (s.includes("international conference on learning representations")) return "ICLR";
  if (s.includes("computers & graphics") || s.includes("computers and graphics")) return "Computers & Graphics";
  return src;
};

export function parseBib(source: string): Paper[] {
  const papers: Paper[] = [];
  const re = /@(\w+)\s*\{\s*([^,\s]+)\s*,/g;
  let m: RegExpExecArray | null;
  const entryStarts: { type: string; key: string; bodyStart: number; entryStart: number }[] = [];
  while ((m = re.exec(source)) !== null) {
    entryStarts.push({
      type: m[1],
      key: m[2],
      bodyStart: m.index + m[0].length,
      entryStart: m.index,
    });
  }
  for (let i = 0; i < entryStarts.length; i++) {
    const { type, key, bodyStart, entryStart } = entryStarts[i];
    let depth = 1;
    let end = bodyStart;
    for (let j = bodyStart; j < source.length; j++) {
      const c = source[j];
      if (c === "{") depth++;
      else if (c === "}") {
        depth--;
        if (depth === 0) {
          end = j;
          break;
        }
      }
    }
    const body = source.slice(bodyStart, end);
    const bibtex = source.slice(entryStart, end + 1);
    const title = readField(body, "title") || "";
    const authorRaw = readField(body, "author") || "";
    const yearStr = readField(body, "year") || "0";
    const year = parseInt(yearStr, 10) || 0;
    const journal = readField(body, "journal");
    const booktitle = readField(body, "booktitle");
    const preview = readField(body, "preview");
    const pdf = readField(body, "pdf");
    const code = readField(body, "code");
    const html = readField(body, "html");
    const demo = readField(body, "demo");
    const links: { label: string; href: string }[] = [];
    if (pdf) links.push({ label: "PDF", href: pdf });
    if (code) links.push({ label: "Code", href: code });
    if (html) links.push({ label: "Project", href: html });
    if (demo) links.push({ label: "Demo", href: demo });
    const venue = shortenVenue({ type, booktitle, journal });
    const arxivField = readField(body, "arxiv");
    let venueHref: string | undefined;
    if (arxivField) {
      venueHref = `https://arxiv.org/abs/${arxivField.trim()}`;
    } else if (venue === "arXiv") {
      const arxivId = (journal || "").match(/arXiv:\s*([\d.]+)/i)?.[1];
      if (arxivId) venueHref = `https://arxiv.org/abs/${arxivId}`;
    }
    papers.push({
      key,
      type,
      year,
      title,
      authors: splitAuthors(authorRaw),
      venue,
      venueHref,
      preview,
      links,
      bibtex,
    });
  }
  return papers;
}
