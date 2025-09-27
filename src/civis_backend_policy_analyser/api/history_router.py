from fastapi import APIRouter
from civis_backend_policy_analyser.config.logging_config import logger

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.history_schema import DocumentHistoryDeleteOut, DocumentHistorySchemaOut, PaginatedHistoryOut
from civis_backend_policy_analyser.views.document_metadata_view import DocumentMetadataView
from civis_backend_policy_analyser.views.history_view import HistoryView


history_router = APIRouter(
    prefix='/api/history',
    tags=['history'],
    responses={404: {'description': 'No history found.'}},
)


@history_router.get('/{user_id}')
async def get_history_report(
    user_id: str, 
    db_session: DBSessionDep, 
    page: int = 1, 
    page_size: int = 10
) -> PaginatedHistoryOut:
    """
    Fetch the paginated history report for the given user_id.
    """
    try:
        history_view = HistoryView(db_session)
        history = await history_view.get_user_history(user_id, page, page_size)
        return history
    except Exception as e:
        logger.error(f"Error fetching history for user {user_id}: {e}")
        return {
            "history": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "message": f"History report for user {user_id} not available yet."
        }
    
@history_router.delete('/doc_summary/{doc_summary_id}')
async def delete_history_report(doc_summary_id: int, db_session: DBSessionDep) -> DocumentHistoryDeleteOut:
    """
    Delete the history report for the given document summary ID.
    """
    try:
        # Clean up vector store for the document if it is present
        document_service = DocumentMetadataView(db_session)
        await document_service.clean_vector_db_store(doc_summary_id)

        history_view = HistoryView(db_session)
        await history_view.delete_document_history(doc_summary_id)

        return {"message": f"History report for document {doc_summary_id} deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting history for document {doc_summary_id}: {e}")
        return {"message": f"Failed to delete history report for document {doc_summary_id}."}