import requests
import time
import json

UNISWAP_SUBGRAPH_ARB = 'https://api.thegraph.com/subgraphs/name/revert-finance/uniswap-v3-arbitrum'
UNISWAP_SUBGRAPH_MAINNET = 'https://api.thegraph.com/subgraphs/name/revert-finance/uniswap-v3-mainnet'


def query_fee_gt(fee_tier_gt: int, endpoint: str):
    variables = {"fee_tier_gt": fee_tier_gt}
    query = """
           query Pools ($fee_tier_gt: Int){
  pools(where:{feeTier_gt: $fee_tier_gt},orderBy:"feeTier",orderDirection:asc, first:1){
    feeTier 
  }
}
        """
    response = requests.post(endpoint, json={'query': query, 'variables': variables})
    while response.status_code != 200:
        time.sleep(1)
        response = requests.post(endpoint, json={'query': query, 'variables': variables})
    try:
        fee_tier = json.loads(response.text)['data']['pools'][0]['feeTier']
        return fee_tier
    except:
        return None


def query_all_fee_tier(endpoint: str):
    tiers = []
    fee_tier_gt = 0
    while True:
        try:
            tier = query_fee_gt(fee_tier_gt, endpoint)
            if tier is None:
                return tiers
            tiers.append(tier)
            fee_tier_gt = int(tier)
        except:
            break


def main():
    tiers = query_all_fee_tier(UNISWAP_SUBGRAPH_MAINNET)
    print(*tiers)


if __name__ == '__main__':
    main()
