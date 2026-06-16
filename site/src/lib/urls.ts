export function sitePath(path: string) {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  const normalized = path.startsWith('/') ? path : `/${path}`;
  const withBase = `${base}${normalized}` || normalized;
  if (/\.[^/]+$/.test(normalized)) return withBase;
  return withBase.endsWith('/') ? withBase : `${withBase}/`;
}
