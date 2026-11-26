MavunoShield V2.0

Actuarial modelling for rainfall-index agricultural climate-risk research


This is the Version 2.0 release of the MavunoShield student research prototype, with Kitui County, Kenya as the initial pilot geography.


What's new in V2.0


Clear V2.0 branding in the application.

Historical rainfall CSV upload and descriptive analysis.

A preliminary historical-burn-cost pricing illustration from uploaded seasonal observations.

Scenario explorer for contract payout sensitivity.

Expanded documentation of data quality, basis risk and model limitations.

Reviewer checklist for CUK and actuarial expert feedback.


Run locally


Install Python 3.10 or newer.

Open a terminal in this folder.

Run pip install -r requirements.txt.

Run streamlit run app.py.

Open the local address shown by Streamlit.


Update your existing Streamlit deployment


Download and extract this V2.0 ZIP.

Open your existing GitHub repository named MavunoShield.

Replace the old app.py, requirements.txt, README.md, and supporting documentation with the files from this package.

Commit the changes to the main branch.

Streamlit Community Cloud should redeploy automatically. Check the app logs if deployment fails.


Do not create a second repository unless you specifically want a separate test deployment.


Historical rainfall CSV format

Required columns:



year: observation year

rainfall_mm: seasonal or annual rainfall total in millimetres


Optional columns: season, location, source.


Use one consistent location and season definition for a given analysis. Document the source, extraction date, spatial resolution, aggregation and missing-data treatment. The supplied rainfall_template.csv is a format example only; its zero values are placeholders and must NOT be treated as observed rainfall.


Important research limitations

The farm assessment premium rate is user-entered and illustrative. The historical-burn-cost output is a preliminary average simulated payout, not a complete commercial tariff. The project does not include verified Kitui rainfall or crop-loss observations. A rainfall index can have basis risk because index payouts may differ from actual farm losses.


MavunoShield is not an insurer, does not issue policies, and must not be used to collect premiums or promise payouts. Empirical and commercial claims require validation and expert/regulatory review.

