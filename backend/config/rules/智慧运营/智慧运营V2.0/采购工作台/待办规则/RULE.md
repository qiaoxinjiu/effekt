---
name: generated-rule
description: 1.需要进行倒序排序
2.需要在卡片上展示状态
---

# 待办规则

## Rule
1.需要进行倒序排序
2.需要在卡片上展示状态

## Applicable scene
待办列表、任务卡片、工单列表等需要按倒序展示并在卡片上呈现状态的场景；适用于 AI 根据 PRD/需求生成测试用例时识别排序规则与卡片展示约束。

## Example
输入场景：待办列表中存在多条记录，按创建时间/时间序列需要倒序展示，且每条卡片需要显示当前状态。
预期：列表默认按倒序排列；每张卡片可见状态信息，状态展示与数据源一致，刷新后仍保持正确展示。

## Test design constraints
- Generate cases that verify this rule is satisfied in normal flows.
- Generate negative and boundary cases when the rule describes validation, limits, state changes, permissions, or data constraints.
- Mark missing prerequisites as “待确认” instead of inventing behavior.

## Metadata
- Code: RULE_20260515175047622133
- Product: 智慧运营
- Project: 智慧运营V2.0
- Module: 采购工作台
- Priority: 2
- Tags: 排序, 状态展示, 待办, 列表, 卡片
