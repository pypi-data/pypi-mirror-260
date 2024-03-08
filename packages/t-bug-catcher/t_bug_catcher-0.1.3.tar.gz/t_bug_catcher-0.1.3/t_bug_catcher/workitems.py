from .utils import logger

try:
    from RPA.Robocorp.WorkItems import WorkItems

    work_items = WorkItems()
    work_items.get_input_work_item()
    work_item = work_items.get_work_item_variables()
    variables = work_item.get("variables", dict())
except (ImportError, KeyError):
    logger.warning("Workitems unavailable. Variables will be empty.")
    variables = {}
