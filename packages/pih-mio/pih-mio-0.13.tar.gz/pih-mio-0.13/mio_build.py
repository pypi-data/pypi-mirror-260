import ipih

from pih import A
from pih.tools import j
from build_tools import build
from MobileHelperService.const import SD

build(
    SD,
    requires_packages=(
        A.PTH_FCD_DIST.NAME(j((A.CT_SR.MOBILE_HELPER.standalone_name, "content"), "-")),
        A.PTH_FCD_DIST.NAME("tls"),
    ),
)
