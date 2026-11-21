# SQE Assignment (Part A) - SauceDemo UI Automation with Playwright (Python)

Automated UI tests for https://www.saucedemo.com using **Playwright for Python** and **pytest**.
Design: Page Object Model, data-driven tests (CSV), auto-waiting (no sleeps), automatic screenshot on failure.

## 1. Requirements

- Python 3.10 or newer
- Internet access (the tests run against the public demo site)

## 2. Setup (one time)

```bash
# 1. create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 2. install the libraries
pip install -r requirements.txt

# 3. download the browsers Playwright controls
playwright install chromium     # add firefox / webkit if you want them
```

Check versions for your report: `python --version`, `pip show playwright pytest pytest-html`.

## 3. Run the tests

```bash
pytest                                   # whole suite, headless Chromium, HTML report in reports/report.html
pytest --show-browser                    # watch the browser while it runs
pytest --browser-name firefox            # another browser (chromium | firefox | webkit)
pytest tests/test_login.py               # one file
pytest -k "sort"                         # tests whose name contains "sort"
python run_three_times.py                # runs the suite 3 times and prints the Task 5 table
```

Outputs:

| Output | Location |
|--------|----------|
| HTML report | `reports/report.html` (3-run mode: `reports/report_run1.html` ... `run3`) |
| Run summary table | `reports/run_summary.md` and `reports/run_summary.csv` |
| Failure screenshots | `screenshots/FAIL_<test>_<time>.png` (also embedded in the HTML report) |

## 4. Folder structure

```
SQE_Assignment_A/
|-- config.py              base URL, demo users, password
|-- conftest.py            browser/page fixtures, page-object fixtures, screenshot-on-failure hook
|-- pytest.ini             pytest settings (test folder, default HTML report)
|-- requirements.txt       libraries
|-- run_three_times.py     runs the suite 3 times and builds the results table
|-- pages/                 Page Objects (locators + actions, no assertions)
|   |-- base_page.py       shared header (cart icon and badge)
|   |-- login_page.py
|   |-- inventory_page.py
|   |-- product_page.py
|   |-- cart_page.py
|   `-- checkout_page.py
|-- tests/                 test logic only (assertions)
|   |-- test_hello_world.py   environment check
|   |-- test_login.py         scenarios 1, 2, 3, 4, 10
|   |-- test_inventory.py     scenarios 5, 11
|   |-- test_cart.py          scenarios 6, 7
|   `-- test_checkout.py      scenarios 8, 9, 12
|-- data/                  external test data
|   |-- login_data.csv        5 data sets
|   `-- checkout_data.csv     3 data sets
|-- utils/                 helpers (CSV reader, reusable checkout flow)
|-- reports/               generated reports (not committed)
|-- screenshots/           generated failure screenshots (not committed)
`-- .github/workflows/tests.yml   CI pipeline (bonus)
```

## 5. Scenario coverage

| # | Scenario | Test |
|---|----------|------|
| 1 | Valid login | `test_login_valid_standard_user_shows_products` |
| 2 | Invalid password | `test_login_invalid_password_shows_error` |
| 3 | Empty username / password | `test_login_negative_cases_data_driven` (empty_username, empty_password, both_empty) |
| 4 | Locked-out user | `test_login_negative_cases_data_driven` (locked_out_user) |
| 5 | Sorting | `test_sort_products` (4 sort options) |
| 6 | Add one / multiple items | `test_add_one_item_...`, `test_add_multiple_items_...` |
| 7 | Remove item | `test_remove_item_...`, `test_remove_last_item_hides_badge` |
| 8 | Checkout end to end | `test_checkout_end_to_end_shows_order_complete` |
| 9 | Checkout missing fields | `test_checkout_missing_field_shows_validation_message` (3 data sets) |
| 10 | Logout and back button | `test_logout_...`, `test_back_button_after_logout_...` |
| 11 | Product detail | `test_product_detail_matches_inventory_list` |
| 12 | Totals at overview | `test_checkout_overview_totals_are_correct` |

## 6. Design decisions

- **Page Object Model:** locators and actions live in `pages/`; tests only call page methods and assert.
- **Locators:** `data-test` attributes and one unique id (`#react-burger-menu-btn`). No XPath is used.
- **Waits:** Playwright auto-waits before every action, and `expect(...)` retries assertions. There is no `sleep`.
- **Independence:** every test gets a new browser context (clean cookies and storage) and logs in by itself, so tests can run in any order.
- **Data-driven:** `login_data.csv` and `checkout_data.csv` are read by `utils/data_reader.py` and fed to `pytest.mark.parametrize`.
- **Failure handling:** `conftest.py` saves a full-page screenshot when a test fails.

## 7. If a test fails because the site changed

SauceDemo is a public demo and can change. Open the page, press F12, inspect the element and update
the locator in the matching file in `pages/`. `playwright codegen https://www.saucedemo.com` also shows locators.
Write down the date you tested.

## 8. AI usage

See the AI Usage Statement in the report.
