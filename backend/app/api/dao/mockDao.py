# encoding: UTF-8
from ..model.mockModel import MockDocument, MockInterface, MockScene, MockCallLog, MockParseIssue


class MockDao:
    @staticmethod
    def create(session, item):
        session.add(item)
        session.flush()
        return item.id

    @staticmethod
    def create_all(session, items):
        session.add_all(items)
        session.flush()
        return [item.id for item in items]

    @staticmethod
    def get_by_id(session, model, item_id):
        return session.query(model).filter(model.id == item_id, model.is_delete == 0).first()

    @staticmethod
    def list_by_filters(session, model, filters, page_no=1, page_size=20, order_by=None):
        query = session.query(model).filter(*filters)
        if order_by is not None:
            query = query.order_by(order_by)
        total = query.count()
        items = query.offset((page_no - 1) * page_size).limit(page_size).all()
        return items, total

    @staticmethod
    def update_by_id(session, model, item_id, update_info):
        result = session.query(model).filter(model.id == item_id, model.is_delete == 0).update(update_info)
        session.flush()
        return result

    @staticmethod
    def list_scenes(session, interface_id, only_enabled=False):
        filters = [MockScene.interface_id == interface_id, MockScene.is_delete == 0]
        if only_enabled:
            filters.append(MockScene.status == 1)
        return session.query(MockScene).filter(*filters).order_by(MockScene.priority.desc(), MockScene.id.asc()).all()

    @staticmethod
    def find_enabled_interfaces(session, project_id, method):
        return session.query(MockInterface).filter(
            MockInterface.project_id == project_id,
            MockInterface.method == method.upper(),
            MockInterface.status == 1,
            MockInterface.is_delete == 0
        ).order_by(MockInterface.path_score.desc(), MockInterface.id.asc()).all()

    @staticmethod
    def get_scene_by_code(session, interface_id, scene_code):
        return session.query(MockScene).filter(
            MockScene.interface_id == interface_id,
            MockScene.scene_code == scene_code,
            MockScene.status == 1,
            MockScene.is_delete == 0
        ).order_by(MockScene.priority.desc(), MockScene.id.asc()).first()

    @staticmethod
    def count_interfaces_by_document(session, document_id):
        return session.query(MockInterface).filter(
            MockInterface.document_id == document_id,
            MockInterface.is_delete == 0
        ).count()
