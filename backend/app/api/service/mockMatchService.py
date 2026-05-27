# encoding: UTF-8
import json
import re


class MockMatchService:
    @staticmethod
    def normalize_path(path):
        if not path:
            return '/'
        path = '/' + path.strip('/')
        return path

    @staticmethod
    def build_path_pattern(path):
        normalized = MockMatchService.normalize_path(path)
        params = []
        score = 0
        regex_parts = []
        for part in normalized.strip('/').split('/'):
            if not part:
                continue
            if (part.startswith('{') and part.endswith('}')) or part.startswith(':'):
                name = part[1:-1] if part.startswith('{') else part[1:]
                params.append(name)
                regex_parts.append('([^/]+)')
            else:
                score += 10
                regex_parts.append(re.escape(part))
        regex = '^/' + '/'.join(regex_parts) + '$'
        return regex, params, score

    @staticmethod
    def match_interface(interfaces, request_path):
        normalized = MockMatchService.normalize_path(request_path)
        for interface in interfaces:
            if MockMatchService.normalize_path(interface.path) == normalized:
                return interface, {}
        for interface in interfaces:
            if not interface.path_regex:
                continue
            matched = re.match(interface.path_regex, normalized)
            if not matched:
                continue
            try:
                params = json.loads(interface.path_params or '[]')
            except Exception:
                params = []
            return interface, dict(zip(params, matched.groups()))
        return None, {}

    @staticmethod
    def choose_scene(scenes, explicit_scene, context):
        if explicit_scene:
            for scene in scenes:
                if scene.scene_code == explicit_scene:
                    return scene
        matched_scenes = []
        for scene in scenes:
            match_rule = MockMatchService._loads(scene.match_rule, {})
            if match_rule and MockMatchService.match_rule(match_rule, context):
                matched_scenes.append(scene)
        if matched_scenes:
            return sorted(matched_scenes, key=lambda item: item.priority or 0, reverse=True)[0]
        for scene in scenes:
            if scene.scene_code == 'success':
                return scene
        return scenes[0] if scenes else None

    @staticmethod
    def match_rule(rule, context):
        for scope in ['query', 'body', 'headers', 'path']:
            expected = rule.get(scope)
            if not expected:
                continue
            actual = context.get('request', {}).get(scope, {}) or {}
            for key, condition in expected.items():
                if not MockMatchService._match_condition(actual.get(key), condition):
                    return False
        return True

    @staticmethod
    def _match_condition(actual, condition):
        if not isinstance(condition, dict) or 'op' not in condition:
            return str(actual) == str(condition)
        op = condition.get('op') or 'eq'
        expected = condition.get('value')
        if op == 'exists':
            return actual not in (None, '') if expected in (None, True, 'true', 'True') else actual in (None, '')
        if op == 'eq':
            return str(actual) == str(expected)
        if op == 'ne':
            return str(actual) != str(expected)
        if op == 'contains':
            return str(expected) in str(actual or '')
        if op == 'in':
            return str(actual) in [str(item) for item in (expected or [])]
        if op == 'regex':
            return re.search(str(expected), str(actual or '')) is not None
        try:
            actual_num = float(actual)
            expected_num = float(expected)
        except Exception:
            return False
        if op == 'gt':
            return actual_num > expected_num
        if op == 'gte':
            return actual_num >= expected_num
        if op == 'lt':
            return actual_num < expected_num
        if op == 'lte':
            return actual_num <= expected_num
        return False

    @staticmethod
    def _loads(value, default):
        if not value:
            return default
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except Exception:
            return default
