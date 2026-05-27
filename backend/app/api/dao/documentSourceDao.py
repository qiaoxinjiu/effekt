# encoding: UTF-8
from sqlalchemy import func

from ..model.documentSourceModel import DocumentSource


class DocumentSourceDao:
    
    @staticmethod
    def create(session, document_source):
        session.add(document_source)
        session.flush()
        return document_source.id
    
    @staticmethod
    def get_by_id(session, document_id):
        return session.query(DocumentSource).filter(
            DocumentSource.id == document_id,
            DocumentSource.is_delete == 0
        ).first()
    
    @staticmethod
    def get_by_source(session, source):
        return session.query(DocumentSource).filter(
            DocumentSource.source == source,
            DocumentSource.is_delete == 0
        ).first()
    
    @staticmethod
    def list_by_filters(session, filters, page_no=1, page_size=20, order_by=None):
        query = session.query(DocumentSource).filter(*filters)
        
        if order_by is not None:
            query = query.order_by(order_by)
        
        total = query.count()
        
        items = query.offset((page_no - 1) * page_size).limit(page_size).all()
        
        return items, total
    
    @staticmethod
    def update_by_id(session, document_id, update_info):
        result = session.query(DocumentSource).filter(
            DocumentSource.id == document_id,
            DocumentSource.is_delete == 0
        ).update(update_info)
        session.flush()
        return result
    
    @staticmethod
    def delete_by_id(session, document_id):
        return session.query(DocumentSource).filter(
            DocumentSource.id == document_id,
            DocumentSource.is_delete == 0
        ).update({'is_delete': 1})
    
    @staticmethod
    def get_latest_version(session, product_id, project_id, source):
        return session.query(DocumentSource).filter(
            DocumentSource.product_id == product_id,
            DocumentSource.project_id == project_id,
            DocumentSource.source == source,
            DocumentSource.is_delete == 0
        ).order_by(DocumentSource.version.desc()).first()
    
    @staticmethod
    def get_max_version(session, product_id, project_id, source):
        result = session.query(func.max(DocumentSource.version)).filter(
            DocumentSource.product_id == product_id,
            DocumentSource.project_id == project_id,
            DocumentSource.source == source,
            DocumentSource.is_delete == 0
        ).scalar()
        return result if result else 0
