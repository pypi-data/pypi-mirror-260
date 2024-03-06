from common_utils.utils.blueprint_util import Outlining


controller: Outlining = Outlining("v2", __name__, url_prefix="/version2")


@controller.get("")
def index():
    return "version2 index"
