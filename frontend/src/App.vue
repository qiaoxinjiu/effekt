<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script>
import { getRoleList, parseMenusFromRoleListResponse } from '@/api/rbacApi'

export default {
  name: 'App',
  mounted() {
    this.applyTheme()
    const authUser = JSON.parse(localStorage.getItem('authUser') || 'null')
    const userMenus = JSON.parse(localStorage.getItem('userMenus') || '[]')
    if (authUser) {
      this.$store.commit('SetCurrentUser', authUser)
      this.$store.commit('SetRole', authUser.roleIds || [])
      this.$store.commit('SetUserMenus', userMenus)
      this.loadUserMenus(authUser)
    }
  },
  methods: {
    applyTheme() {
      const theme = localStorage.getItem('uiTheme') || 'dark'
      document.body.classList.remove('theme-dark', 'theme-light')
      document.body.classList.add(theme === 'light' ? 'theme-light' : 'theme-dark')
    },
    loadUserMenus(authUser) {
      const roleId = authUser && authUser.roleIds && authUser.roleIds.length ? authUser.roleIds[0] : undefined
      if (!roleId) {
        return
      }
      getRoleList({ roleId }).then(res => {
        this.$store.commit('SetUserMenus', parseMenusFromRoleListResponse(res))
      }).catch(() => {})
    }
  }
}
</script>

<style>
html,
body {
  height: 100%;
  margin: 0;
  overflow: hidden;
  background: #070b16;
  color: #dbeafe;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", Arial, sans-serif;
}

#app{
  height: 100%;
  overflow: hidden;
}

* {
  box-sizing: border-box;
}

button,
.el-button,
.el-link,
.el-menu-item,
.el-submenu__title {
  cursor: pointer;
}

.el-card {
  border-color: rgba(148, 163, 184, 0.2);
  background: #111827;
  color: #e5e7eb;
}

.el-table,
.el-table__expanded-cell {
  background-color: #111827 !important;
  color: #e5e7eb !important;
}

.el-table th,
.el-table tr,
.el-table td {
  background-color: #111827 !important;
  color: #e5e7eb !important;
}

.el-table th,
.el-table thead,
.el-table__header-wrapper th,
.el-table__fixed-header-wrapper th {
  background: #1f2937 !important;
  color: #f8fafc !important;
  font-weight: 700;
}

.el-table .cell,
.el-table th > .cell,
.el-table__body-wrapper,
.el-table__fixed-body-wrapper {
  color: inherit !important;
}

.el-table td,
.el-table th.is-leaf {
  border-bottom-color: rgba(148, 163, 184, 0.18) !important;
}

.el-table--border,
.el-table--group,
.el-table--border td,
.el-table--border th,
.el-table__fixed-right-patch {
  border-color: rgba(148, 163, 184, 0.18) !important;
}

.el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: #162033 !important;
  color: #e5e7eb !important;
}

.el-table--enable-row-hover .el-table__body tr:hover > td,
.el-table__body tr.hover-row > td,
.el-table__body tr.hover-row.current-row > td,
.el-table__body tr.hover-row.el-table__row--striped > td,
.el-table__body tr.hover-row.el-table__row--striped.current-row > td {
  background-color: #233149 !important;
  color: #f8fafc !important;
}

.el-table__body tr.current-row > td,
.el-table__body tr.current-row:hover > td {
  background-color: rgba(56, 189, 248, 0.16) !important;
  color: #f8fafc !important;
}

.el-table__fixed,
.el-table__fixed-right,
.el-table__fixed::before,
.el-table__fixed-right::before {
  background-color: #111827 !important;
}

.el-table::before,
.el-table--group::after,
.el-table--border::after {
  background-color: rgba(148, 163, 184, 0.18) !important;
}

.el-form-item__label,
.el-checkbox,
.el-radio,
.el-dialog__body,
.el-pagination,
.el-pagination button,
.el-pagination span:not([class*=suffix]),
.el-select-dropdown__item,
.el-dropdown-menu__item {
  color: #dbeafe;
}

.el-input__inner,
.el-textarea__inner,
.el-select .el-input__inner,
.el-date-editor .el-input__inner {
  background-color: #0f172a;
  border-color: rgba(148, 163, 184, 0.28);
  color: #f8fafc;
}

.el-input__inner::placeholder,
.el-textarea__inner::placeholder {
  color: #64748b;
}

.el-input__inner:hover,
.el-textarea__inner:hover,
.el-input__inner:focus,
.el-textarea__inner:focus {
  border-color: #38bdf8;
}

