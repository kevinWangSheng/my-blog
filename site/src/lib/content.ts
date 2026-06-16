import { getCollection, type CollectionEntry } from 'astro:content';
import { sitePath } from './urls';

export type PublicCollection = 'projects' | 'notes' | 'logs' | 'essays' | 'links';
export type AnyEntry = CollectionEntry<PublicCollection>;

export function entrySlug(entry: { id: string }) {
  return entry.id.replace(/\.(md|mdx)$/i, '');
}

export function collectionPath(collection: PublicCollection) {
  return collection === 'links' ? sitePath('/links') : sitePath(`/${collection}`);
}

export function entryPath(collection: PublicCollection, entry: { id: string }) {
  if (collection === 'links') return sitePath('/links');
  return `${collectionPath(collection)}${entrySlug(entry)}/`;
}

export function formatDate(date: Date | string) {
  return new Intl.DateTimeFormat('en', { year: 'numeric', month: 'short', day: '2-digit' }).format(new Date(date));
}

export function byDateDesc<T extends { data: { date: Date } }>(items: T[]) {
  return [...items].sort((a, b) => +new Date(b.data.date) - +new Date(a.data.date));
}

export async function getPublicCollection<T extends PublicCollection>(collection: T) {
  const entries = await getCollection(collection, ({ data }) => data.visibility === 'public');
  return byDateDesc(entries);
}

export type RelatedEntry = {
  collection: PublicCollection;
  title: string;
  description: string;
  date: Date;
  path: string;
  reason: string;
  tags: string[];
  external?: boolean;
};

function asTags(entry: AnyEntry) {
  return Array.isArray(entry.data.tags) ? entry.data.tags : [];
}

function asRelated(entry: AnyEntry) {
  const related = (entry.data as { related?: string[] }).related;
  return Array.isArray(related) ? related : [];
}

function sameSeries(current: AnyEntry, candidate: AnyEntry) {
  const currentSeries = (current.data as { series?: string }).series;
  const candidateSeries = (candidate.data as { series?: string }).series;
  return Boolean(currentSeries && candidateSeries && currentSeries === candidateSeries);
}

function targetCollections(collection: PublicCollection): PublicCollection[] {
  if (collection === 'essays') return ['essays', 'notes', 'links'];
  if (collection === 'notes') return ['notes', 'essays', 'links'];
  if (collection === 'logs') return ['logs', 'notes', 'essays'];
  if (collection === 'projects') return ['projects', 'notes', 'essays'];
  return ['links', 'essays', 'notes'];
}

export async function getRelatedEntries(collection: PublicCollection, entry: AnyEntry, limit = 4): Promise<RelatedEntry[]> {
  const pools = await Promise.all(targetCollections(collection).map(async (target) => ({
    collection: target,
    entries: await getPublicCollection(target)
  })));
  const currentSlug = entrySlug(entry);
  const currentTags = new Set(asTags(entry));
  const currentRelated = new Set(asRelated(entry));

  const scored = pools.flatMap(({ collection: target, entries }) => entries.map((candidate) => {
    const candidateSlug = entrySlug(candidate);
    if (target === collection && candidateSlug === currentSlug) return null;

    const candidateTags = asTags(candidate);
    const sharedTags = candidateTags.filter((tag) => currentTags.has(tag));
    const linked = currentRelated.has(candidateSlug) || asRelated(candidate).includes(currentSlug);
    const series = sameSeries(entry, candidate);
    const sameCollection = target === collection;

    let score = 0;
    let reason = '';
    if (series) {
      score += 100;
      reason = 'Same series';
    }
    if (linked) {
      score += 80;
      reason ||= 'Explicitly related';
    }
    if (sharedTags.length) {
      score += sharedTags.length * 18;
      reason ||= `Shared tag: ${sharedTags[0]}`;
    }
    if (sameCollection) {
      score += 6;
      reason ||= 'Recent in this collection';
    }
    if (target === 'links' && collection === 'essays') {
      score += 10;
      reason ||= 'Source shelf';
    }
    score += Math.max(0, 5 - Math.abs(+new Date(entry.data.date) - +new Date(candidate.data.date)) / 86_400_000);
    if (score <= 0) return null;

    return {
      collection: target,
      title: candidate.data.title,
      description: candidate.data.description,
      date: candidate.data.date,
      path: target === 'links' ? (candidate.data as { url: string }).url : entryPath(target, candidate),
      reason,
      tags: candidateTags,
      external: target === 'links'
    } satisfies RelatedEntry;
  })).filter(Boolean) as RelatedEntry[];

  return scored
    .sort((a, b) => {
      const scoreA = (a.reason === 'Same series' ? 100 : 0) + (a.reason === 'Explicitly related' ? 80 : 0) + a.tags.filter((tag) => currentTags.has(tag)).length * 18 + +new Date(a.date) / 1e12;
      const scoreB = (b.reason === 'Same series' ? 100 : 0) + (b.reason === 'Explicitly related' ? 80 : 0) + b.tags.filter((tag) => currentTags.has(tag)).length * 18 + +new Date(b.date) / 1e12;
      return scoreB - scoreA;
    })
    .slice(0, limit);
}

export const collectionLabels: Record<PublicCollection, { title: string; eyebrow: string; description: string }> = {
  projects: {
    title: 'Projects',
    eyebrow: 'Capability evidence',
    description: '项目入口会保持克制:只有足够公开、质量过线、证据完整的项目才会展示。'
  },
  notes: {
    title: 'Notes',
    eyebrow: 'Working memory',
    description: '短而密的阶段性判断,保留正在形成的想法和可复用的概念。'
  },
  logs: {
    title: 'Logs',
    eyebrow: 'Process records',
    description: '阶段记录和 devlog。当前没有公开 log,后续只放对读者有价值的项目或学习过程记录。'
  },
  essays: {
    title: 'Essays',
    eyebrow: 'Long-form synthesis',
    description: '更完整的文章,把学习、实验和判断收束成可以被别人阅读的表达。'
  },
  links: {
    title: 'Links',
    eyebrow: 'Source shelf',
    description: '值得反复返回的资料、工具和参考源,附带为什么收藏它。'
  }
};
