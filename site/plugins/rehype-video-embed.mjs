/**
 * rehype-video-embed —— 零依赖构建期插件。
 *
 * 约定:Markdown 正文里「独占一行、只放一个 YouTube / Bilibili 链接」的段落,
 * 会被就地替换成一个懒加载 facade 播放器(先渲染封面 + 播放键,点击才注入 iframe)。
 * 行内链接、脚注里的链接、句子中间的链接都不受影响 —— 只有段落里唯一子节点是单个 <a> 才命中。
 *
 * 不引入任何依赖:自己走 hast 树,自己造节点。客户端升级逻辑在 BaseLayout 的
 * initVideoEmbeds();样式在 global.css 的 .video-embed。隐私域用 youtube-nocookie。
 */

const YT_ID = /^[A-Za-z0-9_-]{11}$/;

// 把 YouTube 的 t / start 参数(90、1m30s、2h3m1s)折算成秒。
function parseStart(raw) {
  if (!raw) return 0;
  if (/^\d+$/.test(raw)) return parseInt(raw, 10);
  const m = raw.match(/(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?/);
  if (!m) return 0;
  return (parseInt(m[1] || 0, 10) * 3600) + (parseInt(m[2] || 0, 10) * 60) + parseInt(m[3] || 0, 10);
}

// 识别 YouTube 链接 → { id, start }。不匹配返回 null。
function matchYouTube(url) {
  let u;
  try { u = new URL(url); } catch { return null; }
  const host = u.hostname.replace(/^www\.|^m\./, '');
  let id = '';
  if (host === 'youtu.be') {
    id = u.pathname.slice(1).split('/')[0];
  } else if (host === 'youtube.com' || host === 'youtube-nocookie.com') {
    if (u.pathname === '/watch') id = u.searchParams.get('v') || '';
    else {
      const m = u.pathname.match(/^\/(?:embed|shorts|live|v)\/([^/?#]+)/);
      if (m) id = m[1];
    }
  } else {
    return null;
  }
  if (!YT_ID.test(id)) return null;
  const start = parseStart(u.searchParams.get('t') || u.searchParams.get('start') || '');
  return { id, start };
}

// 识别 Bilibili 链接 → { bvid } 或 { aid }。不匹配返回 null。
function matchBilibili(url) {
  let u;
  try { u = new URL(url); } catch { return null; }
  if (!/(^|\.)bilibili\.com$/.test(u.hostname)) return null;
  const bv = u.pathname.match(/\/video\/(BV[0-9A-Za-z]+)/);
  if (bv) return { bvid: bv[1] };
  const av = u.pathname.match(/\/video\/av(\d+)/i);
  if (av) return { aid: av[1] };
  return null;
}

// 从链接构造 facade 的 hast 节点;识别不了返回 null(段落保持原样)。
function buildEmbed(href) {
  const yt = matchYouTube(href);
  if (yt) {
    const params = new URLSearchParams({ autoplay: '1', rel: '0' });
    if (yt.start) params.set('start', String(yt.start));
    const embedSrc = `https://www.youtube-nocookie.com/embed/${yt.id}?${params.toString()}`;
    const thumb = `https://i.ytimg.com/vi/${yt.id}/hqdefault.jpg`;
    return facade('youtube', 'YouTube', embedSrc, thumb);
  }
  const bili = matchBilibili(href);
  if (bili) {
    const params = new URLSearchParams({ autoplay: '1', high_quality: '1', danmaku: '0' });
    if (bili.bvid) params.set('bvid', bili.bvid); else params.set('aid', bili.aid);
    const embedSrc = `https://player.bilibili.com/player.html?${params.toString()}`;
    return facade('bilibili', 'Bilibili', embedSrc, null);
  }
  return null;
}

function el(tagName, properties, children = []) {
  return { type: 'element', tagName, properties, children };
}

function facade(provider, label, embedSrc, thumb) {
  const inner = [];
  if (thumb) {
    inner.push(el('img', {
      className: ['video-embed__thumb'],
      src: thumb,
      alt: '',
      loading: 'lazy',
      decoding: 'async',
      width: 480,
      height: 270
    }));
  }
  inner.push(el('span', { className: ['video-embed__play'], 'aria-hidden': 'true' }));
  inner.push(el('span', { className: ['video-embed__badge'] }, [{ type: 'text', value: label }]));

  const button = el('button', {
    type: 'button',
    className: ['video-embed__btn'],
    'aria-label': `播放 ${label} 视频`
  }, inner);

  return el('div', {
    className: ['video-embed'],
    'data-provider': provider,
    'data-embed-src': embedSrc,
    'data-title': `${label} 视频播放器`
  }, [button]);
}

// 段落是否「只包一个 <a>」(忽略纯空白文本)。是则返回该 <a>,否则 null。
function soleAnchor(node) {
  if (node.type !== 'element' || node.tagName !== 'p') return null;
  let anchor = null;
  for (const child of node.children) {
    if (child.type === 'text' && child.value.trim() === '') continue;
    if (child.type === 'element' && child.tagName === 'a' && !anchor) { anchor = child; continue; }
    return null; // 出现第二个有意义节点 → 不是独占一行的裸链接
  }
  return anchor;
}

export default function rehypeVideoEmbed() {
  return (tree) => {
    const walk = (parent) => {
      if (!parent.children) return;
      for (let i = 0; i < parent.children.length; i++) {
        const child = parent.children[i];
        const anchor = soleAnchor(child);
        if (anchor) {
          const href = anchor.properties && anchor.properties.href;
          const embed = typeof href === 'string' ? buildEmbed(href) : null;
          if (embed) { parent.children[i] = embed; continue; }
        }
        walk(child);
      }
    };
    walk(tree);
  };
}
