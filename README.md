# DSSA Technical Assessment

Thank you for taking the time to complete this technical assessment. There is no strict time limit — we would rather see a thorough piece of work than a rushed one.

The brief is intentionally light on prescription. We are at least as interested in the decisions you make and how you justify them as we are in the final score numbers. You can structure your code, split it into modules, and lay out the project however you see fit.

**A note on AI tools:** using AI assistants (Copilot, ChatGPT, Claude, etc.) is fine — we use them too. That said, we want to see your thinking. Submissions that lean heavily on AI without clear understanding behind them will come through in the code and the QA response, and won't be accepted.

## Background

CDP scores climate and environmental disclosures from companies that respond to our questionnaire. For this assessment, we are exploring a simplified scoring approach for a new version of the questionnaire.

You have been given:

- A small dataset of company responses (`data.json`)
- A single scoring criterion (described below)

Your job is to implement the criterion against the dataset.

## The data

`data.json` contains responses from eight companies to a single question, `q_1_1`.

A company's response to `q_1_1` is made up of one or more **rows** (`r1`, `r2`, …), each representing a distinct disclosure entry. Each row has four fields:

- `c1` — free-text answer
- `c2` — a date
- `c3` — a list of numbers
- `c4` — the theme(s) the row applies to (a list containing one or both of `"Climate Change"` and `"Water"`)

`c4` is the theme selection. A row tagged with a theme is in scope for that theme's criterion, and only that theme's criterion. A row tagged with both is in scope for both.

The data was pulled directly from raw submissions and has not been cleaned. It is representative of the kind of variability you would expect in production.

### Field conventions

There are two distinct patterns for missing data you will encounter in the response objects, and they mean different things:

- A field present with a `null` value (e.g. `"c2": null`) means the company was shown the field but did not provide an answer.
- A field whose key is absent entirely means the field was not applicable to the company.

How you handle each of these in your scoring is up to you.

## The scoring criteria

Two themes are scored for `q_1_1`: **Climate Change** and **Water**.

Both criteria reference the first three statements of the lorem ipsum, separated by commas:

> *"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"*

### Climate Change

**ROUTE A)**

For rows where 'Climate Change' is selected in column 'c4' AND 'c2' is after 2023-01-01:

Second statement of the lorem ipsum present in 'c1' AND 'c3' contains more than 3 elements - 3 points

Third statement of the lorem ipsum present in 'c1' AND 'c3' contains at least one even element - 1 point

A maximum of 4/4 points is available for this route.

OR

**NON-DISCLOSURE ROUTE)**

For rows where 'Climate Change' is selected in column 'c4' AND 'c2' is on or before 2023-01-01, or 'c2' is not provided - 0/0.5 points

A maximum of 0/0.5 points is available for this route.

OR

**NOT APPLICABLE ROUTE)**

'Climate Change' NOT selected in column 'c4' in any row - 0/0 points

A maximum of 0/0 points is available for this route.

### Water

**ROUTE A)**

For rows where 'Water' is selected in column 'c4' AND 'c2' is after 2023-01-01:

First statement of the lorem ipsum present in 'c1' AND 'c3' contains at least one even element - 1 point

Third statement of the lorem ipsum present in 'c1' AND 'c3' contains more than 3 elements - 1 point

A maximum of 2/2 points is available for this route.

OR

**ROUTE B)**

For rows where 'Water' is selected in column 'c4' AND 'c2' is on or before 2023-01-01 - 1/2 points

A maximum of 1/2 points is available for this route.

OR

**NON-DISCLOSURE ROUTE)**

For rows where 'Water' is selected in column 'c4' AND 'c2' is not provided - 0/0.5 points

A maximum of 0/0.5 points is available for this route.

OR

**NOT APPLICABLE ROUTE)**

'Water' NOT selected in column 'c4' in any row - 0/0 points

A maximum of 0/0 points is available for this route.

## Your task

Implement the scoring in `main.py`. Your solution should score every company under both themes and produce **per-row scores** for the full dataset.

You need to implement both the **Climate Change** and **Water** themes.

## How to approach this

These are rough steps. Take them in any order that suits you:

1. Look at `data.json` and identify the data quality issues that need handling
2. Implement the Climate Change scoring criterion
3. Implement the Water scoring criterion
4. Score every company under both themes, producing per-row scores. Save the output as a CSV file in the local folder, formatted so a non-technical reviewer can read it and validate the scores
5. Write tests for your scoring logic
6. Write your QA response in `qa_response.md`

## QA query

Once you have your scoring working, please look at **Company 5**'s result.

A non-technical member of our QA team has flagged it during review:

> *"I looked at Company 5's response. They've submitted multiple rows, each with a date, statements and a list of numbers — to me their answers looked fine, but every row scored 0 out of 4 on Climate Change. Can you help me understand why?"*

In `qa_response.md`, write a short reply (around 250–350 words) covering:

1. Why Company 5 scored the way they did, in plain language a non-technical reader can follow
2. Whether you think the criterion is producing the right outcome here, and anything you would raise with the scoring methodology team

## Submission

Please send back everything you have written, including `qa_response.md`.

Good luck — and please reach out if anything in the brief is unclear before you start.
