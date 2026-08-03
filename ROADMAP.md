# HW Radar Roadmap

HW Radar is a Python tool that monitors Romanian online stores for new Hot Wheels products and sends alerts to Discord.

---

## v0.1.0 - Initial Release

- [x] Create the Python project
- [x] Add Git version control
- [x] Publish the repository on GitHub
- [x] Build the SMYK scraper
- [x] Create the Product model
- [x] Add product memory with JSON
- [x] Add Discord notifications
- [x] Add basic keyword filtering

---

## v0.2.0 - Smarter SMYK Monitoring

- [x] Add support for multiple SMYK pages
- [x] Detect pagination automatically
- [x] Create a full SMYK product baseline
- [x] Add `.env` support
- [x] Improve collectible product filtering
- [x] Ignore clothing, puzzles, school supplies, and playsets
- [x] Add `CHANGELOG.md`

---

## v0.3.0 - Cloud Automation

- [ ] Create a GitHub Actions workflow
- [ ] Run HW Radar every 30 minutes
- [ ] Add the Discord webhook as a GitHub Secret
- [ ] Preserve `seen_products.json` between workflow runs
- [ ] Test the workflow manually
- [ ] Confirm the monitor works while the PC is turned off
- [ ] Add failure logs for unsuccessful runs

---

## v0.4.0 - Noriel Support

- [ ] Investigate Noriel's 403 response
- [ ] Check for a hidden product API
- [ ] Add a Noriel scraper
- [ ] Support browser automation if required
- [ ] Merge SMYK and Noriel products into one workflow
- [ ] Add store-specific error handling
- [ ] Confirm duplicate detection works across both stores

---

## v0.5.0 - Better Notifications

- [ ] Add product images to Discord embeds
- [ ] Add cleaner prices with spaces before `Lei`
- [ ] Add the detection timestamp
- [ ] Add the store name and direct product link
- [ ] Handle Discord rate limits automatically
- [ ] Add notification summaries when many products appear

---

## v0.6.0 - Email Notifications

- [ ] Add email configuration
- [ ] Store email credentials securely
- [ ] Send alerts by email
- [ ] Include product name, price, store, and link
- [ ] Allow Discord and email alerts to be enabled separately

---

## v0.7.0 - Product Tracking

- [ ] Store complete product records instead of URLs only
- [ ] Add first-seen timestamps
- [ ] Add last-seen timestamps
- [ ] Detect price changes
- [ ] Detect price drops
- [ ] Detect products returning to stock
- [ ] Keep a simple price history

---

## v0.8.0 - Configuration Improvements

- [ ] Move watched brands and series into a dedicated configuration file
- [ ] Add favorite manufacturers
- [ ] Add ignored categories
- [ ] Add store enable and disable options
- [ ] Add configurable notification rules
- [ ] Add configurable price limits

---

## v1.0.0 - Public Release

- [ ] Monitor SMYK
- [ ] Monitor Noriel
- [ ] Run automatically every 30 minutes
- [ ] Send Discord notifications
- [ ] Send email notifications
- [ ] Track product history
- [ ] Add installation instructions
- [ ] Add configuration documentation
- [ ] Add screenshots
- [ ] Add an open-source license
- [ ] Create the first GitHub release