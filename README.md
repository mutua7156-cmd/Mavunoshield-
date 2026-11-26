# MavunoShield

A Streamlit research prototype for agricultural climate-risk awareness and rainfall-index actuarial illustrations.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Start the application:

   `streamlit run app.py`

## Deploy

This project can be deployed using Streamlit Community Cloud by connecting a GitHub repository containing `app.py` and `requirements.txt`.

## Important research limitations

- County rainfall reference values are placeholders, not validated climate normals.
- The premium rate is user-assumed, not actuarially priced.
- The payout formula is a simple educational rainfall-index illustration.
- The app does not forecast weather, estimate actual crop loss, issue insurance, or guarantee payouts.
- Before academic publication, obtain reliable local rainfall and crop-loss data, cite sources, calibrate parameters, and validate basis risk.

## Suggested next research tasks

1. Select one county, crop, and growing season.
2. Obtain a documented rainfall dataset and define the reference period.
3. Compare rainfall index values with crop-yield/loss observations.
4. Estimate expected payout cost from historical seasons.
5. Add uncertainty analysis and out-of-sample validation.
