import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from db.application_dal import ApplicationDAL
from dependencies import get_application_dal

from serializers.message_serializer import MessageSerializer

router = APIRouter()


@router.post("/messages")
async def send_message(
    content: str,
    sender_id: uuid.UUID,
    receiver_id: uuid.UUID,
    application_dal: ApplicationDAL = Depends(get_application_dal),
):
    try:
        message = await application_dal.create_message(
            content=content, sender_id=sender_id, receiver_id=receiver_id
        )
        message_dict = message.__dict__

        if "forwarded_to_id" not in message_dict:
            forwarded_to_id = None
        if "reply_id" not in message_dict:
            reply_id = None

        message = MessageSerializer(
            **message_dict, forwarded_to_id=forwarded_to_id, reply_id=reply_id
        ).model_dump()

        message["id"] = str(message["id"])
        message["sender_id"] = str(message["sender_id"])
        message["receiver_id"] = str(message["receiver_id"])
        message["forwarded_to_id"] = (
            str(message["forwarded_to_id"])
            if message["forwarded_to_id"] is not None
            else None
        )
        message["reply_id"] = (
            str(message["reply_id"]) if message["reply_id"] is not None else None
        )

        return JSONResponse(status_code=201, content=message)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/messages", response_model=list[MessageSerializer])
async def list_messages(application_dal: ApplicationDAL = Depends(get_application_dal)):
    messages = await application_dal.get_all_messages()

    response_dict = [message.__dict__ for message in messages]

    response = [MessageSerializer(**message) for message in response_dict]

    return response


@router.get("/messages/{message_id}", response_model=MessageSerializer)
async def get_message(
    message_id: uuid.UUID,
    application_dal: ApplicationDAL = Depends(get_application_dal),
):
    message = await application_dal.get_message(message_id=message_id)

    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return message


@router.put("/messages/{message_id}/reply", response_model=MessageSerializer)
async def reply_message(
    message_id: uuid.UUID,
    content: str,
    application_dal: ApplicationDAL = Depends(get_application_dal),
):
    try:
        message_to_reply = await application_dal.get_message(message_id=message_id)

        sender_id = message_to_reply.receiver_id
        receiver_id = message_to_reply.sender_id

        reply = await application_dal.create_message(
            content=content, sender_id=sender_id, receiver_id=receiver_id
        )

        await application_dal.update_message(message_id=message_id, reply_id=reply.id)

        return JSONResponse(status_code=200, content="Reply sent")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/messages/{message_id}/forward", response_model=MessageSerializer)
async def forward_message(
    message_id: uuid.UUID,
    forwarded_to_id: uuid.UUID,
    application_dal: ApplicationDAL = Depends(get_application_dal),
):
    try:
        await application_dal.update_message(
            message_id=message_id, forwarded_to_id=forwarded_to_id
        )
        return JSONResponse(status_code=200, content="Message forwarded")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: uuid.UUID,
    application_dal: ApplicationDAL = Depends(get_application_dal),
):
    try:
        await application_dal.delete_message(message_id=message_id)

        return JSONResponse(status_code=204, content="Message deleted")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
