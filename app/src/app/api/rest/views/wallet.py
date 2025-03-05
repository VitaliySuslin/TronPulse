from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.sql.selectable import Select
from typing import Dict, Optional, List

from src.app.api.rest.schemas.requests.wallet import PaginationRequest, WalletInfoRequest
from src.app.api.rest.schemas.responses.wallet import (
    WalletListResponse,
    WalletInfoResponse,
    WalletResponse,
)
from src.app.db.orm.wallet import WalletRequest
from src.app.extensions.sqlalchemy import PoolConnector
from src.app.config import settings
from src.integrations.external.tron.client import TronClient
from src.app.utils.pydantic.error_response import (
    DefaultErrorResponseSchema,
    DetailDefaultErrorResponseSchema,
)


router = APIRouter(
    tags=["Tron Methods"],
    prefix=settings.API_PATH_PREF
)

@router.get(
    "/tron/wallets",
    response_model=WalletListResponse
)
async def get_wallet_requests(
    pagination: PaginationRequest = Depends(),
    session: AsyncSession = Depends(PoolConnector.get_session)
) -> WalletListResponse:
    offset: int = (pagination.page - 1) * pagination.size
    query: Select = select(WalletRequest).order_by(WalletRequest.requested_at.desc()).offset(offset).limit(pagination.size)
    count_query: Select = select(func.count()).select_from(WalletRequest)

    result: ChunkedIteratorResult = await session.execute(query)
    total: int = await session.scalar(count_query)

    items: List[WalletResponse] = [
        WalletResponse(
            id=item.id,
            address=item.address,
            bandwidth=item.bandwidth,
            energy=item.energy,
            trx_balance=item.trx_balance,
            requested_at=item.requested_at
        )
        for item in result.scalars().all()
    ]

    return WalletListResponse(
        items=items,
        total=total,
        page=pagination.page,
        size=pagination.size
    )

@router.post(
    "/tron/wallet",
    response_model=WalletInfoResponse
)
async def get_wallet_info(
    request: WalletInfoRequest,
    session: AsyncSession = Depends(PoolConnector.get_session)
) -> WalletInfoResponse:
    try:
        client: TronClient = TronClient(network=request.network)

        wallet_info: Optional[Dict] = client.get_wallet_info(request.address)

        if not wallet_info:
            raise HTTPException(
                status_code=400,
                detail=DefaultErrorResponseSchema(
                    code=1001,
                    message="Wallet not found",
                    detail=DetailDefaultErrorResponseSchema(
                        description="The requested wallet address was not found in the Tron network."
                    )
                ).model_dump()
            )

        wallet_request: WalletRequest = WalletRequest(
            address=request.address,
            bandwidth=wallet_info.get("bandwidth"),
            energy=wallet_info.get("energy"),
            trx_balance=wallet_info.get("trx_balance")
        )
        session.add(wallet_request)
        await session.commit()

        return WalletInfoResponse(
            address=request.address,
            bandwidth=wallet_info.get("bandwidth"),
            energy=wallet_info.get("energy"),
            trx_balance=wallet_info.get("trx_balance"),
            network=request.network
        )

    except HTTPException as e:
        raise HTTPException(
            status_code=400,
            detail=DefaultErrorResponseSchema(
                code=1002,
                message="Bad request",
                detail=DetailDefaultErrorResponseSchema(
                    description=str(e.detail)
                )
            ).model_dump()
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=DefaultErrorResponseSchema(
                code=1003,
                message="Internal server error",
                detail=DetailDefaultErrorResponseSchema(
                    description=str(e)
                )
            ).model_dump()
        )
