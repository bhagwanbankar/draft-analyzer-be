import os
from sqlalchemy import select
from sqlalchemy.orm import aliased
from civis_backend_policy_analyser.config.logging_config import logger

from civis_backend_policy_analyser.models.assessment_area_summary import AssessmentAreaSummary
from civis_backend_policy_analyser.models.document_metadata import DocumentMetadata
from civis_backend_policy_analyser.models.document_summary import DocumentSummary
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.models.prompt_score import PromptScore
from civis_backend_policy_analyser.schemas.history_schema import DocumentHistorySchema, DocumentHistorySchemaOut
from civis_backend_policy_analyser.utils.constants import REPORTS_OUTPUT_DIR
from civis_backend_policy_analyser.views.base_view import BaseView



class HistoryView(BaseView):
    schema = DocumentHistorySchema

    async def get_user_history(self, user_id: str) -> DocumentHistorySchemaOut:
        logger.info(f"Fetching history for user: {user_id}")

        ds = aliased(DocumentSummary)
        dt = aliased(DocumentType)
        dm = aliased(DocumentMetadata)

        query = (
            select(
                ds.doc_summary_id,
                ds.doc_type_id,
                ds.created_on.label("summary_time"),
                ds.evaluation_status.label("evaluation_status"),
                dt.doc_type_name.label("doc_type_name"),
                dm.file_name.label("file_name")
            )
            .join(dt, ds.doc_type_id == dt.doc_type_id)
            .join(dm, ds.doc_id == dm.doc_id)
            .where(ds.created_by == user_id)
            .order_by(ds.created_on.desc())
        )

        result = await self.db_session.execute(query)
        rows = result.mappings().all()

        # build history objects
        history = []
        for row in rows:
            history.append(
                DocumentHistorySchema(
                    doc_type_id=row["doc_type_id"],
                    doc_summary_id=row["doc_summary_id"],
                    file_name=row["file_name"],
                    summary_time=row["summary_time"],
                    status=row["evaluation_status"],
                    doc_type=row["doc_type_name"]
                )
            )
        history_out = DocumentHistorySchemaOut(history=history)
        logger.info(f"User history fetched successfully: {history}")

        return history_out

    async def delete_document_history(self, doc_summary_id: int) -> None:
        logger.info(f"Deleting history for document summary ID: {doc_summary_id}")


        # Delete AssessmentAreaSummary records
        assessment_area_summaries = await self.db_session.execute(
            select(AssessmentAreaSummary).where(AssessmentAreaSummary.doc_summary_id == doc_summary_id)
        )
        for summary in assessment_area_summaries.scalars().all():
            # Delete PromptScore records
            prompt_scores = await self.db_session.execute(
                select(PromptScore).where(PromptScore.assessment_summary_id == summary.assessment_summary_id)
            )
            for score in prompt_scores.scalars().all():
                await self.db_session.delete(score)
            await self.db_session.delete(summary)

        
            
        # Delete the document summary entry
        document_summary = await self.db_session.get(DocumentSummary, doc_summary_id)
        
        if document_summary:
            report_file_name = document_summary.report_file_name
            if report_file_name:
                generated_report = os.path.join(REPORTS_OUTPUT_DIR, report_file_name)
                if os.path.exists(generated_report):
                    os.remove(generated_report)
                    logger.info(f"Deleted report file: {generated_report}")
                else:
                    logger.warning(f"Report file not found, could not delete: {generated_report}")
            else:
                logger.warning("No report file name found for document summary, skipping file deletion.")
                
            await self.db_session.delete(document_summary)
            await self.db_session.commit()
            
            logger.info(f"Document summary with ID {doc_summary_id} deleted successfully.")
        else:
            logger.warning(f"Document summary with ID {doc_summary_id} not found.")