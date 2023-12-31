from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.request import ListRequestBase, ListResponseBase, RequestBase, ResponseBase
from src.auth.jwt_handler import get_current_user
from src.models.model import Performer
from src.service.performer import PerformerService

router = APIRouter(prefix="/performers", tags=["performer"])


class PerformerListRequest(ListRequestBase):
    pass


class PerformerListResponse(ListResponseBase):
    class Performer(ResponseBase):
        id: UUID
        name: str

    performers: list[Performer]


@router.get("")
async def performer_list_handler(
    q: PerformerListRequest = Depends(),
    performer_service: PerformerService = Depends(),
) -> PerformerListResponse:
    performers = await performer_service.get_performer_list(
        limit=q.limit,
        cursor=q.cursor,
    )
    return PerformerListResponse(
        performers=[
            PerformerListResponse.Performer.model_validate(
                performer, from_attributes=True
            )
            for performer in performers
        ],
        next_cursor=(performers[-1].created_at if len(performers) >= q.limit else None),
    )


class PerformerCreateRequest(RequestBase):
    name: str

    @property
    def model(self) -> Performer:
        return Performer.create(
            name=self.name,
        )


class PerformerCreateResponse(ResponseBase):
    id: UUID
    name: str


@router.post("")
async def performer_create_handler(
    q: PerformerCreateRequest,
    performer_service: PerformerService = Depends(),
) -> PerformerCreateResponse:
    performer = await performer_service.save_performer(
        q.model,
    )

    return PerformerCreateResponse.model_validate(performer, from_attributes=True)


class PerformerLikeResponse(ResponseBase):
    pass


@router.post("/{performerId}/like")
async def performer_like_handler(
    performerId: UUID,
    performer_service: PerformerService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> PerformerLikeResponse:
    await performer_service.like_performer(
        performer_id=performerId,
        user_id=user_id,
    )

    return PerformerLikeResponse()


class PerformerUnlikeResponse(ResponseBase):
    pass


@router.delete("/{performerId}/like")
async def performer_unlike_handler(
    performerId: UUID,
    performer_service: PerformerService = Depends(),
    user_id: UUID = Depends(get_current_user),
) -> PerformerUnlikeResponse:
    await performer_service.unlike_performer(
        performer_id=performerId,
        user_id=user_id,
    )

    return PerformerUnlikeResponse()
