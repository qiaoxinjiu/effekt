<template>
  <div class="bug-steps-rich-wrap">
    <div ref="editorHost" class="bug-steps-rich-host"></div>
  </div>
</template>

<script>
// 使用已打包的 min，避免 babel-loader 读 wangeditor 内 .babelrc 导致构建失败
import E from 'wangeditor/dist/wangEditor.min.js'
import { uploadBugStepImage } from '@/api/bugApi'
import {
  parseBugUploadFileUrl,
  normalizeUploadPathSlashes,
  rewriteBugImageUrlForAccess
} from '@/utils/bugStepsFormat'

const EMPTY_HTML = '<p><br></p>'

function normalizeHtmlForCompare(html) {
  const h = (html || '').trim()
  if (!h || h === EMPTY_HTML || h === '<p><br/></p>') return ''
  return h
}

export default {
  name: 'BugStepsRichEditor',
  props: {
    value: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
      default: '请输入复现步骤，工具栏可插入图片，支持粘贴截图'
    },
    height: {
      type: Number,
      default: 360
    }
  },
  data() {
    return {
      editor: null,
      syncing: false,
      _pasteImgHostEl: null,
      _pasteImgHandlerBound: null
    }
  },
  watch: {
    value(val) {
      this.syncFromParent(val)
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initEditor()
    })
  },
  beforeDestroy() {
    this.teardownPasteImageUpload()
    if (this.editor) {
      try {
        this.editor.destroy()
      } catch (e) { /* ignore */ }
      this.editor = null
    }
  },
  methods: {
    syncFromParent(val) {
      if (!this.editor) return
      const cur = normalizeHtmlForCompare(this.editor.txt.html())
      const next = normalizeHtmlForCompare(val)
      if (cur === next) return
      this.syncing = true
      this.editor.txt.html(next ? val : EMPTY_HTML)
      this.$nextTick(() => {
        this.syncing = false
      })
    },
    initEditor() {
      if (!this.$refs.editorHost || this.editor) return
      const EditorCtor = E && E.default ? E.default : E
      const editor = new EditorCtor(this.$refs.editorHost)
      // 必须低于 Element UI 下拉面板的 z-index（约 2000+），否则模块等 el-select 会被富文本盖住
      editor.config.zIndex = 500
      editor.config.placeholder = this.placeholder
      editor.config.height = this.height
      if (editor.config.menus && editor.config.menus.indexOf('video') !== -1) {
        editor.config.menus = editor.config.menus.filter(function (m) {
          return m !== 'video'
        })
      }
      const self = this
      editor.config.customUploadImg = function (resultFiles, insertImgFn) {
        if (!resultFiles || !resultFiles.length) return
        resultFiles.reduce(function (chain, file) {
          return chain.then(function () {
            return uploadBugStepImage(file).then(function (res) {
              const raw = normalizeUploadPathSlashes(parseBugUploadFileUrl(res))
              if (!raw) {
                self.$message.error('上传成功但未返回图片地址')
                return
              }
              const url = rewriteBugImageUrlForAccess(raw)
              insertImgFn(url)
            })
          })
        }, Promise.resolve()).catch(function () {
          self.$message.error('图片上传失败')
        })
      }
      editor.config.onchange = function (html) {
        if (self.syncing) return
        const h = html || ''
        if (normalizeHtmlForCompare(h) === '') {
          self.$emit('input', '')
        } else {
          self.$emit('input', h)
        }
      }
      editor.create()
      this.editor = editor
      const initial = this.value && this.value.trim() ? this.value : EMPTY_HTML
      editor.txt.html(initial)
      this.bindPasteImageUpload(editor)
    },
    teardownPasteImageUpload() {
      if (this._pasteImgHostEl && this._pasteImgHandlerBound) {
        this._pasteImgHostEl.removeEventListener('paste', this._pasteImgHandlerBound, true)
      }
      this._pasteImgHostEl = null
      this._pasteImgHandlerBound = null
    },
    /** 粘贴截图走 /bug/upload，与工具栏插入图片一致 */
    bindPasteImageUpload(editor) {
      this.teardownPasteImageUpload()
      const el = editor.$textElem && editor.$textElem[0]
      if (!el) return
      const self = this
      this._pasteImgHostEl = el
      this._pasteImgHandlerBound = function (e) {
        const cd = e.clipboardData
        if (!cd) return
        let file = null
        if (cd.items && cd.items.length) {
          for (let i = 0; i < cd.items.length; i++) {
            const it = cd.items[i]
            if (it.kind === 'file' && it.type && it.type.indexOf('image/') === 0) {
              file = it.getAsFile()
              if (file) break
            }
          }
        }
        if (!file && cd.files && cd.files.length) {
          for (let i = 0; i < cd.files.length; i++) {
            const f = cd.files[i]
            if (f && f.type && f.type.indexOf('image/') === 0) {
              file = f
              break
            }
          }
        }
        if (!file) return
        e.preventDefault()
        e.stopPropagation()
        uploadBugStepImage(file)
          .then(function (res) {
            const raw = normalizeUploadPathSlashes(parseBugUploadFileUrl(res))
            if (!raw) {
              self.$message.error('上传成功但未返回图片地址')
              return
            }
            const url = rewriteBugImageUrlForAccess(raw)
            const imgHtml = '<img src="' + url + '" style="max-width:100%;"/>'
            let inserted = false
            if (editor.cmd && typeof editor.cmd.do === 'function') {
              try {
                editor.cmd.do('insertHTML', imgHtml)
                inserted = true
              } catch (e1) {
                try {
                  editor.cmd.do('insertHtml', imgHtml)
                  inserted = true
                } catch (e2) { /* ignore */ }
              }
            }
            if (!inserted) self.$message.error('插入图片失败')
          })
          .catch(function () {
            self.$message.error('图片上传失败')
          })
      }
      el.addEventListener('paste', this._pasteImgHandlerBound, true)
    }
  }
}
</script>

<style scoped>
.bug-steps-rich-wrap {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  background: #fff;
  overflow: hidden;
  position: relative;
  z-index: 0;
}
.bug-steps-rich-host {
  text-align: left;
}
</style>