.el-dialog,
.el-drawer,
.el-message-box {
  background: #111827;
  color: #e5e7eb;
  border: 1px solid rgba(148, 163, 184, 0.2);
}

.el-dialog__title,
.el-message-box__title {
  color: #f8fafc;
}

.el-dialog__header,
.el-dialog__footer,
.el-message-box__header,
.el-message-box__content {
  border-color: rgba(148, 163, 184, 0.16);
}

.el-select-dropdown,
.el-dropdown-menu,
.el-picker-panel {
  background: #111827;
  border-color: rgba(148, 163, 184, 0.22);
  color: #e5e7eb;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover,
.el-dropdown-menu__item:hover {
  background-color: #1e293b;
  color: #f8fafc;
}

.el-select-dropdown__item.selected {
  color: #38bdf8;
}

.el-pagination .btn-prev,
.el-pagination .btn-next,
.el-pager li {
  background: #111827;
  color: #dbeafe;
  border: 1px solid rgba(148, 163, 184, 0.18);
}

.el-pager li.active {
  color: #38bdf8;
  border-color: rgba(56, 189, 248, 0.5);
}

.el-tag:not(.el-tag--success):not(.el-tag--warning):not(.el-tag--danger):not(.el-tag--info) {
  border-color: rgba(56, 189, 248, 0.28);
  background: rgba(56, 189, 248, 0.12);
  color: #bae6fd;
}

.el-tag.el-tag--success {
  border-color: rgba(103, 194, 58, 0.45);
  background: rgba(103, 194, 58, 0.16);
  color: #86efac;
}

.el-tag.el-tag--warning {
  border-color: rgba(230, 162, 60, 0.45);
  background: rgba(230, 162, 60, 0.16);
  color: #fcd34d;
}

.el-tag.el-tag--danger {
  border-color: rgba(245, 108, 108, 0.45);
  background: rgba(245, 108, 108, 0.16);
  color: #fca5a5;
}

.el-tag.el-tag--info {
  border-color: rgba(148, 163, 184, 0.35);
  background: rgba(148, 163, 184, 0.14);
  color: #cbd5e1;
}

.el-card__header {
  background: #162033;
  border-bottom-color: rgba(148, 163, 184, 0.18);
  color: #f8fafc;
}

.el-tabs__item {
  color: #cbd5e1;
}

.el-tabs__item:hover,
.el-tabs__item.is-active {
  color: #38bdf8;
}

.el-tabs__nav-wrap::after {
  background-color: rgba(148, 163, 184, 0.18);
}

.el-popover,
.el-tooltip__popper.is-light {
  background: #111827;
  border-color: rgba(148, 163, 184, 0.22);
  color: #e5e7eb;
}

.el-tree,
.el-tree-node__content {
  background: transparent;
  color: #e5e7eb;
}

.el-tree-node__content:hover,
.el-tree-node:focus > .el-tree-node__content {
  background-color: #1e293b;
  color: #f8fafc;
}

.el-loading-mask {
  background-color: rgba(15, 23, 42, 0.72);
}

body.theme-light {
  background: #eef4ff;
  color: #1f2937;
}

body.theme-light .el-card {
  border-color: #dbe5f3;
  background: #ffffff;
  color: #1f2937;
  box-shadow: 0 12px 32px rgba(37, 99, 235, 0.08);
}

body.theme-light .el-table,
body.theme-light .el-table__expanded-cell {
  background-color: #ffffff !important;
  color: #1f2937 !important;
}

body.theme-light .el-table th,
body.theme-light .el-table tr,
body.theme-light .el-table td {
  background-color: #ffffff !important;
  color: #1f2937 !important;
}

body.theme-light .el-table th,
body.theme-light .el-table thead,
body.theme-light .el-table__header-wrapper th,
body.theme-light .el-table__fixed-header-wrapper th {
  background: #f1f6ff !important;
  color: #0f172a !important;
}

body.theme-light .el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: #f8fbff !important;
  color: #1f2937 !important;
}

body.theme-light .el-table--enable-row-hover .el-table__body tr:hover > td,
body.theme-light .el-table__body tr.hover-row > td,
body.theme-light .el-table__body tr.hover-row.current-row > td,
body.theme-light .el-table__body tr.hover-row.el-table__row--striped > td,
body.theme-light .el-table__body tr.hover-row.el-table__row--striped.current-row > td {
  background-color: #eaf2ff !important;
  color: #0f172a !important;
}

