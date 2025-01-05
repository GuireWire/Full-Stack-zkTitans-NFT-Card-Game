from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network
from contracts import zkTitans


def deploy_zktitans(metadata_uri: str) -> VyperContract:
    """
    Deploy the zkTitans contract
    @param metadata_uri: Base URI for token metadata
    """
    print("Using metadata URI:", metadata_uri)

    titans: VyperContract = zkTitans.deploy(metadata_uri)
    print("Deployed zkTitans contract at:", titans.address)

    return titans


def moccasin_main() -> VyperContract:
    # Define metadata URI - same as in your deploy.ts
    metadata_uri = ""

    active_network = get_active_network()

    # Deploy contract
    titans = deploy_zktitans(metadata_uri)

    # Verify contract if on a non-local network
    if (
        active_network.has_explorer()
        and active_network.is_local_or_forked_network() is False
    ):
        print("Verifying contract on explorer...")
        result = active_network.moccasin_verify(titans)
        result.wait_for_verification()

    return titans
