from fastapi import FastAPI, Request
import os
from fastapi import FastAPI, Header, Request, HTTPException
from typing import Annotated
from fastapi import APIRouter, Depends
import anyio
router = APIRouter()
from fastapi.responses import StreamingResponse
import aiofiles

@router.get("/download/{filename}")
async def download_file(request: Request, filename: str,
                        range: str | None = Header(default=None, description="HTTP Range header, e.g. bytes=0-1023")

                        ):
    file_path = f"/tmp/{filename}"
    file_size = os.path.getsize(file_path)

    # 解析 Range 请求头
    range_header = request.headers.get("range")
    if range_header:
        _, range_spec = range_header.split("=")
        start, end = range_spec.split("-")
        start = int(start)
        end = int(end) if end else file_size - 1
    else:
        start, end = 0, file_size - 1

    async def async_iterfile(path, start, end):
        async with aiofiles.open(path, "rb") as f:
            await f.seek(start)
            remaining = end - start + 1
            chunk_size = 1024 * 1024  # 1MB
            while remaining > 0:
                chunk = await f.read(min(chunk_size, remaining))
                if not chunk:
                    break
                yield chunk
                remaining -= len(chunk)

    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(end - start + 1),
    }

    return StreamingResponse(
        async_iterfile(file_path, start, end),
        status_code=206 if range_header else 200,
        headers=headers,
        media_type="application/octet-stream"
    )