body.theme-light .el-table__body tr.current-row > td,
body.theme-light .el-table__body tr.current-row:hover > td {
  background-color: #dbeafe !important;
  color: #0f172a !important;
}

body.theme-light .el-table td,
body.theme-light .el-table th.is-leaf,
body.theme-light .el-table--border,
body.theme-light .el-table--group,
body.theme-light .el-table--border td,
body.theme-light .el-table--border th,
body.theme-light .el-table__fixed-right-patch {
  border-color: #e2e8f0 !important;
}

body.theme-light .el-table__fixed,
body.theme-light .el-table__fixed-right,
body.theme-light .el-table__fixed::before,
body.theme-light .el-table__fixed-right::before {
  background-color: #ffffff !important;
}

body.theme-light .el-table::before,
body.theme-light .el-table--group::after,
body.theme-light .el-table--border::after {
  background-color: #e2e8f0 !important;
}

body.theme-light .el-form-item__label,
body.theme-light .el-checkbox,
body.theme-light .el-radio,
body.theme-light .el-dialog__body,
body.theme-light .el-pagination,
body.theme-light .el-pagination button,
body.theme-light .el-pagination span:not([class*=suffix]),
body.theme-light .el-select-dropdown__item,
body.theme-light .el-dropdown-menu__item {
  color: #334155;
}

body.theme-light .el-input__inner,
body.theme-light .el-textarea__inner,
body.theme-light .el-select .el-input__inner,
body.theme-light .el-date-editor .el-input__inner {
  background-color: #ffffff;
  border-color: #d8e1ef;
  color: #0f172a;
}

body.theme-light .el-input__inner::placeholder,
body.theme-light .el-textarea__inner::placeholder {
  color: #94a3b8;
}

body.theme-light .el-dialog,
body.theme-light .el-drawer,
body.theme-light .el-message-box,
body.theme-light .el-select-dropdown,
body.theme-light .el-dropdown-menu,
body.theme-light .el-picker-panel,
body.theme-light .el-popover,
body.theme-light .el-tooltip__popper.is-light {
  background: #ffffff;
  border-color: #dbe5f3;
  color: #1f2937;
}

body.theme-light .el-dialog__title,
body.theme-light .el-message-box__title,
body.theme-light .el-card__header {
  color: #0f172a;
}

body.theme-light .el-card__header {
  background: #f8fbff;
  border-bottom-color: #e2e8f0;
}

body.theme-light .el-select-dropdown__item.hover,
body.theme-light .el-select-dropdown__item:hover,
body.theme-light .el-dropdown-menu__item:hover,
body.theme-light .el-tree-node__content:hover,
body.theme-light .el-tree-node:focus > .el-tree-node__content {
  background-color: #eaf2ff;
  color: #0f172a;
}

body.theme-light .el-pagination .btn-prev,
body.theme-light .el-pagination .btn-next,
body.theme-light .el-pager li {
  background: #ffffff;
  color: #334155;
  border-color: #e2e8f0;
}

body.theme-light .el-tabs__item {
  color: #64748b;
}

body.theme-light .el-tabs__item:hover,
body.theme-light .el-tabs__item.is-active,
body.theme-light .el-select-dropdown__item.selected,
body.theme-light .el-pager li.active {
  color: #2563eb;
}

body.theme-light .el-tabs__nav-wrap::after {
  background-color: #e2e8f0;
}

body.theme-light .el-tag:not(.el-tag--success):not(.el-tag--warning):not(.el-tag--danger):not(.el-tag--info) {
  border-color: #bfdbfe;
  background: #eff6ff;
  color: #1d4ed8;
}

body.theme-light .el-tag.el-tag--success {
  border-color: #e1f3d8;
  background: #f0f9eb;
  color: #67c23a;
}

body.theme-light .el-tag.el-tag--warning {
  border-color: #faecd8;
  background: #fdf6ec;
  color: #e6a23c;
}

body.theme-light .el-tag.el-tag--danger {
  border-color: #fde2e2;
  background: #fef0f0;
  color: #f56c6c;
}

body.theme-light .el-tag.el-tag--info {
  border-color: #e9e9eb;
  background: #f4f4f5;
  color: #909399;
}

body.theme-light .el-tree,
body.theme-light .el-tree-node__content {
  color: #334155;
}

body.theme-light .el-loading-mask {
  background-color: rgba(248, 250, 252, 0.72);
}
</style>
