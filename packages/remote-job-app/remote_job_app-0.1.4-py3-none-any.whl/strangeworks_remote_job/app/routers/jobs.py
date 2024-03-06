"""Job API v2.0.0."""
from typing import Optional

from fastapi import APIRouter, Request

from strangeworks_remote_job.basic import cancel, fetch_result, fetch_status, submit

from .types.job import JobRequest, JobResponse, SubmitRequest


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/submit")
async def run_job(request: Request, submit_request: Optional[SubmitRequest] = None):
    """Submit a job run request."""
    ctx = request.state.params.ctx
    data = submit_request.input if submit_request else None
    remote_api = request.state.params.remote_api
    artifact_generator = request.state.params.artifact_generator
    job = submit(ctx, remote_api, data, artifact_generator)
    return JobResponse(job)


@router.post("/fetch-status")
async def list_job_details(job_request: JobRequest, request: Request):
    """Fetch job status."""
    ctx = request.state.params.ctx
    remote_api = request.state.params.remote_api
    job = fetch_status(ctx, remote_api, job_request.slug)
    return JobResponse(job)


@router.post("/fetch-result")
def get_job_results(job_request: JobRequest, request: Request):
    """Fetch Job Results."""
    ctx = request.state.params.ctx
    remote_api = request.state.params.remote_api
    artifact_generator = request.state.params.artifact_generator
    job = fetch_result(ctx, remote_api, job_request.slug, artifact_generator)
    return JobResponse(job)


@router.post("/cancel")
def cancel_job(job_request: JobRequest, request: Request):
    """Send a request to cancel a job."""
    ctx = request.state.params.ctx
    remote_api = request.state.params.remote_api
    job = cancel(ctx, remote_api, job_request.slug)
    return JobResponse(job)
