import celery.states as states
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .worker import celery

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/add/{param1}/{param2}")
async def add(param1: int, param2: int):
    task = celery.send_task('regular_task', args=[param1, param2])
    return JSONResponse({
        "task_id": task.id,
        "task_status": task.status
    })
    
@app.get("/heavy")
async def heavy():
    task = celery.send_task('heavy_task')
    return JSONResponse({
        "task_id": task.id,
        "task_status": task.status
    })

@app.get("/call_error")
async def call_error():
    task = celery.send_task('task_net_error')
    return JSONResponse({
        "task_id": task.id,
        "task_status": task.status
    })
    
@app.get("/call_error_retry")
async def call_error_retry():
    task = celery.send_task('task_retry_error')
    return JSONResponse({
        "task_id": task.id,
        "task_status": task.status
    })

@app.get("/call_custom_error")
async def call_custom_error():
    task = celery.send_task('task_custom_net_error')
    return JSONResponse({
        "task_id": task.id,
        "task_status": task.status
    })

@app.get("/check/{task_id}")
async def check_task(task_id: str):
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return {
            "message": res.state,
        }
    else:
        return {
            "message": str(res.result),
        }
        
@app.get("/make_dead_letter/{number}")
async def make_dead_letter(number: int):
    task = celery.send_task('task_dead_if_failed', args=[number])
    # task.revoke(terminate=True)
    return JSONResponse({
        "task_id": task.id,
        "task_status": task.status
    })        


@app.get("/health_check")
async def health_check():
    return {"Status": "Ok"}