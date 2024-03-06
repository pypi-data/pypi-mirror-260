import logging
from common_utils.utils.blueprint_util import Outlining


controller: Outlining = Outlining("base_modules", __name__, url_prefix="/base")
logger: logging.Logger = logging.getLogger(controller.name)


@controller.get("")
def index():
    logger.info("module index")
    return "module index"
