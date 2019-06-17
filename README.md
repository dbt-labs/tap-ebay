# tap-ebay

Author: Drew Banin (drew@fishtownanalytics.com)

This is a [Singer](http://singer.io) tap that produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

It:
- Generates a catalog of available order data from the Ebay fulfillment API
- Extracts the following resources:
  - [orders](https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrders#h2-samples)

### Quick Start

1. Install

```bash
git clone git@github.com:fishtown-analytics/tap-ebay.git
cd tap-ebay
pip install .
```

2. Authentication

This tap calls the fulfillment API which requires a User access token.

In order to retrieve a User access token the service needs to:
* use a _refresh_ token (long-lived) and exchange it for an _access_ token (short-lived)

This likely requires two Ebay accounts:
* A seller account which owns the sales data,
* A developer account which is used for applications to access the sales data.

In order to create a refresh token:
* Seller account needs to grant permission to Developer account to use the API,
* Developer account needs to exchange the authorization code for a refresh token.

### Generating a refresh token

**Read [the documentation](https://developer.ebay.com/api-docs/static/oauth-authorization-code-grant.html)**

1. Obtain credentials to both Seller and Developer account.
1. Go to [eBay's Application Keys](https://developer.ebay.com/my/keys) and note `Cert ID (Client Secret)`.
1. Sign in using Developer username and password.
1. Go to the specified _authorization url_ (see below) in your browser.
1. Sign in using Seller username and password. 
1. Grant access by clicking _Agree_.
1. After being redirected, copy the value of query param `code`.
1. Execute: `./get-refresh-token.sh` providing your credentials as arguments
1. Copy `refresh_token` from the response and store it with the job configuration.

**Example authorization url**

```
https://auth.ebay.com/oauth2/authorize?client_id=<client_id>
    &response_type=code
    &redirect_uri=<redirect_uri>
    &scope=https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly
```

Note: It is critical that the scope provided in the `config.json` file matches
the scope requested from this authorization url!


3. Create the config file.

There is a template you can use at `config.json.example`, just copy it to `config.json` in the repo root and insert your credentials

4. Run the application to generate a catalog.

```bash
tap-ebay -c config.json --discover > catalog.json
```

5. Select the tables you'd like to replicate

Step 4 generates a a file called `catalog.json` that specifies all the available endpoints and fields.
You'll need to open the file and select the ones you'd like to replicate.
See the [Singer guide on Catalog Format](https://github.com/singer-io/getting-started/blob/c3de2a10e10164689ddd6f24fee7289184682c1f/BEST_PRACTICES.md#catalog-format)
for more information on how tables are selected.

6. Run it!

```bash
tap-ebay -c config.json --catalog catalog.json
```

Copyright &copy; 2019 Stitch
