from fastapi.routing import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post('/tasks')   
def create_task(
    data: TaskCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    task = Task(
        name=data.name,
        description=data.description,
        due_date=data.due_date,
        status=data.status,
        priority=data.priority,
        category_id=data.category_id,
        user_id=current_user.user_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/tasks", response_model=List[TaskResponse])
def get_task_list(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return (
        db.query(Task)
        .filter(Task.user_id == current_user.user_id)
        .all()
    )


@router.get("/{task_id}", response_model=TaskResponse)
def get_one_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    task = (
        db.query(Task)
        .filter(Task.task_id == task_id, Task.user_id == current_user.user_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    task = (
        db.query(Task)
        .filter(Task.task_id == task_id, Task.user_id == current_user.user_id)
        .first()
    )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete('/tasks/{pk}')
def delete_task():
    pass
