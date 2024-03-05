from digitalhub_core import (
    delete_artifact,
    delete_function,
    delete_project,
    delete_run,
    delete_secret,
    delete_service,
    delete_task,
    delete_workflow,
    get_artifact,
    get_function,
    get_run,
    get_secret,
    get_service,
    get_task,
    get_workflow,
    import_artifact,
    import_function,
    import_run,
    import_secret,
    import_service,
    import_task,
    import_workflow,
    new_artifact,
    new_function,
    new_run,
    new_secret,
    new_service,
    new_task,
    new_workflow,
    set_dhub_env,
    set_store,
    update_artifact,
    update_function,
    update_project,
    update_run,
    update_secret,
    update_service,
    update_task,
    update_workflow,
)

_PROJECT_IMPORTED = False

if not _PROJECT_IMPORTED:
    try:
        from digitalhub_ml import (
            delete_model,
            get_model,
            get_or_create_project,
            get_project,
            import_model,
            import_project,
            new_model,
            new_project,
            update_model,
        )

        _PROJECT_IMPORTED = True
    except ImportError:
        ...

if not _PROJECT_IMPORTED:
    try:
        from digitalhub_data import (
            delete_dataitem,
            get_dataitem,
            get_or_create_project,
            get_project,
            import_dataitem,
            import_project,
            new_dataitem,
            new_project,
            update_dataitem,
        )

        _PROJECT_IMPORTED = True
    except ImportError:
        ...

if not _PROJECT_IMPORTED:
    from digitalhub_core import get_or_create_project, get_project, import_project, new_project
