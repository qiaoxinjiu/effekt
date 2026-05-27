/** 复现步骤中的截图：存 Markdown 图片语法，详情页安全渲染 */

/** Markdown 图片：允许 ] 与 ( 之间有空格，与部分编辑器行为一致 */
export function getBugStepImageMarkdownRegex() {
  return /!\[[^\]]*\]\s*\(\s*((?:https?:\/\/|\/)[^)\s]+)\s*\)/gi
}

/** 新建 / 无复现步骤数据时，富文本编辑器内的默认骨架 */
export const BUG_STEPS_DEFAULT_HTML =
  '<p>复现步骤：</p>' +
  '<p><br></p>' +
  '<p><br></p>' +
  '<p>实际结果：</p>' +
  '<p><br></p>' +
  '<p><br></p>' +
  '<p>预期结果：</p>' +
  '<p><br></p>'

export function escapeHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** 用于 HTML 属性（如 img src） */
export function escapeHtmlAttr(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
}

/**
 * 上传文件路径中的反斜杠统一为 /
 * @param {string} url
 */
export function normalizeUploadPathSlashes(url) {
  return String(url || '').trim().replace(/\\/g, '/')
}

/**
 * 静态资源（Bug 上传图）访问根，不含末尾 /
 * - 开发环境默认 http://localhost:8881（与后端文件服务常见端口一致）
 * - 可在 index.html 里设置 window.__BUG_UPLOAD_ORIGIN__ 覆盖
 * - 打包时可配置 VUE_APP_BUG_UPLOAD_ORIGIN（需在 webpack DefinePlugin 中注入）
 */
export function getBugUploadStaticOrigin() {
  if (typeof window !== 'undefined' && window.__BUG_UPLOAD_ORIGIN__) {
    return String(window.__BUG_UPLOAD_ORIGIN__).replace(/\/$/, '')
  }
  try {
    if (typeof process !== 'undefined' && process.env && process.env.VUE_APP_BUG_UPLOAD_ORIGIN) {
      return String(process.env.VUE_APP_BUG_UPLOAD_ORIGIN).replace(/\/$/, '')
    }
  } catch (e) { /* ignore */ }
  try {
    if (typeof process !== 'undefined' && process.env && process.env.NODE_ENV === 'development') {
      return 'http://localhost:8881'
    }
  } catch (e2) { /* ignore */ }
  return ''
}

/**
 * 浏览器实际加载图片用的地址：/uploads/... 在开发环境走 8881 端口
 * 存库仍可为接口返回的完整 URL，仅展示/预览时改写
 */
