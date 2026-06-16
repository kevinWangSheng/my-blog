import { defineCollection } from 'astro/content/config';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const visibility = z.enum(['public', 'draft', 'private']).default('public');
const source = z.object({
  label: z.string(),
  url: z.string().url().optional()
}).optional();

const shared = {
  title: z.string().min(1),
  description: z.string().min(1),
  date: z.coerce.date(),
  updated: z.coerce.date().optional(),
  tags: z.array(z.string()).default([]),
  source,
  visibility
};

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    ...shared,
    status: z.enum(['active', 'shipped', 'paused', 'archived']).default('active'),
    role: z.string().min(1),
    repo: z.string().url().optional(),
    demo: z.string().url().optional(),
    period: z.string().min(1)
  })
});

const notes = defineCollection({
  loader: glob({ base: './src/content/notes', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    ...shared,
    topic: z.string().min(1),
    related: z.array(z.string()).default([])
  })
});

const essays = defineCollection({
  loader: glob({ base: './src/content/essays', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    ...shared,
    canonical: z.string().url().optional(),
    series: z.string().optional()
  })
});

const links = defineCollection({
  loader: glob({ base: './src/content/links', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    ...shared,
    url: z.string().url(),
    category: z.enum(['paper', 'tool', 'essay', 'dataset', 'reference', 'feed']).default('reference'),
    feed: z.string().url().optional(),
    note: z.string().min(1)
  })
});

export const collections = { projects, notes, essays, links };
