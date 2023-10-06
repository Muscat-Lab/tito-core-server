from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, ResponseBase

router = APIRouter(prefix="/performanceContents", tags=["performanceContent"])


class PerformanceContentListRequest(ListRequestBase):
    performance_id: UUID


class PerformanceContentListResponse(ListResponseBase):
    class PerformanceContent(ResponseBase):
        id: UUID
        performance_id: UUID
        heading: str
        content: str

    performance_contents: list[PerformanceContent]


@router.get("")
async def performance_content_list_handler(
    q: PerformanceContentListRequest = Depends(),
) -> PerformanceContentListResponse:
    return PerformanceContentListResponse(
        performance_contents=[
            PerformanceContentListResponse.PerformanceContent(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                performance_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1a"),
                heading="heading1",
                content="content2",
            ),
            PerformanceContentListResponse.PerformanceContent(
                id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                performance_id=UUID("d1b9d1a0-0b1a-4e1a-9b1a-0b1a0b1a0b1b"),
                heading="heading2",
                content="content2",
            ),
        ],
        next_cursor=None,
    )