export function rewriteBugImageUrlForAccess(url) {
  const u = normalizeUploadPathSlashes(url)
  if (!u) return ''
  const staticOrigin = getBugUploadStaticOrigin()
  let path = ''
  if (/^https?:\/\//i.test(u)) {
    const dbl = u.indexOf('//')
    const pathStart = u.indexOf('/', dbl >= 0 ? dbl + 2 : 0)
    path = pathStart >= 0 ? u.slice(pathStart) : '/'
  } else if (u.startsWith('/')) {
    path = u
  } else {
    return u
  }
  path = normalizeUploadPathSlashes(path)
  if (staticOrigin && path.indexOf('/uploads/') === 0) {
    return staticOrigin + path
  }
  if (/^https?:\/\//i.test(u)) return u
  return resolveUploadPublicUrl(path)
}

/** 相对路径补全为当前站点 origin（无专用静态域时） */
export function resolveUploadPublicUrl(url) {
  const u = String(url || '').trim()
  if (!u) return ''
  if (/^https?:\/\//i.test(u)) return u
  if (u.startsWith('//')) return `${window.location.protocol}${u}`
  if (u.startsWith('/')) return `${window.location.origin}${u}`
  return u
}

/**
 * 解析 POST /bug/upload 成功响应（与接口一致：{ code, message, data: { url } }）
 */
export function parseBugUploadFileUrl(res) {
  if (!res) return ''
  const inner = res.data
  if (inner && typeof inner === 'object' && inner.url != null && inner.url !== '') {
    return String(inner.url).trim()
  }
  if (typeof inner === 'string' && (inner.startsWith('http') || inner.startsWith('/'))) {
    return inner.trim()
  }
  if (typeof res === 'string' && (res.startsWith('http') || res.startsWith('/'))) {
    return res.trim()
  }
  if (res.url != null && res.url !== '') {
    return String(res.url).trim()
  }
  const legacy =
    (inner && inner.fileUrl) ||
    (inner && inner.file_url) ||
    (inner && inner.path) ||
    (inner && typeof inner.data === 'object' && inner.data && inner.data.url) ||
    ''
  return legacy ? String(legacy).trim() : ''
}

/**
 * 将步骤文本转为可展示的 HTML（仅把 Markdown 图片转为 img，其余转义）
 */
export function formatBugStepsToHtml(raw) {
  const s = String(raw || '')
  const re = getBugStepImageMarkdownRegex()
  let out = ''
  let last = 0
  let m
  re.lastIndex = 0
  while ((m = re.exec(s)) !== null) {
    out += escapeHtml(s.slice(last, m.index)).replace(/\n/g, '<br>')
    const rawUrl = normalizeUploadPathSlashes(m[1])
    const displaySrc = rewriteBugImageUrlForAccess(rawUrl)
    if (displaySrc && (/^https?:\/\//i.test(displaySrc) || displaySrc.startsWith('/'))) {
      out += `<img class="bug-step-img" src="${escapeHtmlAttr(displaySrc)}" alt="截图" />`
    } else {
      out += escapeHtml(m[0])
    }
    last = m.index + m[0].length
  }
  out += escapeHtml(s.slice(last)).replace(/\n/g, '<br>')
  return out
}

/** 判断是否为富文本 HTML（与旧版纯文本 / Markdown 区分） */
export function isStepsLikelyHtml(s) {
  return /<\s*(p|div|br|img|span|ul|ol|li|h[1-6]|table|strong|em)\b/i.test(String(s || '').trim())
}

/** 将 HTML 中 img 的 src 改写为可访问地址（开发环境 /uploads → 8881） */
export function rewriteImgSrcsInHtml(html) {
  return String(html || '').replace(/(<img\b[^>]*\bsrc\s*=\s*)(["'])([^"']*)\2/gi, function (_m, pre, q, src) {
    const fixed = rewriteBugImageUrlForAccess(normalizeUploadPathSlashes(src))
    return pre + q + escapeHtmlAttr(fixed) + q
  })
}

/**
 * 旧数据（纯文本 / Markdown 图片）转为 wangEditor 可用的 HTML
 */
export function legacyStepsToEditorHtml(raw) {
  const s = String(raw || '')
  if (!s.trim()) return BUG_STEPS_DEFAULT_HTML
  if (isStepsLikelyHtml(s)) return rewriteImgSrcsInHtml(s)
  const re = getBugStepImageMarkdownRegex()
  let out = ''
  let last = 0
  let m
  re.lastIndex = 0
  while ((m = re.exec(s)) !== null) {
    const text = s.slice(last, m.index)
    if (text) {
      out += '<p>' + escapeHtml(text).replace(/\n/g, '<br/>') + '</p>'
    }
    const src = rewriteBugImageUrlForAccess(normalizeUploadPathSlashes(m[1]))
    out += '<p><img src="' + escapeHtmlAttr(src) + '" style="max-width:100%;"/></p>'
    last = m.index + m[0].length
  }
  const tail = s.slice(last)
  if (tail) {
    out += '<p>' + escapeHtml(tail).replace(/\n/g, '<br/>') + '</p>'
  }
  return out || BUG_STEPS_DEFAULT_HTML
}
