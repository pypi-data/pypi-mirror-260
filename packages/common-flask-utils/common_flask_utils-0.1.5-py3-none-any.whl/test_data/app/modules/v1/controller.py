from common_utils.utils.blueprint_util import Outlining


controller: Outlining = Outlining("v1", __name__)


@controller.get("")
def index():
    return "v1 index"
