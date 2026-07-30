from fastapi import Depends

from src.repositories.data_collection.source_registry import (
    SourceRegistryRepository,
)
from src.services.data_collection.source_registry import (
    SourceRegistryService,
)
from src.repositories.data_collection.source_document import (
    SourceDocumentRepository,
)
from src.services.data_collection.source_document import (
    SourceDocumentService,
)
from src.repositories.data_collection.document_version import (
    DocumentVersionRepository,
)
from src.services.data_collection.document_version import (
    DocumentVersionService,
)
from src.repositories.data_collection.collection_log import (
    CollectionLogRepository,
)
from src.services.data_collection.collection_log import (
    CollectionLogService,
)
from src.repositories.data_collection.document_validation import (
    DocumentValidationRepository,
)
from src.services.data_collection.document_validation import (
    DocumentValidationService,
)
from src.repositories.data_collection.ai_extraction import (
    AIExtractionRepository,
)
from src.services.data_collection.ai_extraction import (
    AIExtractionService,
)

def get_source_registry_repository() -> SourceRegistryRepository:
    """Return Source Registry repository."""
    return SourceRegistryRepository()


def get_source_registry_service(
    repository: SourceRegistryRepository = Depends(
        get_source_registry_repository,
    ),
) -> SourceRegistryService:
    """Return Source Registry service."""
    return SourceRegistryService(repository)

def get_source_document_repository() -> SourceDocumentRepository:
    return SourceDocumentRepository()


def get_source_document_service(
    repository: SourceDocumentRepository = Depends(
        get_source_document_repository,
    ),
) -> SourceDocumentService:
    return SourceDocumentService(repository)

def get_document_version_repository() -> DocumentVersionRepository:
    return DocumentVersionRepository()


def get_document_version_service(
    repository: DocumentVersionRepository = Depends(
        get_document_version_repository,
    ),
) -> DocumentVersionService:
    return DocumentVersionService(repository)

def get_collection_log_repository() -> CollectionLogRepository:
    return CollectionLogRepository()


def get_collection_log_service(
    repository: CollectionLogRepository = Depends(
        get_collection_log_repository,
    ),
) -> CollectionLogService:
    return CollectionLogService(repository)

def get_document_validation_repository() -> (
    DocumentValidationRepository
):
    return DocumentValidationRepository()


def get_document_validation_service(
    repository: DocumentValidationRepository = Depends(
        get_document_validation_repository,
    ),
) -> DocumentValidationService:
    return DocumentValidationService(repository)

def get_ai_extraction_repository() -> (
    AIExtractionRepository
):
    return AIExtractionRepository()


def get_ai_extraction_service(
    repository: AIExtractionRepository = Depends(
        get_ai_extraction_repository,
    ),
) -> AIExtractionService:
    return AIExtractionService(repository)