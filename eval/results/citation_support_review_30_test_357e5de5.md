# Citation Support Review (30 Sampled Non-Abstained Answers, test_357e5de5)

Mark whether each cited chunk supports its paired claim. Not auto-scored.

## 1. `financebench_id_01275` (Best Buy)
- **Question:** Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Best Buy in FY2023?
- **Predicted Answer:**

> Based on the cash flow figures in the context:
> 
> - Operating activities provided $1,824 [10].
> - Investing activities used $962 [10].
> - Financing activities used $1,806 [10].
> 
> Operating activities brought in the most cash flow (and were the only category providing positive cash) for Best Buy in FY2023 [10].

### Pair 1.1 ([10] BESTBUY_2023_10K FY2023 p.28)
- **Claim:** Operating activities provided $1,824 [10].
- **Cited Chunk Text:**
```text
Operating activities $  1,824   $  3,252   $  4,927  
Investing activities   (962)    (1,372)    (788) 
Financing activities   (1,806)    (4,297)    (876) 
Effect of exchange rate changes on cash   (8)    (3)    7  
Increase (decrease) in cash, cash equivalents and restricted cash $  (952)   $  (2,420)   $  3,270
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 1.2 ([10] BESTBUY_2023_10K FY2023 p.28)
- **Claim:** Investing activities used $962 [10].
- **Cited Chunk Text:**
```text
Operating activities $  1,824   $  3,252   $  4,927  
Investing activities   (962)    (1,372)    (788) 
Financing activities   (1,806)    (4,297)    (876) 
Effect of exchange rate changes on cash   (8)    (3)    7  
Increase (decrease) in cash, cash equivalents and restricted cash $  (952)   $  (2,420)   $  3,270
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 1.3 ([10] BESTBUY_2023_10K FY2023 p.28)
- **Claim:** Financing activities used $1,806 [10].
- **Cited Chunk Text:**
```text
Operating activities $  1,824   $  3,252   $  4,927  
Investing activities   (962)    (1,372)    (788) 
Financing activities   (1,806)    (4,297)    (876) 
Effect of exchange rate changes on cash   (8)    (3)    7  
Increase (decrease) in cash, cash equivalents and restricted cash $  (952)   $  (2,420)   $  3,270
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 1.4 ([10] BESTBUY_2023_10K FY2023 p.28)
- **Claim:** Operating activities brought in the most cash flow (and were the only category providing positive cash) for Best Buy in FY2023 [10].
- **Cited Chunk Text:**
```text
Operating activities $  1,824   $  3,252   $  4,927  
Investing activities   (962)    (1,372)    (788) 
Financing activities   (1,806)    (4,297)    (876) 
Effect of exchange rate changes on cash   (8)    (3)    7  
Increase (decrease) in cash, cash equivalents and restricted cash $  (952)   $  (2,420)   $  3,270
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 2. `financebench_id_00070` (American Water Works)
- **Question:** Does American Water Works have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- **Predicted Answer:**

> Based on the FY2022 data in the provided excerpts, American Water Works has **negative working capital**.
> 
> Using the Consolidated Balance Sheets [1]:
> - **Total current liabilities** at December 31, 2022: **$2,811 million**
> - The excerpts do **not** explicitly state total current assets for 2022, so a precise working capital figure cannot be computed from the provided context alone. However, comparing total current liabilities of $2,811 million [1] against the largest identifiable current asset components is not possible because current assets are not itemized in the excerpt.
> 
> What can be stated directly: total current liabilities were $2,811 million at December 31, 2022, up from $2,141 million at December 31, 2021 [1]. The excerpt does not include a total current assets line, so the exact working capital amount is not in the excerpts.
> 
> Regarding relevance: the filing describes the business as capital intensive, with capital investments expected to exceed cash flows from operations over the next few years, funded through long-term debt and equity plus remaining HOS sale proceeds [5]. It also notes the Company addresses cash timing differences primarily through short-term liquidity funding mechanisms [7]. However, the excerpts do **not** explicitly state that working capital is not a useful or relevant metric for this company, so that characterization cannot be confirmed from the provided context.

### Pair 2.1 (NO CITATION)
- **Claim:** Based on the FY2022 data in the provided excerpts, American Water Works has **negative working capital**.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.2 ([1] AMERICANWATERWORKS_2022_10K FY2022 p.81)
- **Claim:** Using the Consolidated Balance Sheets [1]:
- **Cited Chunk Text:**
```text
Table of Contents
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Balance Sheets
(In millions, except share and per share data)
December 31, 2022 December 31, 2021
CAPITALIZATION AND LIABILITIES
Capitalization:   
Common stock ($0.01 par value; 500,000,000 shares authorized; 187,200,539 and 186,880,413 shares
issued, respectively) $ 2 $ 2 
Paid-in-capital 6,824 6,781 
Retained earnings 1,267 925 
Accumulated other comprehensive loss (23) (45)
Treasury stock, at cost (5,342,477 and 5,269,324 shares, respectively) (377) (365)
Total common shareholders' equity 7,693 7,298 
Long-term debt 10,926 10,341 
Redeemable preferred stock at redemption value 3 3 
Total long-term debt 10,929 10,344 
Total capitalization 18,622 17,642 
Current liabilities:   
Short-term debt 1,175 584 
Current portion of long-term debt 281 57 
Accounts payable 254 235 
Accrued liabilities 706 701 
Accrued taxes 49 176 
Accrued interest 91 88 
Liabilities related to assets held for sale — 83 
Other 255 217 
Total current liabilities 2,811 2,141 
Regulatory and other long-term liabilities:   
Advances for construction 316 284 
Deferred income taxes and investment tax credits 2,437 2,421 
Regulatory liabilities 1,590 1,600 
Operating lease liabilities 70 80 
Accrued pension expense 235 285 
Other 202 180 
Total regulatory and other long-term liabilities 4,850 4,850 
Contributions in aid of construction 1,504 1,442 
Commitments and contingencies (See Note 16)
Total capitalization and liabilities $ 27,787 $ 26,075 
The accompanying notes are an integral part of these Consolidated Financial Statements. 
80
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.3 (NO CITATION)
- **Claim:** **Total current liabilities** at December 31, 2022: **$2,811 million**
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.4 (NO CITATION)
- **Claim:** The excerpts do **not** explicitly state total current assets for 2022, so a precise working capital figure cannot be computed from the provided context alone.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.5 ([1] AMERICANWATERWORKS_2022_10K FY2022 p.81)
- **Claim:** However, comparing total current liabilities of $2,811 million [1] against the largest identifiable current asset components is not possible because current assets are not itemized in the excerpt.
- **Cited Chunk Text:**
```text
Table of Contents
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Balance Sheets
(In millions, except share and per share data)
December 31, 2022 December 31, 2021
CAPITALIZATION AND LIABILITIES
Capitalization:   
Common stock ($0.01 par value; 500,000,000 shares authorized; 187,200,539 and 186,880,413 shares
issued, respectively) $ 2 $ 2 
Paid-in-capital 6,824 6,781 
Retained earnings 1,267 925 
Accumulated other comprehensive loss (23) (45)
Treasury stock, at cost (5,342,477 and 5,269,324 shares, respectively) (377) (365)
Total common shareholders' equity 7,693 7,298 
Long-term debt 10,926 10,341 
Redeemable preferred stock at redemption value 3 3 
Total long-term debt 10,929 10,344 
Total capitalization 18,622 17,642 
Current liabilities:   
Short-term debt 1,175 584 
Current portion of long-term debt 281 57 
Accounts payable 254 235 
Accrued liabilities 706 701 
Accrued taxes 49 176 
Accrued interest 91 88 
Liabilities related to assets held for sale — 83 
Other 255 217 
Total current liabilities 2,811 2,141 
Regulatory and other long-term liabilities:   
Advances for construction 316 284 
Deferred income taxes and investment tax credits 2,437 2,421 
Regulatory liabilities 1,590 1,600 
Operating lease liabilities 70 80 
Accrued pension expense 235 285 
Other 202 180 
Total regulatory and other long-term liabilities 4,850 4,850 
Contributions in aid of construction 1,504 1,442 
Commitments and contingencies (See Note 16)
Total capitalization and liabilities $ 27,787 $ 26,075 
The accompanying notes are an integral part of these Consolidated Financial Statements. 
80
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.6 ([1] AMERICANWATERWORKS_2022_10K FY2022 p.81)
- **Claim:** What can be stated directly: total current liabilities were $2,811 million at December 31, 2022, up from $2,141 million at December 31, 2021 [1].
- **Cited Chunk Text:**
```text
Table of Contents
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Balance Sheets
(In millions, except share and per share data)
December 31, 2022 December 31, 2021
CAPITALIZATION AND LIABILITIES
Capitalization:   
Common stock ($0.01 par value; 500,000,000 shares authorized; 187,200,539 and 186,880,413 shares
issued, respectively) $ 2 $ 2 
Paid-in-capital 6,824 6,781 
Retained earnings 1,267 925 
Accumulated other comprehensive loss (23) (45)
Treasury stock, at cost (5,342,477 and 5,269,324 shares, respectively) (377) (365)
Total common shareholders' equity 7,693 7,298 
Long-term debt 10,926 10,341 
Redeemable preferred stock at redemption value 3 3 
Total long-term debt 10,929 10,344 
Total capitalization 18,622 17,642 
Current liabilities:   
Short-term debt 1,175 584 
Current portion of long-term debt 281 57 
Accounts payable 254 235 
Accrued liabilities 706 701 
Accrued taxes 49 176 
Accrued interest 91 88 
Liabilities related to assets held for sale — 83 
Other 255 217 
Total current liabilities 2,811 2,141 
Regulatory and other long-term liabilities:   
Advances for construction 316 284 
Deferred income taxes and investment tax credits 2,437 2,421 
Regulatory liabilities 1,590 1,600 
Operating lease liabilities 70 80 
Accrued pension expense 235 285 
Other 202 180 
Total regulatory and other long-term liabilities 4,850 4,850 
Contributions in aid of construction 1,504 1,442 
Commitments and contingencies (See Note 16)
Total capitalization and liabilities $ 27,787 $ 26,075 
The accompanying notes are an integral part of these Consolidated Financial Statements. 
80
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.7 (NO CITATION)
- **Claim:** The excerpt does not include a total current assets line, so the exact working capital amount is not in the excerpts.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.8 ([5] AMERICANWATERWORKS_2022_10K FY2022 p.63)
- **Claim:** Regarding relevance: the filing describes the business as capital intensive, with capital investments expected to exceed cash flows from operations over the next few years, funded through long-term debt and equity plus remaining HOS sale proceeds [5].
- **Cited Chunk Text:**
```text
the extent available, cash flows from operations. Since the Company expects its capital investments over the next few years to be greater than its cash flows
from operating activities, the Company currently plans to fund the excess of its capital investments over its cash flows from operating activities for the next
five years through a combination of long-term debt and equity in addition to the remaining proceeds from the sale of HOS. The remaining proceeds from the
sale of HOS include receipt of a seller promissory note, plus interest, and a contingent cash payment payable upon satisfaction of certain conditions on or
before December 31, 2023. If necessary, the Company may delay certain capital investments or other funding requirements or pursue financing from other
sources to preserve liquidity. In this event, the Company believes it can rely upon cash flows from operations to meet its obligations and fund its minimum
required capital investments for an extended period of time.
The Company regularly evaluates and monitors its cash requirements for capital investments, acquisitions, operations, commitments, debt maturities,
interest and dividends. The Company’s business is capital intensive, with a majority of this capital funded by cash flows from operations. The Company also
obtains funds from external sources, primarily in the debt markets and through short-term commercial paper borrowings, and may also access the equity capital
markets as needed or desired to support capital funding requirements. In order to meet short-term liquidity needs, American Water Capital Corp. (“AWCC”),
the wholly owned finance subsidiary of parent company, issues commercial paper that is supported by its revolving credit facility. The Company’s access to
external financing on reasonable terms may depend on, as appropriate, any or all of the following: current business conditions, including that of the utility and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.9 ([7] AMERICANWATERWORKS_2022_10K FY2022 p.64)
- **Claim:** It also notes the Company addresses cash timing differences primarily through short-term liquidity funding mechanisms [7].
- **Cited Chunk Text:**
```text
acquisitions and construction projects, as well as cash needs, which can fluctuate significantly due to the seasonality of the business and other factors. The
Company addresses cash timing differences primarily through its short-term liquidity funding mechanisms.
Presented in the table below is a summary of the major items affecting the Company’s cash flows from operating activities:
 For the Years Ended December 31,
(In millions) 2022 2021 2020
Net income $ 820 $ 1,263 $ 709 
Add (less):    
Depreciation and amortization 649 636 604 
Deferred income taxes and amortization of investment tax credits (c) 80 230 207 
Other non-cash activities (a) (16) (27) — 
Changes in working capital (b) (355) 126 (55)
Pension and non-pension postretirement benefit contributions (51) (40) (39)
(Gain) or loss on sale of businesses (19) (747) — 
Net cash provided by operating activities $ 1,108 $ 1,441 $ 1,426 
(a) Includes provision for losses on accounts receivable, pension and non-pension postretirement benefits and other non-cash, net. Details of each component can be found on the Consolidated
Statements of Cash Flows.
(b) Changes in working capital include changes to receivables and unbilled revenues, income tax receivable, accounts payable and accrued liabilities, accrued taxes and other current assets and
liabilities, net.
(c) The decrease in the 2022 deferred tax activity is primarily due to the settlement of the deferred tax liability related to New York American Water, sold in January 2022.
63
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 2.10 (NO CITATION)
- **Claim:** However, the excerpts do **not** explicitly state that working capital is not a useful or relevant metric for this company, so that characterization cannot be confirmed from the provided context.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 3. `financebench_id_03531` (Nike)
- **Question:** According to the details clearly outlined within the balance sheet, how much total current assets did Nike have at the end of FY2019? Answer in USD millions.
- **Predicted Answer:**

> Nike's total current assets at the end of FY2019 were $16,525 million [1].

### Pair 3.1 ([1] NIKE_2019_10K FY2019 p.53)
- **Claim:** Nike's total current assets at the end of FY2019 were $16,525 million [1].
- **Cited Chunk Text:**
```text
Table of Contents
NIKE, INC.
CONSOLIDATED BALANCE SHEETS
 
MAY 31, (Dollars in millions)
2019 2018 ASSETS
  Current assets:
  Cash and equivalents
$ 4,466 $ 4,249 Short-term investments
197 996 Accounts receivable, net
4,272 3,498 Inventories
5,622 5,261 Prepaid expenses and other current assets
1,968 1,130 Total current assets
16,525 15,134 Property, plant and equipment, net
4,744 4,454 Identifiable intangible assets, net
283 285 Goodwill
154 154 Deferred income taxes and other assets
2,011 2,509 TOTAL ASSETS
$ 23,717 $ 22,536 LIABILITIES AND SHAREHOLDERS' EQUITY
  Current liabilities:
  Current portion of long-term debt
$ 6 $ 6 Notes payable
9 336 Accounts payable
2,612 2,279 Accrued liabilities
5,010 3,269 Income taxes payable
229 150 Total current liabilities
7,866 6,040 Long-term debt
3,464 3,468 Deferred income taxes and other liabilities
3,347 3,216 Commitments and contingencies (Note 18)
Redeemable preferred stock
— — Shareholders' equity:
  Common stock at stated value:
  Class A convertible — 315 and 329 shares outstanding
— — Class B — 1,253 and 1,272 shares outstanding
3 3 Capital in excess of stated value
7,163 6,384 Accumulated other comprehensive income (loss)
231 (92 ) Retained earnings
1,643 3,517 Total shareholders' equity
9,040 9,812 TOTAL LIABILITIES AND SHAREHOLDERS' EQUITY
$ 23,717 $ 22,536 The accompanying Notes to the Consolidated Financial Statements are an integral part of this statement.
52 
NIKE, INC.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 4. `financebench_id_01487` (Johnson & Johnson)
- **Question:** Did JnJ's net earnings as a percent of sales increase in Q2 of FY2023 compared to Q2 of FY2022?
- **Predicted Answer:**

> Yes. Net earnings as a percent of sales was 20.1% in Q2 2023 versus 20.0% in Q2 2022 [10].

### Pair 4.1 ([10] JOHNSON_JOHNSON_2023Q2_EARNINGS FY2023 p.9)
- **Claim:** Net earnings as a percent of sales was 20.1% in Q2 2023 versus 20.0% in Q2 2022 [10].
- **Cited Chunk Text:**
```text
Sales to customers 25,530$      100.0      24,020$     100.0      6.3
Cost of products sold 8,212          32.2         7,919         33.0         3.7
Gross Profit 17,318        67.8         16,101       67.0         7.6
Selling, marketing and administrative expenses 6,665          26.1         6,226         25.9         7.1
Research and development expense 3,829          15.0         3,703         15.4         3.4
Interest (income) expense, net (23)              (0.1)         (26)             (0.1)          
Other (income) expense, net* (60)              (0.2)         273            1.1            
Restructuring 145             0.5           85              0.4            
Earnings before provision for taxes on income 6,762          26.5         5,840         24.3         15.8
Provision for taxes on income 1,618          6.4           1,026         4.3           57.7
Net earnings 5,144$        20.1         4,814$       20.0         6.9
Net earnings per share (Diluted) 1.96$          1.80$         8.9
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 5. `financebench_id_00995` (AMD)
- **Question:** What are the major products and services that AMD sells as of FY22?
- **Predicted Answer:**

> Based on the provided filing excerpts, AMD sells the following major products and services:
> 
> - Server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and Adaptive System-on-Chip (SoC) products for data centers [3]
> - CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers [3]
> - Discrete GPUs, and semi-custom SoC products and development services [3]
> - Embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products [3]
> - From time to time, it may also sell or license portions of its intellectual property (IP) portfolio [3]
> 
> Additional product detail from the excerpts:
> - Client processors marketed under brands including AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series, for desktop and notebook personal computers [1]
> - Consumer graphics under AMD Radeon graphics, and AMD Embedded Radeon graphics for the embedded graphics market [1]
> - Professional graphics under AMD Radeon PRO graphics [1]
> - Data center graphics under Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers [1]
> - Chipsets sold under AMD trademarks [1]
> - Server microprocessors under the AMD EPYC brand [1]
> - Low-power versions of AMD Athlon, as well as AMD Geode, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded processor solutions [1]
> - FPGA product brands: Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 (list continues in excerpt) [1]
> - Chipsets including X570, B550 and A520 for socket AM4 [4]; WRX80 chipsets for HEDT and Workstation segments [5]; B450 and A320 chipsets for the AM4 desktop platform [10]
> - FPGA-related products including high-volume and low-cost FPGAs, ASICs and ASSPs, CPLDs, DSP devices, products with embedded processors, products with embedded multi-gigabit transceivers, discrete general-purpose GPUs targeting data center and automotive applications, and other new or emerging programmable logic products [6]

### Pair 5.1 (NO CITATION)
- **Claim:** Based on the provided filing excerpts, AMD sells the following major products and services:
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.2 ([3] AMD_2022_10K FY2022 p.3)
- **Claim:** Server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and Adaptive System-on-Chip (SoC) products for data centers [3]
- **Cited Chunk Text:**
```text
We are a global semiconductor company primarily offering:
• server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and
Adaptive System-on-Chip (SoC) products for data centers;
• CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers;
• discrete GPUs, and semi-custom SoC products and development services; and
• embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products.
From time to time, we may also sell or license portions of our intellectual property (IP) portfolio.
1
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.3 ([3] AMD_2022_10K FY2022 p.3)
- **Claim:** CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers [3]
- **Cited Chunk Text:**
```text
We are a global semiconductor company primarily offering:
• server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and
Adaptive System-on-Chip (SoC) products for data centers;
• CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers;
• discrete GPUs, and semi-custom SoC products and development services; and
• embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products.
From time to time, we may also sell or license portions of our intellectual property (IP) portfolio.
1
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.4 ([3] AMD_2022_10K FY2022 p.3)
- **Claim:** Discrete GPUs, and semi-custom SoC products and development services [3]
- **Cited Chunk Text:**
```text
We are a global semiconductor company primarily offering:
• server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and
Adaptive System-on-Chip (SoC) products for data centers;
• CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers;
• discrete GPUs, and semi-custom SoC products and development services; and
• embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products.
From time to time, we may also sell or license portions of our intellectual property (IP) portfolio.
1
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.5 ([3] AMD_2022_10K FY2022 p.3)
- **Claim:** Embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products [3]
- **Cited Chunk Text:**
```text
We are a global semiconductor company primarily offering:
• server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and
Adaptive System-on-Chip (SoC) products for data centers;
• CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers;
• discrete GPUs, and semi-custom SoC products and development services; and
• embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products.
From time to time, we may also sell or license portions of our intellectual property (IP) portfolio.
1
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.6 ([3] AMD_2022_10K FY2022 p.3)
- **Claim:** From time to time, it may also sell or license portions of its intellectual property (IP) portfolio [3]
- **Cited Chunk Text:**
```text
We are a global semiconductor company primarily offering:
• server microprocessors (CPUs) and graphics processing units (GPUs), data processing units (DPUs), Field Programmable Gate Arrays (FPGAs), and
Adaptive System-on-Chip (SoC) products for data centers;
• CPUs, accelerated processing units (APUs) that integrate CPUs and GPUs, and chipsets for desktop and notebook personal computers;
• discrete GPUs, and semi-custom SoC products and development services; and
• embedded CPUs, GPUs, APUs, FPGAs, and Adaptive SoC products.
From time to time, we may also sell or license portions of our intellectual property (IP) portfolio.
1
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.7 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Client processors marketed under brands including AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series, for desktop and notebook personal computers [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.8 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Consumer graphics under AMD Radeon graphics, and AMD Embedded Radeon graphics for the embedded graphics market [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.9 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Professional graphics under AMD Radeon PRO graphics [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.10 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Data center graphics under Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.11 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Chipsets sold under AMD trademarks [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.12 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Server microprocessors under the AMD EPYC brand [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.13 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** Low-power versions of AMD Athlon, as well as AMD Geode, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded processor solutions [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.14 ([1] AMD_2022_10K FY2022 p.10)
- **Claim:** FPGA product brands: Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 (list continues in excerpt) [1]
- **Cited Chunk Text:**
```text
Table of Contents
We generally warrant that our products sold to our customers will conform to our approved specifications and be free from defects in material and workmanship
under normal use and conditions for one year. We offer up to three-year limited warranties for certain product types, and sometimes provide other warranty
periods based on negotiated terms with certain customers.
We market and sell our latest products under the AMD trademark. Our client processors include: AMD Ryzen, AMD Ryzen PRO, Ryzen Threadripper, Ryzen
Threadripper PRO, AMD Athlon, AMD Athlon PRO, and AMD PRO A-Series. These products service desktop and notebook personal computers.
Our product brand for the consumer graphics market is AMD Radeon graphics, and AMD Embedded Radeon graphics is our product brand for the embedded
graphics market.
Our product brand for professional graphics products are AMD Radeon PRO graphics.
Our product brands for data center graphics are Radeon Instinct, Radeon PRO V-series, and AMD Instinct accelerators for servers. We also market and sell our
chipsets under AMD trademarks.
Our product brand for server microprocessors is AMD EPYC processors.
We also sell low-power versions of our AMD Athlon, as well as AMD Geode™, AMD Ryzen, AMD EPYC, AMD R-Series and G-Series processors as embedded
processor solutions.
Our FPGA product brands are Virtex-6, Virtex-7, Virtex UltraScale+, Kintex-7, Kintex UltraScale, Kintex UltraScale+, Artix-7, Artix UltraScale+, Spartan-6 and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.15 ([4] AMD_2022_10K FY2022 p.7)
- **Claim:** Chipsets including X570, B550 and A520 for socket AM4 [4]; WRX80 chipsets for HEDT and Workstation segments [5]; B450 and A320 chipsets for the AM4 desktop platform [10]
- **Cited Chunk Text:**
```text
processors and prior, we offer the X570, B550 and A520 chipsets for socket AM4 for 3  Gen AMD Ryzen desktop processors and 5000 processors. In addition,
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.16 ([5] AMD_2022_10K FY2022 p.7)
- **Claim:** Chipsets including X570, B550 and A520 for socket AM4 [4]; WRX80 chipsets for HEDT and Workstation segments [5]; B450 and A320 chipsets for the AM4 desktop platform [10]
- **Cited Chunk Text:**
```text
affordable mainstream platforms segments. In the High-End Desktop (HEDT) and Workstation segments, we offer the WRX80 chipsets to support the 3  Gen
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.17 ([10] AMD_2022_10K FY2022 p.7)
- **Claim:** Chipsets including X570, B550 and A520 for socket AM4 [4]; WRX80 chipsets for HEDT and Workstation segments [5]; B450 and A320 chipsets for the AM4 desktop platform [10]
- **Cited Chunk Text:**
```text
we continue to offer the B450 and A320 chipsets that are combined with AMD Ryzen processors for the AM4 desktop platform for the performance and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 5.18 ([6] AMD_2022_10K FY2022 p.12)
- **Claim:** FPGA-related products including high-volume and low-cost FPGAs, ASICs and ASSPs, CPLDs, DSP devices, products with embedded processors, products with embedded multi-gigabit transceivers, discrete general-purpose GPUs targeting data center and automotive applications, and other new or emerging programmable logic products [6]
- **Cited Chunk Text:**
```text
• high-volume and low-cost FPGAs as programmable replacements for ASICs and ASSPs;
• ASICs and ASSPs with incremental amounts of embedded programmable logic;
• high-speed, low-density complex programmable logic devices (CPLDs);
• high-performance digital signal processing (DSP) devices;
• products with embedded processors;
• products with embedded multi-gigabit transceivers;
• discrete general-purpose GPUs targeting data center and automotive applications; and
• other new or emerging programmable logic products.
Research and Development
We focus our research and development (R&D) activities on designing and developing products. Our main area of focus is on delivering the next generation of
processors (CPU and GPU), FPGAs and Adaptive SoCs, accelerators (adaptive, graphics and DPU), System on Modules (SOMs) and SmartNICs and
associated software. We focus on designing new ICs with improved performance and performance-per-watt in advanced semiconductor manufacturing
processes, the design of logic and interface IP, advanced packaging technologies, and heterogeneous integration technologies. We also focus on software as
part of the development of our products, including design automation tools for hardware, embedded software, optimized software tools and libraries that extend
the reach of our platforms to software and AI developers. Through our R&D efforts, we were able to introduce a number of new products and enhance our IP
core offerings and software.
We also work with industry leaders on process technology, design tools, intellectual property, software and other industry consortia to conduct early-stage
research and development. We are also actively contributing to numerous industry open-source software initiatives across a broad range of technologies. We
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 6. `financebench_id_00839` (Foot Locker)
- **Question:** Does Foot Locker's new CEO have previous CEO experience in a similar company to Footlocker?
- **Predicted Answer:**

> Yes. Mary N. Dillon, the new CEO effective September 1, 2022, previously served as Executive Chair and CEO of Ulta Beauty, Inc., a beauty retailer [2][7]. She served as CEO of Ulta from July 2013 through June 2021 and as Executive Chair from June 2021 through June 2022 [7]. She also previously served as President and CEO of United States Cellular Corporation from 2010 through 2013 [7]. The excerpts describe Ulta as a consumer-driven, omni-channel retailer, but do not explicitly state that it is a "similar company" to Foot Locker; that characterization is not in the excerpts.

### Pair 6.1 ([2] FOOTLOCKER_2022_8K_dated_2022-08-19 FY2022 p.28)
- **Claim:** Dillon, the new CEO effective September 1, 2022, previously served as Executive Chair and CEO of Ulta Beauty, Inc., a beauty retailer [2][7].
- **Cited Chunk Text:**
```text
Exhibit 99.1
 
 
 
N E W S  R E L E A S E
 
 
Investor Contact: Media Contact:
Robert Higginbotham Cara Tocci
Vice President, Investor Relations Vice President, Corporate Communications
robert.higginbotham@footlocker.com                                                                                cara.tocci@footlocker.com
(212) 720-4600 (914) 582-0304
 
 
RICHARD A. JOHNSON TO RETIRE AS CHAIRMAN AND CEO;
MARY N. DILLON APPOINTED AS CEO, EFFECTIVE SEPTEMBER 1, 2022
 
Dona D. Young to Become Non-Executive Chair, Effective February 1, 2023
Transition Reflects Thorough Succession Planning Process and Strong Governance
 
 
NEW YORK, August 19, 2022 – Foot Locker, Inc. (NYSE: FL) (“Foot Locker” or “the Company”), the New York-based specialty athletic retailer, today
announced that, as part of a planned succession process, Richard A. Johnson will retire as President and Chief Executive Officer, effective September 1,
2022. Mary N. Dillon, former Executive Chair and CEO of Ulta Beauty, Inc., has been appointed President and Chief Executive Officer and a member of
the Foot Locker Board, also effective September 1, 2022.
 
Johnson will continue as Executive Chairman of the Board through January 31, 2023, and will step down from the Board at that time, subsequently
remaining with the Company as a Senior Advisor to the Chief Executive Officer until early April 2023 to facilitate a smooth transition. The Company’s
Board has determined that the Chair and Chief Executive Officer roles will be separated, also effective September 1, 2022, and the Company’s Lead
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 6.2 ([7] FOOTLOCKER_2022_8K_dated_2022-08-19 FY2022 p.1)
- **Claim:** Dillon, the new CEO effective September 1, 2022, previously served as Executive Chair and CEO of Ulta Beauty, Inc., a beauty retailer [2][7].
- **Cited Chunk Text:**
```text
Item 5.02. Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory
Arrangements of Certain Officers.
 
On August 19, 2022, Foot Locker, Inc. (the “Company”), issued a press release announcing that, as part of a planned succession process, Richard
A. Johnson will step down as President and Chief Executive Officer of the Company, effective September 1, 2022. Mary N. Dillon, 61, former Executive
Chair and Chief Executive Officer of Ulta Beauty, Inc., has been appointed President and Chief Executive Officer and a member of the Company’s Board
of Directors (the “Board”) and the Executive Committee of the Board, each effective September 1, 2022. A copy of the press release is furnished as Exhibit
99.1, which is incorporated herein by reference.
 
Ms. Dillon served as Executive Chair of the Board of Directors of Ulta Beauty, Inc. from June 2021 through June 2022. She previously served as
Chief Executive Officer and a member of the Board of Directors of Ulta from July 2013 through June 2021. Prior to Ulta, she served as President and Chief
Executive Officer and a member of the Board of Directors of United States Cellular Corporation from 2010 through 2013; and Global Chief Marketing
Officer and Executive Vice President of McDonald’s Corporation from 2005 through 2010. Previously, Ms. Dillon held several positions of increasing
responsibility at PepsiCo Corporation, including as President of the Quaker Foods division from 2004 through 2005 and as Vice President of Marketing for
Gatorade and Quaker Foods from 2002 through 2004. Ms. Dillon also currently serves on the Board of Directors of each of Starbucks Corporation and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 6.3 ([7] FOOTLOCKER_2022_8K_dated_2022-08-19 FY2022 p.1)
- **Claim:** She served as CEO of Ulta from July 2013 through June 2021 and as Executive Chair from June 2021 through June 2022 [7].
- **Cited Chunk Text:**
```text
Item 5.02. Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory
Arrangements of Certain Officers.
 
On August 19, 2022, Foot Locker, Inc. (the “Company”), issued a press release announcing that, as part of a planned succession process, Richard
A. Johnson will step down as President and Chief Executive Officer of the Company, effective September 1, 2022. Mary N. Dillon, 61, former Executive
Chair and Chief Executive Officer of Ulta Beauty, Inc., has been appointed President and Chief Executive Officer and a member of the Company’s Board
of Directors (the “Board”) and the Executive Committee of the Board, each effective September 1, 2022. A copy of the press release is furnished as Exhibit
99.1, which is incorporated herein by reference.
 
Ms. Dillon served as Executive Chair of the Board of Directors of Ulta Beauty, Inc. from June 2021 through June 2022. She previously served as
Chief Executive Officer and a member of the Board of Directors of Ulta from July 2013 through June 2021. Prior to Ulta, she served as President and Chief
Executive Officer and a member of the Board of Directors of United States Cellular Corporation from 2010 through 2013; and Global Chief Marketing
Officer and Executive Vice President of McDonald’s Corporation from 2005 through 2010. Previously, Ms. Dillon held several positions of increasing
responsibility at PepsiCo Corporation, including as President of the Quaker Foods division from 2004 through 2005 and as Vice President of Marketing for
Gatorade and Quaker Foods from 2002 through 2004. Ms. Dillon also currently serves on the Board of Directors of each of Starbucks Corporation and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 6.4 ([7] FOOTLOCKER_2022_8K_dated_2022-08-19 FY2022 p.1)
- **Claim:** She also previously served as President and CEO of United States Cellular Corporation from 2010 through 2013 [7].
- **Cited Chunk Text:**
```text
Item 5.02. Departure of Directors or Certain Officers; Election of Directors; Appointment of Certain Officers; Compensatory
Arrangements of Certain Officers.
 
On August 19, 2022, Foot Locker, Inc. (the “Company”), issued a press release announcing that, as part of a planned succession process, Richard
A. Johnson will step down as President and Chief Executive Officer of the Company, effective September 1, 2022. Mary N. Dillon, 61, former Executive
Chair and Chief Executive Officer of Ulta Beauty, Inc., has been appointed President and Chief Executive Officer and a member of the Company’s Board
of Directors (the “Board”) and the Executive Committee of the Board, each effective September 1, 2022. A copy of the press release is furnished as Exhibit
99.1, which is incorporated herein by reference.
 
Ms. Dillon served as Executive Chair of the Board of Directors of Ulta Beauty, Inc. from June 2021 through June 2022. She previously served as
Chief Executive Officer and a member of the Board of Directors of Ulta from July 2013 through June 2021. Prior to Ulta, she served as President and Chief
Executive Officer and a member of the Board of Directors of United States Cellular Corporation from 2010 through 2013; and Global Chief Marketing
Officer and Executive Vice President of McDonald’s Corporation from 2005 through 2010. Previously, Ms. Dillon held several positions of increasing
responsibility at PepsiCo Corporation, including as President of the Quaker Foods division from 2004 through 2005 and as Vice President of Marketing for
Gatorade and Quaker Foods from 2002 through 2004. Ms. Dillon also currently serves on the Board of Directors of each of Starbucks Corporation and
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 6.5 (NO CITATION)
- **Claim:** The excerpts describe Ulta as a consumer-driven, omni-channel retailer, but do not explicitly state that it is a "similar company" to Foot Locker; that characterization is not in the excerpts.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 7. `financebench_id_00746` (Ulta Beauty)
- **Question:** Which debt securities are registered to trade on a national securities exchange under Ulta Beauty's name as of FY2023?
- **Predicted Answer:**

> Based on the provided excerpts, the only security registered pursuant to Section 12(b) of the Act under Ulta Beauty's name is its **common stock, par value $0.01 per share (trading symbol: ULTA)**, listed on the NASDAQ Global Select Market [1]. The excerpts do not identify any debt securities registered to trade on a national securities exchange [1].

### Pair 7.1 ([1] ULTABEAUTY_2023_10K FY2023 p.0)
- **Claim:** Based on the provided excerpts, the only security registered pursuant to Section 12(b) of the Act under Ulta Beauty's name is its **common stock, par value $0.01 per share (trading symbol: ULTA)**, listed on the NASDAQ Global Select Market [1].
- **Cited Chunk Text:**
```text
Table of Contents
UNITED STATES
SECURITIES AND EXCHANGE COMMISSION
Washington, DC 20549
FORM 10-K
☒ Annual Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934
For the fiscal year ended January 28, 2023
or
☐ Transition Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934
For the transition period from _____________ to _____________
Commission File Number: 001-33764
ULTA BEAUTY, INC.
(Exact name of registrant as specified in its charter)
Delaware
(State or other jurisdiction of
incorporation or organization)
38-4022268
(I.R.S. Employer
Identification No.)
1000 Remington Blvd., Suite 120
Bolingbrook, Illinois
(Address of principal executive offices)
60440
(Zip code)
Registrant’s telephone number, including area code: (630) 410-4800
Securities registered pursuant to Section 12(b) of the Act:
Title of each class Trading symbol Name of each exchange on which registered
Common stock, par value $0.01 per share ULTA The NASDAQ Global Select Market
Securities registered pursuant to Section 12(g) of the Act: None
Indicate by check mark if the registrant is a well-known seasoned issuer, as defined in Rule 405 of the Securities Act. ⌧ Yes ◻ No
Indicate by check mark if the registrant is not required to file reports pursuant to Section 13 or Section 15(d) of the Act. ◻ Yes ⌧ No
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 7.2 ([1] ULTABEAUTY_2023_10K FY2023 p.0)
- **Claim:** The excerpts do not identify any debt securities registered to trade on a national securities exchange [1].
- **Cited Chunk Text:**
```text
Table of Contents
UNITED STATES
SECURITIES AND EXCHANGE COMMISSION
Washington, DC 20549
FORM 10-K
☒ Annual Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934
For the fiscal year ended January 28, 2023
or
☐ Transition Report Pursuant to Section 13 or 15(d) of the Securities Exchange Act of 1934
For the transition period from _____________ to _____________
Commission File Number: 001-33764
ULTA BEAUTY, INC.
(Exact name of registrant as specified in its charter)
Delaware
(State or other jurisdiction of
incorporation or organization)
38-4022268
(I.R.S. Employer
Identification No.)
1000 Remington Blvd., Suite 120
Bolingbrook, Illinois
(Address of principal executive offices)
60440
(Zip code)
Registrant’s telephone number, including area code: (630) 410-4800
Securities registered pursuant to Section 12(b) of the Act:
Title of each class Trading symbol Name of each exchange on which registered
Common stock, par value $0.01 per share ULTA The NASDAQ Global Select Market
Securities registered pursuant to Section 12(g) of the Act: None
Indicate by check mark if the registrant is a well-known seasoned issuer, as defined in Rule 405 of the Securities Act. ⌧ Yes ◻ No
Indicate by check mark if the registrant is not required to file reports pursuant to Section 13 or Section 15(d) of the Act. ◻ Yes ⌧ No
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 8. `financebench_id_06272` (Coca-Cola)
- **Question:** What is Coca Cola's FY2022 dividend payout ratio (using total cash dividends paid and net income attributable to shareholders)? Round answer to two decimal places. Answer the question asked by assuming you only have access to information clearly displayed in the cash flow statement and the income statement.
- **Predicted Answer:**

> Based on the provided excerpts:
> 
> - Total cash dividends paid in FY2022: **$7,616 million** [1] (the income statement shows dividends per share of $1.76 [3], but the cash paid figure is stated on page 56 [1]).
> - Net income attributable to shareowners of The Coca-Cola Company in FY2022: **$9,542 million** [9].
> 
> Dividend payout ratio = $7,616 / $9,542 = **0.80** (rounded to two decimal places).
> 
> **Answer: 0.80**

### Pair 8.1 ([1] COCACOLA_2022_10K FY2022 p.56)
- **Claim:** Total cash dividends paid in FY2022: **$7,616 million** [1] (the income statement shows dividends per share of $1.76 [3], but the cash paid figure is stated on page 56 [1]).
- **Cited Chunk Text:**
```text
stock issued to employees. The net impact of the Company’s issuances of stock and share repurchases during 2022 resulted in a net cash outflow of $581 million.
During 2021, the Company did not repurchase shares of our common stock under the share repurchase plans authorized by our Board of Directors.
Dividends
The Company paid dividends of $7,616 million and $7,252 million during the years ended December 31, 2022 and 2021, respectively.
At its February 2023 meeting, our Board of Directors increased our regular quarterly dividend to $0.46 per share, equivalent to a full year dividend of $1.84 per share in 2023.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 8.2 ([3] COCACOLA_2022_10K FY2022 p.66)
- **Claim:** Total cash dividends paid in FY2022: **$7,616 million** [1] (the income statement shows dividends per share of $1.76 [3], but the cash paid figure is stated on page 56 [1]).
- **Cited Chunk Text:**
```text
THE COCA-COLA COMPANY AND SUBSIDIARIES
CONSOLIDATED STATEMENTS OF SHAREOWNERS’ EQUITY
(In millions except per share data)
Year Ended December 31, 2022 2021 2020
Equity Attributable to Shareowners of The Coca-Cola Company    
    Number of Common Shares Outstanding    
   Balance at beginning of year 4,325 4,302 4,280 
Treasury stock issued to employees related to stock-based compensation plans 24 23 22 
Purchases of stock for treasury (21) — — 
   Balance at end of year 4,328 4,325 4,302 
    Common Stock $ 1,760 $ 1,760 $ 1,760 
    Capital Surplus    
   Balance at beginning of year 18,116 17,601 17,154 
Stock issued to employees related to stock-based compensation plans 373 216 307 
Stock-based compensation expense 332 299 141 
Other activities 1 — (1)
   Balance at end of year 18,822 18,116 17,601 
    Reinvested Earnings    
   Balance at beginning of year 69,094 66,555 65,855 
Adoption of accounting standards — 19 — 
Net income attributable to shareowners of The Coca-Cola Company 9,542 9,771 7,747 
Dividends (per share — $1.76, $1.68 and $1.64 in 2022, 2021 and 2020, respectively) (7,617) (7,251) (7,047)
   Balance at end of year 71,019 69,094 66,555 
    Accumulated Other Comprehensive Income (Loss)    
   Balance at beginning of year (14,330) (14,601) (13,544)
Net other comprehensive income (loss) (565) 271 (1,057)
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 8.3 ([9] COCACOLA_2022_10K FY2022 p.62)
- **Claim:** Net income attributable to shareowners of The Coca-Cola Company in FY2022: **$9,542 million** [9].
- **Cited Chunk Text:**
```text
THE COCA-COLA COMPANY AND SUBSIDIARIES
CONSOLIDATED STATEMENTS OF INCOME
(In millions except per share data)
Year Ended December 31, 2022 2021 2020
Net Operating Revenues $ 43,004 $ 38,655 $ 33,014 
Cost of goods sold 18,000 15,357 13,433 
Gross Profit 25,004 23,298 19,581 
Selling, general and administrative expenses 12,880 12,144 9,731 
Other operating charges 1,215 846 853 
Operating Income 10,909 10,308 8,997 
Interest income 449 276 370 
Interest expense 882 1,597 1,437 
Equity income (loss) — net 1,472 1,438 978 
Other income (loss) — net (262) 2,000 841 
Income Before Income Taxes 11,686 12,425 9,749 
Income taxes 2,115 2,621 1,981 
Consolidated Net Income 9,571 9,804 7,768 
Less: Net income (loss) attributable to noncontrolling interests 29 33 21 
Net Income Attributable to Shareowners of The Coca-Cola Company $ 9,542 $ 9,771 $ 7,747 
Basic Net Income Per Share $ 2.20 $ 2.26 $ 1.80 
Diluted Net Income Per Share $ 2.19 $ 2.25 $ 1.79 
Average Shares Outstanding — Basic 4,328 4,315 4,295 
Effect of dilutive securities 22 25 28 
Average Shares Outstanding — Diluted 4,350 4,340 4,323 
Calculated based on net income attributable to shareowners of The Coca-Cola Company.
Refer to Notes to Consolidated Financial Statements.
1
1
1 
61
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 8.4 (NO CITATION)
- **Claim:** Dividend payout ratio = $7,616 / $9,542 = **0.80** (rounded to two decimal places).
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 9. `financebench_id_00517` (Boeing)
- **Question:** Are there any product categories / service categories that represent more than 20% of Boeing's revenue for FY2022?
- **Predicted Answer:**

> Based on the provided excerpts, the revenue breakdown is given by **segment** (Commercial Airplanes, Defense, Space & Security, Global Services, Boeing Capital) rather than by individual product or service category. The only product/service split shown is total "Sales of products" and "Sales of services" [2].
> 
> Using the segment figures for FY2022 [1]:
> - Commercial Airplanes: $25,867M of $66,608M total ≈ 38.8%
> - Defense, Space & Security: $23,162M ≈ 34.8%
> - Global Services: $17,611M ≈ 26.4%
> - Boeing Capital: $199M ≈ 0.3%
> 
> So, three segments each exceed 20% of total revenue: Commercial Airplanes, Defense, Space & Security, and Global Services [1].
> 
> However, the excerpts do not provide a product-category or service-category breakdown (e.g., by aircraft model or specific service line) sufficient to determine whether any individual product or service category exceeds 20% of revenue. That specific breakdown is not in the excerpts.

### Pair 9.1 (NO CITATION)
- **Claim:** Based on the provided excerpts, the revenue breakdown is given by **segment** (Commercial Airplanes, Defense, Space & Security, Global Services, Boeing Capital) rather than by individual product or service category.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.2 ([2] BOEING_2022_10K FY2022 p.54)
- **Claim:** The only product/service split shown is total "Sales of products" and "Sales of services" [2].
- **Cited Chunk Text:**
```text
Table of Contents
The Boeing Company and Subsidiaries
Consolidated Statements of Operations
(Dollars in millions, except per share data)    
Years ended December 31, 2022 2021 2020
Sales of products $55,893 $51,386 $47,142 
Sales of services 10,715 10,900 11,016 
Total revenues 66,608 62,286 58,158 
Cost of products (53,969) (49,954) (54,568)
Cost of services (9,109) (9,283) (9,232)
Boeing Capital interest expense (28) (32) (43)
Total costs and expenses (63,106) (59,269) (63,843)
3,502 3,017 (5,685)
(Loss)/income from operating investments, net (16) 210 9 
General and administrative expense (4,187) (4,157) (4,817)
Research and development expense, net (2,852) (2,249) (2,476)
Gain on dispositions, net 6 277 202 
Loss from operations (3,547) (2,902) (12,767)
Other income, net 1,058 551 447 
Interest and debt expense (2,533) (2,682) (2,156)
Loss before income taxes (5,022) (5,033) (14,476)
Income tax (expense)/benefit (31) 743 2,535 
Net loss (5,053) (4,290) (11,941)
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.3 ([1] BOEING_2022_10K FY2022 p.61)
- **Claim:** Using the segment figures for FY2022 [1]:
- **Cited Chunk Text:**
```text
Table of Contents
The Boeing Company and Subsidiaries
Notes to the Consolidated Financial Statements
Summary of Business Segment Data
(Dollars in millions)  
Years ended December 31, 2022 2021 2020
Revenues:
Commercial Airplanes $25,867 $19,493 $16,162 
Defense, Space & Security 23,162 26,540 26,257 
Global Services 17,611 16,328 15,543 
Boeing Capital 199 272 261 
Unallocated items, eliminations and other (231) (347) (65)
Total revenues $66,608 $62,286 $58,158 
(Loss)/earnings from operations:
Commercial Airplanes ($2,370) ($6,475) ($13,847)
Defense, Space & Security (3,544) 1,544 1,539 
Global Services 2,727 2,017 450 
Boeing Capital 29 106 63 
Segment operating loss (3,158) (2,808) (11,795)
Unallocated items, eliminations and other (1,532) (1,267) (2,355)
FAS/CAS service cost adjustment 1,143 1,173 1,383 
Loss from operations (3,547) (2,902) (12,767)
Other income, net 1,058 551 447 
Interest and debt expense (2,533) (2,682) (2,156)
Loss before income taxes (5,022) (5,033) (14,476)
Income tax (expense)/benefit (31) 743 2,535
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.4 (NO CITATION)
- **Claim:** Commercial Airplanes: $25,867M of $66,608M total ≈ 38.8%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.5 (NO CITATION)
- **Claim:** Defense, Space & Security: $23,162M ≈ 34.8%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.6 (NO CITATION)
- **Claim:** Global Services: $17,611M ≈ 26.4%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.7 (NO CITATION)
- **Claim:** Boeing Capital: $199M ≈ 0.3%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.8 ([1] BOEING_2022_10K FY2022 p.61)
- **Claim:** So, three segments each exceed 20% of total revenue: Commercial Airplanes, Defense, Space & Security, and Global Services [1].
- **Cited Chunk Text:**
```text
Table of Contents
The Boeing Company and Subsidiaries
Notes to the Consolidated Financial Statements
Summary of Business Segment Data
(Dollars in millions)  
Years ended December 31, 2022 2021 2020
Revenues:
Commercial Airplanes $25,867 $19,493 $16,162 
Defense, Space & Security 23,162 26,540 26,257 
Global Services 17,611 16,328 15,543 
Boeing Capital 199 272 261 
Unallocated items, eliminations and other (231) (347) (65)
Total revenues $66,608 $62,286 $58,158 
(Loss)/earnings from operations:
Commercial Airplanes ($2,370) ($6,475) ($13,847)
Defense, Space & Security (3,544) 1,544 1,539 
Global Services 2,727 2,017 450 
Boeing Capital 29 106 63 
Segment operating loss (3,158) (2,808) (11,795)
Unallocated items, eliminations and other (1,532) (1,267) (2,355)
FAS/CAS service cost adjustment 1,143 1,173 1,383 
Loss from operations (3,547) (2,902) (12,767)
Other income, net 1,058 551 447 
Interest and debt expense (2,533) (2,682) (2,156)
Loss before income taxes (5,022) (5,033) (14,476)
Income tax (expense)/benefit (31) 743 2,535
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.9 (NO CITATION)
- **Claim:** However, the excerpts do not provide a product-category or service-category breakdown (e.g., by aircraft model or specific service line) sufficient to determine whether any individual product or service category exceeds 20% of revenue.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 9.10 (NO CITATION)
- **Claim:** That specific breakdown is not in the excerpts.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 10. `financebench_id_00684` (Amcor)
- **Question:** Does AMCOR have an improving gross margin profile as of FY2023? If gross margin is not a useful metric for a company like this, then state that and explain why.
- **Predicted Answer:**

> Based on the provided excerpts, Amcor's gross margin did not improve in FY2023.
> 
> - FY2023: Net sales of $14,694 million and gross profit of $2,725 million [10].
> - FY2022: Net sales of $14,544 million and gross profit of $2,820 million [10].
> 
> Gross profit declined from $2,820 million in FY2022 to $2,725 million in FY2023, while net sales increased, indicating a lower gross margin profile year over year [10].
> 
> The excerpts do not state that gross margin is an unsuitable metric for this company, so I cannot support that characterization from the provided context.

### Pair 10.1 (NO CITATION)
- **Claim:** Based on the provided excerpts, Amcor's gross margin did not improve in FY2023.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 10.2 ([10] AMCOR_2023_10K FY2023 p.49)
- **Claim:** FY2023: Net sales of $14,694 million and gross profit of $2,725 million [10].
- **Cited Chunk Text:**
```text
Amcor plc and Subsidiaries
Consolidated Statements of Income
($ in millions, except per share data)
For the years ended June 30, 2023 2022 2021
Net sales $ 14,694 $ 14,544 $ 12,861 
Cost of sales (11,969) (11,724) (10,129)
Gross profit 2,725 2,820 2,732 
Selling, general, and administrative expenses (1,246) (1,284) (1,292)
Research and development expenses (101) (96) (100)
Restructuring, impairment, and other related activities, net 104 (234) (94)
Other income, net 26 33 75 
Operating income 1,508 1,239 1,321 
Interest income 31 24 14 
Interest expense (290) (159) (153)
Other non-operating income, net 2 11 11 
Income before income taxes and equity in income of affiliated companies 1,251 1,115 1,193 
Income tax expense (193) (300) (261)
Equity in income of affiliated companies, net of tax — — 19 
Net income $ 1,058 $ 815 $ 951 
Net income attributable to non-controlling interests (10) (10) (12)
Net income attributable to Amcor plc $ 1,048 $ 805 $ 939 
Basic earnings per share:
Basic earnings per share $ 0.709 $ 0.532 $ 0.604 
Diluted earnings per share $ 0.705 $ 0.529 $ 0.602 
 See accompanying notes to consolidated financial statements.
50
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 10.3 ([10] AMCOR_2023_10K FY2023 p.49)
- **Claim:** FY2022: Net sales of $14,544 million and gross profit of $2,820 million [10].
- **Cited Chunk Text:**
```text
Amcor plc and Subsidiaries
Consolidated Statements of Income
($ in millions, except per share data)
For the years ended June 30, 2023 2022 2021
Net sales $ 14,694 $ 14,544 $ 12,861 
Cost of sales (11,969) (11,724) (10,129)
Gross profit 2,725 2,820 2,732 
Selling, general, and administrative expenses (1,246) (1,284) (1,292)
Research and development expenses (101) (96) (100)
Restructuring, impairment, and other related activities, net 104 (234) (94)
Other income, net 26 33 75 
Operating income 1,508 1,239 1,321 
Interest income 31 24 14 
Interest expense (290) (159) (153)
Other non-operating income, net 2 11 11 
Income before income taxes and equity in income of affiliated companies 1,251 1,115 1,193 
Income tax expense (193) (300) (261)
Equity in income of affiliated companies, net of tax — — 19 
Net income $ 1,058 $ 815 $ 951 
Net income attributable to non-controlling interests (10) (10) (12)
Net income attributable to Amcor plc $ 1,048 $ 805 $ 939 
Basic earnings per share:
Basic earnings per share $ 0.709 $ 0.532 $ 0.604 
Diluted earnings per share $ 0.705 $ 0.529 $ 0.602 
 See accompanying notes to consolidated financial statements.
50
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 10.4 ([10] AMCOR_2023_10K FY2023 p.49)
- **Claim:** Gross profit declined from $2,820 million in FY2022 to $2,725 million in FY2023, while net sales increased, indicating a lower gross margin profile year over year [10].
- **Cited Chunk Text:**
```text
Amcor plc and Subsidiaries
Consolidated Statements of Income
($ in millions, except per share data)
For the years ended June 30, 2023 2022 2021
Net sales $ 14,694 $ 14,544 $ 12,861 
Cost of sales (11,969) (11,724) (10,129)
Gross profit 2,725 2,820 2,732 
Selling, general, and administrative expenses (1,246) (1,284) (1,292)
Research and development expenses (101) (96) (100)
Restructuring, impairment, and other related activities, net 104 (234) (94)
Other income, net 26 33 75 
Operating income 1,508 1,239 1,321 
Interest income 31 24 14 
Interest expense (290) (159) (153)
Other non-operating income, net 2 11 11 
Income before income taxes and equity in income of affiliated companies 1,251 1,115 1,193 
Income tax expense (193) (300) (261)
Equity in income of affiliated companies, net of tax — — 19 
Net income $ 1,058 $ 815 $ 951 
Net income attributable to non-controlling interests (10) (10) (12)
Net income attributable to Amcor plc $ 1,048 $ 805 $ 939 
Basic earnings per share:
Basic earnings per share $ 0.709 $ 0.532 $ 0.604 
Diluted earnings per share $ 0.705 $ 0.529 $ 0.602 
 See accompanying notes to consolidated financial statements.
50
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 10.5 (NO CITATION)
- **Claim:** The excerpts do not state that gross margin is an unsuitable metric for this company, so I cannot support that characterization from the provided context.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 11. `financebench_id_01163` (Nike)
- **Question:** Among operations, investing, and financing activities, which brought in the most (or lost the least) cash flow for Nike in FY2023?
- **Predicted Answer:**

> Based on the provided excerpts:
> 
> - **Investing activities** brought in cash: an inflow of $564 million for fiscal 2023 [3].
> - **Financing activities** lost cash: an outflow of $7,447 million for fiscal 2023 [4].
> - **Operating activities**: The excerpts show net income of $5,070 million for 2023 [6], but the actual "cash provided (used) by operations" total figure is not explicitly stated in the excerpts (the line item appears only as a heading) [6].
> 
> Comparing the two explicitly stated figures, **investing activities** brought in the most cash (an inflow of $564 million) versus financing's outflow of $7,447 million [3][4]. However, the total cash from operations figure is not provided in the excerpts, so a complete comparison across all three categories cannot be made from the given context.

### Pair 11.1 ([3] NIKE_2023_10K FY2023 p.47)
- **Claim:** **Investing activities** brought in cash: an inflow of $564 million for fiscal 2023 [3].
- **Cited Chunk Text:**
```text
the current period and timing of wholesale shipments. Further impacting these changes was a lower available supply of inventory 
in the prior year due to supply chain constraints. 
Cash provided (used) by investing activities was an inflow of $564 million for fiscal 2023, compared to an outflow of $1,524 
million for fiscal 2022, primarily driven by the net change in short-term investments. For fiscal 2023, the net change in short-term
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 11.2 ([4] NIKE_2023_10K FY2023 p.48)
- **Claim:** **Financing activities** lost cash: an outflow of $7,447 million for fiscal 2023 [4].
- **Cited Chunk Text:**
```text
investments (including sales, maturities and purchases) resulted in a cash inflow of $1,481 million compared to a cash outflow of 
$747 million for fiscal 2022. Additionally, we continue to invest in our infrastructure to support future growth, specifically focused 
around digital capabilities, our end-to-end technology foundation, our corporate facilities and improvements across our supply 
chain. 
Cash provided (used) by financing activities was an outflow of $7,447 million for fiscal 2023 compared to an outflow of $4,836 
million for fiscal 2022. The increased outflow in fiscal 2023 was driven by higher share repurchases of $5,480 million for fiscal 
2023 compared to $4,014 million for fiscal 2022, the repayment of $500 million of senior notes that matured in fiscal 2023, as well 
as lower proceeds from stock option exercises, which resulted in a cash inflow of $651 million in fiscal 2023 compared to $1,151 
million in fiscal 2022.
In fiscal 2023, we purchased a total of 50.0 million shares of NIKE's Class B Common Stock for $5.5 billion (an average price of 
$110.32 per share). In August 2022, we terminated the previous four-year, $15 billion share repurchase program approved by the 
Board of Directors in June 2018. Under this program, we repurchased 6.5 million shares for a total approximate cost of 
$710.0 million (an average price of $109.85 per share) during the first quarter of fiscal 2023 and 83.8 million shares for a total 
approximate cost of $9.4 billion (an average price of $111.82 per share) during the term of the program. Upon termination of the
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 11.3 ([6] NIKE_2023_10K FY2023 p.61)
- **Claim:** **Operating activities**: The excerpts show net income of $5,070 million for 2023 [6], but the actual "cash provided (used) by operations" total figure is not explicitly stated in the excerpts (the line item appears only as a heading) [6].
- **Cited Chunk Text:**
```text
NIKE, INC.
CONSOLIDATED STATEMENTS OF CASH FLOWS
YEAR ENDED MAY 31,
(Dollars in millions) 2023 2022 2021
Cash provided (used) by operations:
Net income $ 5,070 $ 6,046 $ 5,727 
Adjustments to reconcile net income to net cash provided (used) by operations:
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 11.4 ([3] NIKE_2023_10K FY2023 p.47)
- **Claim:** Comparing the two explicitly stated figures, **investing activities** brought in the most cash (an inflow of $564 million) versus financing's outflow of $7,447 million [3][4].
- **Cited Chunk Text:**
```text
the current period and timing of wholesale shipments. Further impacting these changes was a lower available supply of inventory 
in the prior year due to supply chain constraints. 
Cash provided (used) by investing activities was an inflow of $564 million for fiscal 2023, compared to an outflow of $1,524 
million for fiscal 2022, primarily driven by the net change in short-term investments. For fiscal 2023, the net change in short-term
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 11.5 ([4] NIKE_2023_10K FY2023 p.48)
- **Claim:** Comparing the two explicitly stated figures, **investing activities** brought in the most cash (an inflow of $564 million) versus financing's outflow of $7,447 million [3][4].
- **Cited Chunk Text:**
```text
investments (including sales, maturities and purchases) resulted in a cash inflow of $1,481 million compared to a cash outflow of 
$747 million for fiscal 2022. Additionally, we continue to invest in our infrastructure to support future growth, specifically focused 
around digital capabilities, our end-to-end technology foundation, our corporate facilities and improvements across our supply 
chain. 
Cash provided (used) by financing activities was an outflow of $7,447 million for fiscal 2023 compared to an outflow of $4,836 
million for fiscal 2022. The increased outflow in fiscal 2023 was driven by higher share repurchases of $5,480 million for fiscal 
2023 compared to $4,014 million for fiscal 2022, the repayment of $500 million of senior notes that matured in fiscal 2023, as well 
as lower proceeds from stock option exercises, which resulted in a cash inflow of $651 million in fiscal 2023 compared to $1,151 
million in fiscal 2022.
In fiscal 2023, we purchased a total of 50.0 million shares of NIKE's Class B Common Stock for $5.5 billion (an average price of 
$110.32 per share). In August 2022, we terminated the previous four-year, $15 billion share repurchase program approved by the 
Board of Directors in June 2018. Under this program, we repurchased 6.5 million shares for a total approximate cost of 
$710.0 million (an average price of $109.85 per share) during the first quarter of fiscal 2023 and 83.8 million shares for a total 
approximate cost of $9.4 billion (an average price of $111.82 per share) during the term of the program. Upon termination of the
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 11.6 (NO CITATION)
- **Claim:** However, the total cash from operations figure is not provided in the excerpts, so a complete comparison across all three categories cannot be made from the given context.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 12. `financebench_id_00407` (MGM Resorts)
- **Question:** Which type of debt received the largest investment among the short term investments for MGM in H1 FY2023?
- **Predicted Answer:**

> Based on the short-term investments table as of June 30, 2023, corporate bonds received the largest investment at $416,420 thousand [1].

### Pair 12.1 ([1] MGMRESORTS_2023Q2_10Q FY2023 p.10)
- **Claim:** Based on the short-term investments table as of June 30, 2023, corporate bonds received the largest investment at $416,420 thousand [1].
- **Cited Chunk Text:**
```text
The following tables present information regarding the Company’s debt investments:
Fair value level June 30, 2023 December 31, 2022
(In thousands)
Cash and cash equivalents:
Money market funds Level 1 $ 2,195 $ 12,009 
Commercial paper and certificates of deposit Level 2 — 5,992 
Cash and cash equivalents 2,195 18,001 
Short-term investments:
U.S. government securities Level 1 57,696 56,835 
U.S. agency securities Level 2 29,049 9,530 
Commercial paper and certificates of deposit Level 2 4,561 4,466 
Corporate bonds Level 2 416,420 213,875 
Short-term investments 507,726 284,706 
Total debt investments $ 509,921 $ 302,707 
Restricted cash. MGM China’s pledged cash of $87 million and $124 million as of June 30, 2023 and December 31, 2022, respectively, securing the
bank guarantees discussed in Note 9 is restricted in use and classified within “Other long-term assets, net.” Such amounts plus “Cash and cash equivalents” on
the consolidated balance sheets equal “Cash, cash equivalents, and restricted cash” on the consolidated statements of cash flows as of June 30, 2023 and
December 31, 2022.
Accounts receivable. As of June 30, 2023 and December 31, 2022, the loss reserve on accounts receivable was $129 million and $113 million,
respectively.
Note receivable. In February 2023, the secured note receivable related to the sale of Circus Circus Las Vegas and the adjacent land was repaid, prior to
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 13. `financebench_id_01148` (Amcor)
- **Question:** What industry does AMCOR primarily operate in?
- **Predicted Answer:**

> Amcor primarily operates in the packaging industry. It is described as "a global leader in developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer goods end markets" [1][5][8]. The company develops and produces "a broad range of packaging products including flexible packaging, rigid packaging containers, specialty cartons, and closures" [1][7], and its business activities are organized around two reportable segments, Flexibles and Rigid Packaging [1][7].

### Pair 13.1 (NO CITATION)
- **Claim:** Amcor primarily operates in the packaging industry.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 13.2 ([1] AMCOR_2023_10K FY2023 p.54)
- **Claim:** It is described as "a global leader in developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer goods end markets" [1][5][8].
- **Cited Chunk Text:**
```text
Amcor plc and Subsidiaries
Notes to Consolidated Financial Statements
Note 1 - Business Description
    Amcor plc ("Amcor" or the "Company") is a public limited company incorporated under the Laws of the Bailiwick of Jersey. The Company's
history dates back more than 150 years, with origins in both Australia and the United States of America. Today, Amcor is a global leader in
developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer
goods end markets. The Company's innovation excellence and global packaging expertise enables the Company to solve packaging challenges
around the world every day, producing packaging that is more functional, appealing, and cost effective for its customers and their consumers and
importantly, more sustainable for the environment.
    The Company's business activities are organized around two reportable segments, Flexibles and Rigid Packaging. The Company has a globally
diverse operating footprint, selling to customers in Europe, North America, Latin America, and the Asia Pacific regions. The Company develops
and produces a broad range of packaging products including flexible packaging, rigid packaging containers, specialty cartons, and closures. The
Company's sales are widely diversified, with the majority of sales made to the food, beverage, pharmaceutical, medical device, home and
personal care, and other consumer goods end markets. All markets are considered to be highly competitive as to price, innovation, quality, and
service.
55
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 13.3 ([5] AMCOR_2023_10K FY2023 p.4)
- **Claim:** It is described as "a global leader in developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer goods end markets" [1][5][8].
- **Cited Chunk Text:**
```text
PART I
Item 1. - Business
The Company
    Amcor plc (ARBN 630 385 278) is a public limited company incorporated under the Laws of the Bailiwick of Jersey. Our history dates back
more than 150 years, with origins in both Australia and the USA. Today, we are a global leader in developing and producing responsible
packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other products. Our innovation excellence and global
packaging expertise enables us to solve packaging challenges around the world every day, producing packaging that is more functional,
appealing, and cost effective for our customers and their consumers and importantly, more sustainable for the environment.
Sustainability
    Sustainability is central to our business and one of our most exciting opportunities for growth. Working daily to embed sustainability deeper
into everything we do, Amcor has been a leader in the industry in promoting sustainability. We aspire to improve the quality of lives, protect
ecosystems, and preserve natural resources for future generations by offering a unique range of responsible packaging solutions, leveraging our
global scale, reach, and expertise to meet our customers’ growing sustainability expectations. In January 2018, we became the world’s first
packaging company to pledge that all our packaging would be designed to be recycled, compostable, or reusable by 2025 and also committed to
increasing the amount of recycled content we use. We are delivering against these commitments and continue to lead in the development of a
responsible packaging value chain through our innovations and partnerships. We have identified a clear path to meeting our sustainability
ambitions and those of our customers by focusing on the three elements of responsible packaging – product innovation, consumer participation,
and infrastructure development.
Differentiated Solutions
    Our product portfolio is diverse and dynamic due to our constant innovation and close partnerships with our customers. Behind every one of
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 13.4 ([8] AMCOR_2023Q2_10Q FY2023 p.9)
- **Claim:** It is described as "a global leader in developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer goods end markets" [1][5][8].
- **Cited Chunk Text:**
```text
Amcor plc and Subsidiaries
Notes to Condensed Consolidated Financial Statements
Note 1 - Nature of Operations and Basis of Presentation
    Amcor plc ("Amcor" or the "Company") is a public limited company incorporated under the Laws of the Bailiwick of Jersey. The Company's
history dates back more than 150 years, with origins in both Australia and the United States of America. Today, Amcor is a global leader in
developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer
goods end markets. The Company's innovation excellence and global packaging expertise enable the Company to solve packaging challenges
around the world every day, producing packaging that is more functional, appealing, and cost effective for its customers and their consumers and
importantly, more sustainable for the environment.
    The accompanying unaudited condensed consolidated financial statements have been prepared in accordance with accounting principles
generally accepted in the United States ("U.S. GAAP") for interim financial information. Consistent with these requirements, this Form 10-Q
does not include all the information required by U.S. GAAP for complete financial statements. Further, the year-end condensed consolidated
balance sheet data as of June 30, 2022 was derived from audited financial statements but does not include all disclosures required by U.S. GAAP.
It is management's opinion, however, that all material and recurring adjustments have been made that are necessary for a fair statement of its
interim financial position, results of operations, and cash flows. For further information, this Form 10-Q should be read in conjunction with the
audited consolidated financial statements and accompanying notes in the Company's Annual Report on Form 10-K for the fiscal year ended June
30, 2022.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 13.5 ([1] AMCOR_2023_10K FY2023 p.54)
- **Claim:** The company develops and produces "a broad range of packaging products including flexible packaging, rigid packaging containers, specialty cartons, and closures" [1][7], and its business activities are organized around two reportable segments, Flexibles and Rigid Packaging [1][7].
- **Cited Chunk Text:**
```text
Amcor plc and Subsidiaries
Notes to Consolidated Financial Statements
Note 1 - Business Description
    Amcor plc ("Amcor" or the "Company") is a public limited company incorporated under the Laws of the Bailiwick of Jersey. The Company's
history dates back more than 150 years, with origins in both Australia and the United States of America. Today, Amcor is a global leader in
developing and producing responsible packaging for food, beverage, pharmaceutical, medical, home and personal-care, and other consumer
goods end markets. The Company's innovation excellence and global packaging expertise enables the Company to solve packaging challenges
around the world every day, producing packaging that is more functional, appealing, and cost effective for its customers and their consumers and
importantly, more sustainable for the environment.
    The Company's business activities are organized around two reportable segments, Flexibles and Rigid Packaging. The Company has a globally
diverse operating footprint, selling to customers in Europe, North America, Latin America, and the Asia Pacific regions. The Company develops
and produces a broad range of packaging products including flexible packaging, rigid packaging containers, specialty cartons, and closures. The
Company's sales are widely diversified, with the majority of sales made to the food, beverage, pharmaceutical, medical device, home and
personal care, and other consumer goods end markets. All markets are considered to be highly competitive as to price, innovation, quality, and
service.
55
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 13.6 ([7] AMCOR_2020_10K FY2020 p.52)
- **Claim:** The company develops and produces "a broad range of packaging products including flexible packaging, rigid packaging containers, specialty cartons, and closures" [1][7], and its business activities are organized around two reportable segments, Flexibles and Rigid Packaging [1][7].
- **Cited Chunk Text:**
```text
Notes to Consolidated Financial Statements
 
Note 1 - Business Description
        Amcor plc ("Amcor" or the "Company") is a holding company originally incorporated under the name Arctic Jersey Limited as a limited company incorporated under the Laws of the Bailiwick
of Jersey in July 2018, in order to effect the Company's combination with Bemis Company, Inc. On October 10, 2018, Arctic Jersey Limited was renamed "Amcor plc" and became a public limited
company incorporated under the Laws of the Bailiwick of Jersey. On June 11, 2019, the Company completed its acquisition of Bemis Company, Inc ("Bemis"). The combination of Amcor and Bemis
has created a global packaging leader. See Note 4, "Acquisitions and Divestitures," for more information on the Bemis acquisition.
        The Company develops and produces a broad range of packaging products including flexible packaging, rigid packaging containers, specialty cartons, and closures. The Company employs
approximately 47,000 individuals and has 231 principal manufacturing facilities in more than 40 countries.
        The Company's business activities are organized around two reporting segments, Flexibles and Rigid Packaging. The Company has a globally diverse operating footprint, selling to customers in
Europe, North America, Latin America, Africa and the Asia Pacific regions. The Company's sales are widely diversified, with the majority of sales made to the defensive food, beverage,
pharmaceutical, medical device, home and personal care, and other consumer goods end markets. All markets are considered to be highly competitive as to price, innovation, quality and service.
53
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 14. `financebench_id_00005` (Corning)
- **Question:** Does Corning have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.
- **Predicted Answer:**

> Yes. Corning reported positive working capital of $2,278 million in FY2022 [1]. The context does not indicate that working capital is an irrelevant or non-useful metric for the company; in fact, the filing presents working capital measures and states that Corning funds its working capital with cash from operations and short-term borrowings [1][2].

### Pair 14.1 ([1] CORNING_2022_10K FY2022 p.33)
- **Claim:** Corning reported positive working capital of $2,278 million in FY2022 [1].
- **Cited Chunk Text:**
```text
2022   2021  
Working capital  $ 2,278  $ 2,853 
Current ratio  1.4:1  1.6:1 
Trade accounts receivable, net of doubtful accounts  $ 1,721  $ 2,004 
Days sales outstanding   45   49 
Inventories  $ 2,904  $ 2,481 
Inventory turns   3.4   3.7 
Days payable outstanding (1)   52   50 
Long-term debt  $ 6,687  $ 6,989 
Total debt  $ 6,911  $ 7,044 
Total debt to total capital   36%  36%
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 14.2 ([1] CORNING_2022_10K FY2022 p.33)
- **Claim:** The context does not indicate that working capital is an irrelevant or non-useful metric for the company; in fact, the filing presents working capital measures and states that Corning funds its working capital with cash from operations and short-term borrowings [1][2].
- **Cited Chunk Text:**
```text
2022   2021  
Working capital  $ 2,278  $ 2,853 
Current ratio  1.4:1  1.6:1 
Trade accounts receivable, net of doubtful accounts  $ 1,721  $ 2,004 
Days sales outstanding   45   49 
Inventories  $ 2,904  $ 2,481 
Inventory turns   3.4   3.7 
Days payable outstanding (1)   52   50 
Long-term debt  $ 6,687  $ 6,989 
Total debt  $ 6,911  $ 7,044 
Total debt to total capital   36%  36%
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 14.3 ([2] CORNING_2022_10K FY2022 p.33)
- **Claim:** The context does not indicate that working capital is an irrelevant or non-useful metric for the company; in fact, the filing presents working capital measures and states that Corning funds its working capital with cash from operations and short-term borrowings [1][2].
- **Cited Chunk Text:**
```text
Table of Contents
 
LIQUIDITY AND CAPITAL RESOURCES
 
Our financial condition and liquidity are strong. We are not aware of any known trends, demands, commitments, events or uncertainties that will result in or that are
reasonably likely to result in a material decrease in our liquidity. In addition, other than items discussed, there are no known material trends, favorable or unfavorable, in
our capital resources and no expected material changes in the mix of such resources.
 
Our major source of funding for 2023 and beyond will be our operating cash flow, our existing balances of cash and cash equivalents and proceeds from any issuances of
debt. We believe we have sufficient liquidity to fund operations, acquisitions, capital expenditures, scheduled debt repayments, dividend payments and share repurchase
programs through 2023. We will continue to generate cash from operations and maintain access to our revolving credit facilities and commercial paper programs as
discussed in more detail below.
 
Key Balance Sheet Data
 
We fund our working capital with cash from operations and short-term borrowings, including commercial paper, when necessary. In addition, we receive upfront cash
from customers relating to long-term supply agreements, as well as cash incentives from government entities generally for capital expansion and related expenses.
 
The following table presents balance sheet and working capital measures (in millions):
 
  December 31,
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 15. `financebench_id_01328` (PepsiCo)
- **Question:** What is the quantity of restructuring costs directly outlined in Pepsico's income statements for FY2022? If restructuring costs are not explicitly outlined then state 0.
- **Predicted Answer:**

> The consolidated statement of income in the excerpts does not separately outline a restructuring cost line item; it lists net revenue, cost of sales, gross profit, selling, general and administrative expenses, gain associated with the Juice Transaction, impairment of intangible assets, operating profit, and other lines [9]. Restructuring charges appear only in the notes and divisional tables (e.g., total restructuring and impairment charges of $411 million in 2022) [3][7], not as a directly outlined line in the income statement. Therefore, based strictly on the income statement presentation in the excerpts, restructuring costs are not explicitly outlined there.

### Pair 15.1 ([9] PEPSICO_2022_10K FY2022 p.61)
- **Claim:** The consolidated statement of income in the excerpts does not separately outline a restructuring cost line item; it lists net revenue, cost of sales, gross profit, selling, general and administrative expenses, gain associated with the Juice Transaction, impairment of intangible assets, operating profit, and other lines [9].
- **Cited Chunk Text:**
```text
Table of Contents
Consolidated Statement of Income
PepsiCo, Inc. and Subsidiaries
Fiscal years ended December 31, 2022, December 25, 2021 and December 26, 2020
(in millions except per share amounts)
2022 2021 2020
Net Revenue $ 86,392 $ 79,474 $ 70,372 
Cost of sales 40,576 37,075 31,797 
Gross profit 45,816 42,399 38,575 
Selling, general and administrative expenses 34,459 31,237 28,453 
Gain associated with the Juice Transaction (see Note 13) (3,321) — — 
Impairment of intangible assets (see Notes 1 and 4) 3,166 — 42 
Operating Profit 11,512 11,162 10,080 
Other pension and retiree medical benefits income 132 522 117 
Net interest expense and other (939) (1,863) (1,128)
Income before income taxes 10,705 9,821 9,069 
Provision for income taxes 1,727 2,142 1,894 
Net income 8,978 7,679 7,175 
Less: Net income attributable to noncontrolling interests 68 61 55 
Net Income Attributable to PepsiCo $ 8,910 $ 7,618 $ 7,120 
Net Income Attributable to PepsiCo per Common Share
Basic $ 6.45 $ 5.51 $ 5.14 
Diluted $ 6.42 $ 5.49 $ 5.12 
Weighted-average common shares outstanding
Basic 1,380 1,382 1,385 
Diluted 1,387 1,389 1,392 
See accompanying notes to the consolidated financial statements.
60
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 15.2 ([3] PEPSICO_2022_10K FY2022 p.77)
- **Claim:** Restructuring charges appear only in the notes and divisional tables (e.g., total restructuring and impairment charges of $411 million in 2022) [3][7], not as a directly outlined line in the income statement.
- **Cited Chunk Text:**
```text
the initiatives described above. As a result, we expect to incur pre-tax charges of approximately $3.65 billion, including cash
expenditures of approximately $2.9 billion. These pre-tax charges are expected to consist of approximately 55% of severance and
other employee-related costs, 10% for asset impairments (all non-cash) resulting from plant closures and related actions and 35%
for other costs associated with the implementation of our initiatives.
The total plan pre-tax charges are expected to be incurred by division approximately as follows:
FLNA QFNA PBNA LatAm Europe AMESA APAC Corporate
Expected pre-tax charges 15 % 1 % 25 % 10 % 25 % 5 % 4 % 15 %
A summary of our 2019 Productivity Plan charges is as follows:
2022 2021 2020
Cost of sales $ 33 $ 29 $ 30 
Selling, general and administrative expenses 347 208 239 
Other pension and retiree medical benefits expense 31 10 20 
Total restructuring and impairment charges $ 411 $ 247 $ 289 
After-tax amount $ 334 $ 206 $ 231 
Impact on net income attributable to PepsiCo per common share $ (0.24) $ (0.15) $ (0.17)
76
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 15.3 ([7] PEPSICO_2022_10K FY2022 p.78)
- **Claim:** Restructuring charges appear only in the notes and divisional tables (e.g., total restructuring and impairment charges of $411 million in 2022) [3][7], not as a directly outlined line in the income statement.
- **Cited Chunk Text:**
```text
Table of Contents
2022 2021 2020
Plan to Date
through 12/31/2022
FLNA $ 46 $ 28 $ 83 $ 210 
QFNA 7 — 5 19 
PBNA 68 20 47 226 
LatAm 32 37 31 171 
Europe 109 81 48 343 
AMESA 12 15 14 82 
APAC 16 7 5 77 
Corporate 90 49 36 229 
380 237 269 1,357 
Other pension and retiree medical
benefits income 31 10 20 98 
Total $ 411 $ 247 $ 289 $ 1,455 
Plan to Date
through 12/31/2022
Severance and other employee costs $ 807 
Asset impairments 190 
Other costs 458 
Total $ 1,455 
Severance and other employee costs primarily include severance and other termination benefits, as well as voluntary separation
arrangements. Other costs primarily include costs associated with the implementation of our initiatives, including contract
termination costs, consulting and other professional fees.
A summary of our 2019 Productivity Plan is as follows:
Severance and Other
Employee Costs
Asset 
 Impairments Other Costs Total
Liability as of December 28, 2019 $ 128 $ — $ 21 $ 149 
2020 restructuring charges 158 33 98 289 
Cash payments (138) — (117) (255)
Non-cash charges and translation (26) (33) 3 (56)
Liability as of December 26, 2020 122 — 5 127 
2021 restructuring charges 120 32 95 247 
Cash payments (163) — (93) (256)
Non-cash charges and translation (15) (32) — (47)
Liability as of December 25, 2021 64 — 7 71 
2022 restructuring charges 243 33 135 411
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 15.4 (NO CITATION)
- **Claim:** Therefore, based strictly on the income statement presentation in the excerpts, restructuring costs are not explicitly outlined there.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 16. `financebench_id_01491` (Johnson & Johnson)
- **Question:** What is the amount of the cash proceeds that JnJ realised from the separation of Kenvue (formerly Consumer Health business segment), as of August 30, 2023?
- **Predicted Answer:**

> The cash proceeds Johnson & Johnson realized from the Kenvue separation were **$13.2 billion**, generated from the Kenvue debt offering and initial public offering [2][6].

### Pair 16.1 ([2] JOHNSON_JOHNSON_2023_8K_dated-2023-08-30 FY2023 p.3)
- **Claim:** The cash proceeds Johnson & Johnson realized from the Kenvue separation were **$13.2 billion**, generated from the Kenvue debt offering and initial public offering [2][6].
- **Cited Chunk Text:**
```text
Exhibit 99.1
Johnson & Johnson Announces Updated Financials and 2023 Guidance Following Completion of the Kenvue
Separation
• Company expects increased 2023 Reported Sales Growth of 7.0% - 8.0%, Operational Sales Growth of 7.5% - 8.5%, and
Adjusted Operational Sales Growth of 6.2% - 7.2%; Figures exclude the COVID-19 Vaccine
• Company expects 2023 Adjusted Reported Earnings Per Share (EPS) of $10.00 - $10.10, reflecting increased growth of
12.5% at the mid-point and Adjusted Operational EPS of $9.90 - $10.00, reflecting increased growth of 11.5% at the mid-
point
• Company reduced outstanding share count by approximately 191 million; 2023 guidance reflects only a partial-year benefit
of approximately 73.5 million shares or $0.28 benefit to EPS
• Company secured $13.2 billion in cash proceeds from the Kenvue debt offering and initial public offering and maintains 9.5%
of equity stake in Kenvue
• Company maintains its quarterly dividend of $1.19 per share
New Brunswick, N.J. (August 30, 2023) – Johnson & Johnson (NYSE: JNJ) (“the Company”) today announced updates to its financials and
2023 guidance which reflect its operations as a company focused on transformational innovation in Pharmaceutical and MedTech. The
Company has published a recorded webinar for investors to provide additional context behind the updated financials and 2023 guidance
found in this release, which may be accessed by visiting the Investors section of the Company's website at webcasts & presentations.
“The completion of this transaction uniquely positions Johnson & Johnson as a Pharmaceutical and MedTech company focused on delivering
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 16.2 ([6] JOHNSON_JOHNSON_2023_8K_dated-2023-08-30 FY2023 p.5)
- **Claim:** The cash proceeds Johnson & Johnson realized from the Kenvue separation were **$13.2 billion**, generated from the Kenvue debt offering and initial public offering [2][6].
- **Cited Chunk Text:**
```text
shares of common stock accepted in the exchange offer.
The weighted average shares outstanding used in the calculation of the August 2023 Guidance for Adjusted Diluted EPS reflects the net
reduction of approximately 73.5 million shares of Johnson & Johnson outstanding common stock as a result of the Kenvue exchange offer.
Because this net reduction occurred on August 23, 2023, Johnson & Johnson will recognize only a partial-year benefit of $0.28 to its full-year
2023 Adjusted Diluted EPS.
The Company generated $13.2 billion in cash proceeds as result of the Kenvue debt offering and initial public offering. Additionally, Johnson
& Johnson maintains a 9.5% stake in Kenvue common stock, which provides the Company the opportunity to monetize the retained stake in
a tax efficient manner in the next year, subject to a
6
1,2,5
2,5 
3,5 
2,4 
3,4 
8 7
1 
2 
3
4 
5 
6 
7 
8
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 17. `financebench_id_03282` (Netflix)
- **Question:** What is Netflix's year end FY2017 total current liabilities (in USD millions)? Base your judgments on the information provided primarily in the balance sheet.
- **Predicted Answer:**

> Based on the provided excerpts, Netflix's total current liabilities as of December 31, 2017 were $5,466,312 thousand [3], which equals approximately $5,466.3 million.

### Pair 17.1 ([3] NETFLIX_2017_10K FY2017 p.44)
- **Claim:** Based on the provided excerpts, Netflix's total current liabilities as of December 31, 2017 were $5,466,312 thousand [3], which equals approximately $5,466.3 million.
- **Cited Chunk Text:**
```text
$ 4,173,041  $ 3,632,711 Accounts payable
 359,555  312,842 Accrued expenses
 315,094  197,632 Deferred revenue
 618,622  443,472 Total current liabilities
 5,466,312  4,586,657 Non-current content liabilities
 3,329,796  2,894,654 Long-term debt
 6,499,432  3,364,311 Other non-current liabilities
 135,246  61,188 Total liabilities
 15,430,786  10,906,810 Commitments and contingenc
ies (Note 5)  Stockholders’ equity:
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 18. `financebench_id_01009` (PepsiCo)
- **Question:** What are the geographies that Pepsico primarily operates in as of FY2022?
- **Predicted Answer:**

> The excerpts do not provide a full list of the geographies where PepsiCo primarily operates. The only geography-related facts stated are that PepsiCo's research centers are located around the world, including in Brazil, China, India, Ireland, Mexico, Russia, South Africa, the United Kingdom and the United States [7], and that its products are made, manufactured, distributed or sold in more than 200 other countries and territories [7]. A statement of PepsiCo's primary operating geographies as of FY2022 is not explicitly provided in the excerpts.

### Pair 18.1 (NO CITATION)
- **Claim:** The excerpts do not provide a full list of the geographies where PepsiCo primarily operates.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 18.2 ([7] PEPSICO_2022_10K FY2022 p.9)
- **Claim:** The only geography-related facts stated are that PepsiCo's research centers are located around the world, including in Brazil, China, India, Ireland, Mexico, Russia, South Africa, the United Kingdom and the United States [7], and that its products are made, manufactured, distributed or sold in more than 200 other countries and territories [7].
- **Cited Chunk Text:**
```text
dairy, protein, fiber, micronutrients and hydration; development of packaging technology and new package designs, including
reducing the amount of plastic in our packaging and developing recyclable, compostable, biodegradable or otherwise sustainable
packaging; development of marketing, merchandising and dispensing equipment; further expanding our beyond the bottle
portfolio including innovation for our SodaStream business; investments in technology and digitalization, including artificial
intelligence and data analytics to enhance our consumer insights and research; continuing to strengthen our omnichannel
capabilities, particularly in e-commerce; and efforts focused on reducing our impact on the environment, including reducing
water use in our operations and our agricultural practices and reducing our environmental impact in our operations throughout
our value chain.
Our research centers are located around the world, including in Brazil, China, India, Ireland, Mexico, Russia, South Africa, the
United Kingdom and the United States, and leverage consumer insights, food science and engineering to meet our strategy to
continually innovate our portfolio of beverages and convenient foods.
Regulatory Matters
The conduct of our businesses, including the production, storage, distribution, sale, display, advertising, marketing, labeling,
content, quality, safety, transportation, packaging, disposal, recycling and use of our products, as well as our employment and
occupational health and safety practices and protection of personal information, are subject to various laws and regulations
administered by federal, state and local governmental agencies in the United States, as well as to laws and regulations
administered by government entities and agencies in the more than 200 other countries and territories in which our products are
made, manufactured, distributed or sold. It is our policy to abide by the laws and regulations around the world that apply to our
businesses.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 18.3 (NO CITATION)
- **Claim:** A statement of PepsiCo's primary operating geographies as of FY2022 is not explicitly provided in the excerpts.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 19. `financebench_id_02608` (Best Buy)
- **Question:** In agreement with the information outlined in the income statement, what is the FY2015 - FY2017 3 year average net profit margin (as a %) for Best Buy? Answer in units of percents and round to one decimal place.
- **Predicted Answer:**

> Based on the provided excerpts, I can calculate the net profit margin for each year using net earnings attributable to Best Buy Co., Inc. shareholders [2] divided by revenue [3]:
> 
> - FY2017: $1,228 / $39,403 = 3.12%
> - FY2016: $897 / $39,528 = 2.27%
> - FY2015: $1,233 / $40,339 = 3.06%
> 
> 3-year average = (3.12% + 2.27% + 3.06%) / 3 = **2.8%**
> 
> Note: The FY2015 net earnings figure of $1,233 million is from the 12-month column in [3], and revenue of $40,339 million is from [2]. The FY2015 figure includes a $353 million discrete benefit [8], but the question asks for the reported net profit margin, so no adjustment is made.
> 
> **Answer: 2.8%**

### Pair 19.1 ([2] BESTBUY_2017_10K FY2017 p.25)
- **Claim:** Based on the provided excerpts, I can calculate the net profit margin for each year using net earnings attributable to Best Buy Co., Inc. shareholders [2] divided by revenue [3]:
- **Cited Chunk Text:**
```text
$ 39,403   $ 39,528   $ 40,339   $ 40,611   $ 38,252 Operating income
  1,854   1,375   1,450   1,144   90 Net earnings (loss) from con
tinuing operations  1,207   807   1,246   695   (259 ) Gain (loss) from discontinued op
erations  21   90   (11 )   (172 )   (161 ) Net earnings (loss) including non
controlling interests  1,228   897   1,235   523   (420 ) Net earnings (loss) attr
ibutable to Best Buy Co., Inc. shareholders  1,228   897   1,233   532   (441 ) Per Share Data
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.2 ([3] BESTBUY_2017_10K FY2017 p.90)
- **Claim:** Based on the provided excerpts, I can calculate the net profit margin for each year using net earnings attributable to Best Buy Co., Inc. shareholders [2] divided by revenue [3]:
- **Cited Chunk Text:**
```text
ed operating results for each 3-month quarter and full year of fiscal 2017  and  2016  (unaudited) ($ in mill ions): 
Quarter   12-Month  
1st   2nd   3rd   4th   2017 Revenue
$ 8,443   $ 8,533   $ 8,945   $ 13,482   $ 39,403 Comparable sales % change 
(1) (0.1 )%   0.8 %   1.8 %   (0.7 )%   0.3 % Gross profit 
(2) $ 2,145   $ 2,062   $ 2,203   $ 3,030   $ 9,440 Operating income 
(3) 372   289   312   881   1,854 Net earnings from continuing op
erations226   182   192   607   1,207 Gain from discontinued opera
tions, net of tax3   16   2   —   21 Net earnings attributab
le to Best Buy Co., Inc. shareholders229   198   194   607   1,228 Diluted earnings per share 
(4)                   Continuing operations
$ 0.69   $ 0.56   $ 0.60   $ 1.91   $ 3.74 Discontinued operations
0.01   0.05   0.01   —   0.07 Diluted earnings per share
$ 0.70   $ 0.61   $ 0.61   $ 1.91   $ 3.81  
Quarter   12-Month  
1st   2nd   3rd   4th   2016 Revenue
$ 8,558   $ 8,528   $ 8,819   $ 13,623   $ 39,528 Comparable sales % change 
(1) 0.6 %   3.8 %   0.8 %   (1.7 )%   0.5 % Gross profit 
(5) $ 2,030   $ 2,098   $ 2,112   $ 2,951   $ 9,191 Operating income 
(6) 86   288   230   771   1,375 Net earnings from continuing op
erations37   164   129   477   807 Gain (loss) from discontinued op
erations, net of tax92   —   (4 )   2   90 Net earnings attributab
le to Best Buy Co., Inc. shareholders129   164   125   479   897 Diluted earnings (loss) per sh
are (4)                   Continuing operations
$ 0.10   $ 0.46   $ 0.37   $ 1.39   $ 2.30 Discontinued operations
0.26   —   (0.01 )   0.01   0.26 Diluted earnings per share
$ 0.36   $ 0.46   $ 0.36   $ 1.40   $ 2.56 (1)
Our comparable sales calculation compares revenue from stores, websites and call centers operating for at least  14  full months, as well as revenue related to certain other comparable sales channels for a particular period to the corresponding period in the prior year. Relocated stores, as well as remodeled, expanded and downsized stores closed more than 
14  days, are excluded from our comparable sales calculation until at least 
14  full months after reopening. Acquisitions are included in the comparable sales calcula tion beginning with the first fullquarter following the first anniversary of the date of the acquisition. The Canadian brand consolidation, which included
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.3 (NO CITATION)
- **Claim:** FY2017: $1,228 / $39,403 = 3.12%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.4 (NO CITATION)
- **Claim:** FY2016: $897 / $39,528 = 2.27%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.5 (NO CITATION)
- **Claim:** FY2015: $1,233 / $40,339 = 3.06%
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.6 (NO CITATION)
- **Claim:** 3-year average = (3.12% + 2.27% + 3.06%) / 3 = **2.8%**
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.7 ([3] BESTBUY_2017_10K FY2017 p.90)
- **Claim:** Note: The FY2015 net earnings figure of $1,233 million is from the 12-month column in [3], and revenue of $40,339 million is from [2].
- **Cited Chunk Text:**
```text
ed operating results for each 3-month quarter and full year of fiscal 2017  and  2016  (unaudited) ($ in mill ions): 
Quarter   12-Month  
1st   2nd   3rd   4th   2017 Revenue
$ 8,443   $ 8,533   $ 8,945   $ 13,482   $ 39,403 Comparable sales % change 
(1) (0.1 )%   0.8 %   1.8 %   (0.7 )%   0.3 % Gross profit 
(2) $ 2,145   $ 2,062   $ 2,203   $ 3,030   $ 9,440 Operating income 
(3) 372   289   312   881   1,854 Net earnings from continuing op
erations226   182   192   607   1,207 Gain from discontinued opera
tions, net of tax3   16   2   —   21 Net earnings attributab
le to Best Buy Co., Inc. shareholders229   198   194   607   1,228 Diluted earnings per share 
(4)                   Continuing operations
$ 0.69   $ 0.56   $ 0.60   $ 1.91   $ 3.74 Discontinued operations
0.01   0.05   0.01   —   0.07 Diluted earnings per share
$ 0.70   $ 0.61   $ 0.61   $ 1.91   $ 3.81  
Quarter   12-Month  
1st   2nd   3rd   4th   2016 Revenue
$ 8,558   $ 8,528   $ 8,819   $ 13,623   $ 39,528 Comparable sales % change 
(1) 0.6 %   3.8 %   0.8 %   (1.7 )%   0.5 % Gross profit 
(5) $ 2,030   $ 2,098   $ 2,112   $ 2,951   $ 9,191 Operating income 
(6) 86   288   230   771   1,375 Net earnings from continuing op
erations37   164   129   477   807 Gain (loss) from discontinued op
erations, net of tax92   —   (4 )   2   90 Net earnings attributab
le to Best Buy Co., Inc. shareholders129   164   125   479   897 Diluted earnings (loss) per sh
are (4)                   Continuing operations
$ 0.10   $ 0.46   $ 0.37   $ 1.39   $ 2.30 Discontinued operations
0.26   —   (0.01 )   0.01   0.26 Diluted earnings per share
$ 0.36   $ 0.46   $ 0.36   $ 1.40   $ 2.56 (1)
Our comparable sales calculation compares revenue from stores, websites and call centers operating for at least  14  full months, as well as revenue related to certain other comparable sales channels for a particular period to the corresponding period in the prior year. Relocated stores, as well as remodeled, expanded and downsized stores closed more than 
14  days, are excluded from our comparable sales calculation until at least 
14  full months after reopening. Acquisitions are included in the comparable sales calcula tion beginning with the first fullquarter following the first anniversary of the date of the acquisition. The Canadian brand consolidation, which included
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.8 ([2] BESTBUY_2017_10K FY2017 p.25)
- **Claim:** Note: The FY2015 net earnings figure of $1,233 million is from the 12-month column in [3], and revenue of $40,339 million is from [2].
- **Cited Chunk Text:**
```text
$ 39,403   $ 39,528   $ 40,339   $ 40,611   $ 38,252 Operating income
  1,854   1,375   1,450   1,144   90 Net earnings (loss) from con
tinuing operations  1,207   807   1,246   695   (259 ) Gain (loss) from discontinued op
erations  21   90   (11 )   (172 )   (161 ) Net earnings (loss) including non
controlling interests  1,228   897   1,235   523   (420 ) Net earnings (loss) attr
ibutable to Best Buy Co., Inc. shareholders  1,228   897   1,233   532   (441 ) Per Share Data
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 19.9 ([8] BESTBUY_2017_10K FY2017 p.26)
- **Claim:** The FY2015 figure includes a $353 million discrete benefit [8], but the question asks for the reported net profit margin, so no adjustment is made.
- **Cited Chunk Text:**
```text
Included within net earnings (loss) from continuing operations and net earnings (loss) attributable to Best  Buy Co., Inc. shareholders for fiscal 2015 includes $353 million due to a discretebenefit related to reorganizing certain European legal entities.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 20. `financebench_id_03856` (Adobe)
- **Question:** What is the FY2017 operating cash flow ratio for Adobe? Operating cash flow ratio is defined as: cash from operations / total current liabilities. Round your answer to two decimal places. Please utilize information provided primarily within the balance sheet and the cash flow statement.
- **Predicted Answer:**

> Based on the provided excerpts:
> 
> - FY2017 net cash provided by operating activities: $2,912,853 thousand [1][10]
> - Total current liabilities at December 1, 2017: $3,527,457 thousand [2]
> 
> Operating cash flow ratio = 2,912,853 / 3,527,457 = 0.8258...
> 
> **FY2017 operating cash flow ratio = 0.83** (rounded to two decimal places).

### Pair 20.1 ([1] ADOBE_2017_10K FY2017 p.60)
- **Claim:** FY2017 net cash provided by operating activities: $2,912,853 thousand [1][10]
- **Cited Chunk Text:**
```text
Table of Contents
61
ADOBE SYSTEMS INCORPORATED
 CONSOLIDATED STATEMENTS OF CASH FLOWS
(In thousands)
  Years Ended
 
December 1,
2017
December 2,
2016
November 27,
2015
Cash flows from operating activities:    
Net income $ 1,693,954 $ 1,168,782 $ 629,551
Adjustments to reconcile net income to net cash provided by operating activities:
Depreciation, amortization and accretion 325,997 331,535 339,473
Stock-based compensation 451,451 349,912 335,859
Deferred income taxes 51,605 24,222 (69,657)
Gain on the sale of property — — (21,415)
Unrealized (gains) losses on investments (5,494) 3,145 (9,210)
Excess tax benefits from stock-based compensation — (75,105) (68,153)
Other non-cash items 4,625 2,022 1,216
Changes in operating assets and liabilities, net of acquired assets and
    assumed liabilities:
Trade receivables, net (187,173) (160,416) (79,502)
Prepaid expenses and other current assets 28,040 (71,021) (7,701)
Trade payables (45,186) (6,281) 22,870
Accrued expenses 154,125 64,978 (22,564)
Income taxes payable (34,493) 43,115 97,934
Deferred revenue 475,402 524,840 320,801
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 20.2 ([10] ADOBE_2017_10K FY2017 p.60)
- **Claim:** FY2017 net cash provided by operating activities: $2,912,853 thousand [1][10]
- **Cited Chunk Text:**
```text
Deferred revenue 475,402 524,840 320,801
Net cash provided by operating activities 2,912,853 2,199,728 1,469,502
Cash flows from investing activities:    
Purchases of short-term investments (1,931,011) (2,285,222) (2,064,833)
Maturities of short-term investments 759,737 769,228 371,790
Proceeds from sales of short-term investments 1,393,929 860,849 1,176,476
Acquisitions, net of cash acquired (459,626) (48,427) (826,004)
Purchases of property and equipment (178,122) (203,805) (184,936)
Proceeds from sale of property — — 57,779
Purchases of long-term investments, intangibles and other assets (29,918) (58,433) (22,779)
Proceeds from sale of long-term investments 2,134 5,777 4,149
Net cash used for investing activities (442,877) (960,033) (1,488,358)
Cash flows from financing activities:    
Purchases of treasury stock (1,100,000) (1,075,000) (625,000)
Proceeds from issuance of treasury stock 158,351 145,697 164,270
Taxes paid related to net share settlement of equity awards (240,126) (236,400) (186,373)
Excess tax benefits from stock-based compensation — 75,105 68,153
Proceeds from debt issuance — — 989,280
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 20.3 ([2] ADOBE_2017_10K FY2017 p.56)
- **Claim:** Total current liabilities at December 1, 2017: $3,527,457 thousand [2]
- **Cited Chunk Text:**
```text
Table of Contents
57
 ADOBE SYSTEMS INCORPORATED
 CONSOLIDATED BALANCE SHEETS
(In thousands, except par value)
 
December 1,
2017
December 2,
2016
ASSETS
Current assets:    
Cash and cash equivalents $ 2,306,072 $ 1,011,315
Short-term investments 3,513,702 3,749,985
Trade receivables, net of allowances for doubtful accounts of $9,151 and $6,214, respectively 1,217,968 833,033
Prepaid expenses and other current assets 210,071 245,441
Total current assets 7,247,813 5,839,774
Property and equipment, net 936,976 816,264
Goodwill 5,821,561 5,406,474
Purchased and other intangibles, net 385,658 414,405
Investment in lease receivable — 80,439
Other assets 143,548 139,890
Total assets $ 14,535,556 $ 12,697,246
LIABILITIES AND STOCKHOLDERS’ EQUITY
Current liabilities:    
Trade payables $ 113,538 $ 88,024
Accrued expenses 993,773 739,630
Income taxes payable 14,196 38,362
Deferred revenue 2,405,950 1,945,619
Total current liabilities 3,527,457 2,811,635
Long-term liabilities:
Debt and capital lease obligations 1,881,421 1,892,200
Deferred revenue 88,592 69,131
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 20.4 (NO CITATION)
- **Claim:** Operating cash flow ratio = 2,912,853 / 3,527,457 = 0.8258...
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 20.5 (NO CITATION)
- **Claim:** **FY2017 operating cash flow ratio = 0.83** (rounded to two decimal places).
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 21. `financebench_id_00917` (AMD)
- **Question:** What drove operating margin change as of the FY22 for AMD? If operating margin is not a useful metric for a company like this, then please state that and explain why.
- **Predicted Answer:**

> Based on the provided excerpts, operating margin is a useful metric here, and the filing directly explains the change:
> 
> - Operating income for 2022 was $1.3 billion compared to $3.6 billion for 2021 [1]. The decrease in operating income was primarily driven by amortization of intangible assets associated with the Xilinx acquisition [1].
> - Gross margin as a percentage of net revenue was 45% in 2022 versus 48% in 2021, with the decrease primarily due to amortization of intangible assets associated with the Xilinx acquisition [1].
> - Segment-level operating income (loss) for 2022 vs. 2021: Data Center $1,848M vs. $991M; Client $1,190M vs. $2,088M; Gaming $953M vs. $934M; Embedded $2,252M vs. $44M; All Other $(4,979)M vs. $(409)M; Total operating income $1,264M vs. $3,648M [5].
> 
> Note: The excerpts do not explicitly state an "operating margin" percentage figure; they provide operating income dollars and gross margin percentages only [1][5].

### Pair 21.1 (NO CITATION)
- **Claim:** Based on the provided excerpts, operating margin is a useful metric here, and the filing directly explains the change:
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 21.2 ([1] AMD_2022_10K FY2022 p.42)
- **Claim:** Operating income for 2022 was $1.3 billion compared to $3.6 billion for 2021 [1].
- **Cited Chunk Text:**
```text
driven by a weak PC market and significant inventory correction actions across the PC supply chain. Gross margin, as a percentage of net revenue for 2022,
was 45%, compared to 48% in 2021. The decrease in gross margin was primarily due to amortization of intangible assets associated with the Xilinx acquisition.
Operating income for 2022 was $1.3 billion compared to operating income of $3.6 billion for 2021. The decrease in operating income was primarily driven by
amortization of intangible assets associated with the Xilinx acquisition. Net income for 2022 was $1.3 billion compared to $3.2 billion in the prior year. The
decrease in net income was primarily driven by lower operating income.
Cash, cash equivalents and short-term investments as of December 31, 2022 were $5.9 billion, compared to $3.6 billion at the end of 2021. Our aggregate
principal amount of total debt as of December 31, 2022 was $2.5 billion, compared to $313 million as of December 25, 2021.
We took several actions in 2022 to strengthen our financial position. In June 2022, we issued $1.0 billion in aggregate principal amount of senior notes,
consisting of $500 million in aggregate principal amount of 3.924% Senior Notes due 2032 (3.924% Notes) and $500 million in aggregate principal amount of
4.393% Senior Notes due 2052 (4.393% Notes). The 3.924% Notes will mature on June 1, 2032 and bear interest at a rate of 3.924% per annum, and the
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 21.3 ([1] AMD_2022_10K FY2022 p.42)
- **Claim:** The decrease in operating income was primarily driven by amortization of intangible assets associated with the Xilinx acquisition [1].
- **Cited Chunk Text:**
```text
driven by a weak PC market and significant inventory correction actions across the PC supply chain. Gross margin, as a percentage of net revenue for 2022,
was 45%, compared to 48% in 2021. The decrease in gross margin was primarily due to amortization of intangible assets associated with the Xilinx acquisition.
Operating income for 2022 was $1.3 billion compared to operating income of $3.6 billion for 2021. The decrease in operating income was primarily driven by
amortization of intangible assets associated with the Xilinx acquisition. Net income for 2022 was $1.3 billion compared to $3.2 billion in the prior year. The
decrease in net income was primarily driven by lower operating income.
Cash, cash equivalents and short-term investments as of December 31, 2022 were $5.9 billion, compared to $3.6 billion at the end of 2021. Our aggregate
principal amount of total debt as of December 31, 2022 was $2.5 billion, compared to $313 million as of December 25, 2021.
We took several actions in 2022 to strengthen our financial position. In June 2022, we issued $1.0 billion in aggregate principal amount of senior notes,
consisting of $500 million in aggregate principal amount of 3.924% Senior Notes due 2032 (3.924% Notes) and $500 million in aggregate principal amount of
4.393% Senior Notes due 2052 (4.393% Notes). The 3.924% Notes will mature on June 1, 2032 and bear interest at a rate of 3.924% per annum, and the
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 21.4 ([1] AMD_2022_10K FY2022 p.42)
- **Claim:** Gross margin as a percentage of net revenue was 45% in 2022 versus 48% in 2021, with the decrease primarily due to amortization of intangible assets associated with the Xilinx acquisition [1].
- **Cited Chunk Text:**
```text
driven by a weak PC market and significant inventory correction actions across the PC supply chain. Gross margin, as a percentage of net revenue for 2022,
was 45%, compared to 48% in 2021. The decrease in gross margin was primarily due to amortization of intangible assets associated with the Xilinx acquisition.
Operating income for 2022 was $1.3 billion compared to operating income of $3.6 billion for 2021. The decrease in operating income was primarily driven by
amortization of intangible assets associated with the Xilinx acquisition. Net income for 2022 was $1.3 billion compared to $3.2 billion in the prior year. The
decrease in net income was primarily driven by lower operating income.
Cash, cash equivalents and short-term investments as of December 31, 2022 were $5.9 billion, compared to $3.6 billion at the end of 2021. Our aggregate
principal amount of total debt as of December 31, 2022 was $2.5 billion, compared to $313 million as of December 25, 2021.
We took several actions in 2022 to strengthen our financial position. In June 2022, we issued $1.0 billion in aggregate principal amount of senior notes,
consisting of $500 million in aggregate principal amount of 3.924% Senior Notes due 2032 (3.924% Notes) and $500 million in aggregate principal amount of
4.393% Senior Notes due 2052 (4.393% Notes). The 3.924% Notes will mature on June 1, 2032 and bear interest at a rate of 3.924% per annum, and the
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 21.5 ([5] AMD_2022_10K FY2022 p.47)
- **Claim:** Segment-level operating income (loss) for 2022 vs. 2021: Data Center $1,848M vs. $991M; Client $1,190M vs. $2,088M; Gaming $953M vs. $934M; Embedded $2,252M vs. $44M; All Other $(4,979)M vs. $(409)M; Total operating income $1,264M vs. $3,648M [5].
- **Cited Chunk Text:**
```text
Table of Contents
Results of Operations
During the second quarter of fiscal year 2022, we changed our reporting segments to align our financial reporting with how we manage our business in strategic
end markets. This is consistent with how our Chief Operating Decision Maker (CODM) assesses our financial performance and allocates resources. As a result,
we report our financial performance based on the following four reportable segments: Data Center, Client, Gaming, and Embedded.
Additional information on our reportable segments is contained in Note 4 – Segment Reporting of the Notes to Financial Statements (Part II, Item 8 of this Form
10-K).
Our operating results tend to vary seasonally. Historically, our net revenue has been generally higher in the second half of the year than in the first half of the
year, although market conditions and product transitions could impact these trends.
The following table provides a summary of net revenue and operating income (loss) by segment for 2022 and 2021:
Year Ended
December 31,
2022
December 25,
2021
(In millions)
Net revenue:
Data Center $ 6,043 $ 3,694 
Client 6,201 6,887 
Gaming 6,805 5,607 
Embedded 4,552 246 
Total net revenue $ 23,601 $ 16,434 
Operating income (loss):
Data Center $ 1,848 $ 991 
Client 1,190 2,088 
Gaming 953 934 
Embedded 2,252 44 
All Other (4,979) (409)
Total operating income (loss) $ 1,264 $ 3,648 
Data Center
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 21.6 ([1] AMD_2022_10K FY2022 p.42)
- **Claim:** Note: The excerpts do not explicitly state an "operating margin" percentage figure; they provide operating income dollars and gross margin percentages only [1][5].
- **Cited Chunk Text:**
```text
driven by a weak PC market and significant inventory correction actions across the PC supply chain. Gross margin, as a percentage of net revenue for 2022,
was 45%, compared to 48% in 2021. The decrease in gross margin was primarily due to amortization of intangible assets associated with the Xilinx acquisition.
Operating income for 2022 was $1.3 billion compared to operating income of $3.6 billion for 2021. The decrease in operating income was primarily driven by
amortization of intangible assets associated with the Xilinx acquisition. Net income for 2022 was $1.3 billion compared to $3.2 billion in the prior year. The
decrease in net income was primarily driven by lower operating income.
Cash, cash equivalents and short-term investments as of December 31, 2022 were $5.9 billion, compared to $3.6 billion at the end of 2021. Our aggregate
principal amount of total debt as of December 31, 2022 was $2.5 billion, compared to $313 million as of December 25, 2021.
We took several actions in 2022 to strengthen our financial position. In June 2022, we issued $1.0 billion in aggregate principal amount of senior notes,
consisting of $500 million in aggregate principal amount of 3.924% Senior Notes due 2032 (3.924% Notes) and $500 million in aggregate principal amount of
4.393% Senior Notes due 2052 (4.393% Notes). The 3.924% Notes will mature on June 1, 2032 and bear interest at a rate of 3.924% per annum, and the
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 21.7 ([5] AMD_2022_10K FY2022 p.47)
- **Claim:** Note: The excerpts do not explicitly state an "operating margin" percentage figure; they provide operating income dollars and gross margin percentages only [1][5].
- **Cited Chunk Text:**
```text
Table of Contents
Results of Operations
During the second quarter of fiscal year 2022, we changed our reporting segments to align our financial reporting with how we manage our business in strategic
end markets. This is consistent with how our Chief Operating Decision Maker (CODM) assesses our financial performance and allocates resources. As a result,
we report our financial performance based on the following four reportable segments: Data Center, Client, Gaming, and Embedded.
Additional information on our reportable segments is contained in Note 4 – Segment Reporting of the Notes to Financial Statements (Part II, Item 8 of this Form
10-K).
Our operating results tend to vary seasonally. Historically, our net revenue has been generally higher in the second half of the year than in the first half of the
year, although market conditions and product transitions could impact these trends.
The following table provides a summary of net revenue and operating income (loss) by segment for 2022 and 2021:
Year Ended
December 31,
2022
December 25,
2021
(In millions)
Net revenue:
Data Center $ 6,043 $ 3,694 
Client 6,201 6,887 
Gaming 6,805 5,607 
Embedded 4,552 246 
Total net revenue $ 23,601 $ 16,434 
Operating income (loss):
Data Center $ 1,848 $ 991 
Client 1,190 2,088 
Gaming 953 934 
Embedded 2,252 44 
All Other (4,979) (409)
Total operating income (loss) $ 1,264 $ 3,648 
Data Center
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 22. `financebench_id_01346` (Corning)
- **Question:** How much has the effective tax rate of Corning changed between FY2021 and FY2022?
- **Predicted Answer:**

> The effective tax rate was 22.9% in FY2022 and 20.2% in FY2021, an increase of 2.7 percentage points [5]. This is consistent with the rounded figures of 23% in FY2022 versus 20% in FY2021 shown in the segment table [8].

### Pair 22.1 ([5] CORNING_2022_10K FY2022 p.76)
- **Claim:** The effective tax rate was 22.9% in FY2022 and 20.2% in FY2021, an increase of 2.7 percentage points [5].
- **Cited Chunk Text:**
```text
2022  2021  2020 
Statutory U.S. federal income tax rate   21.0%  21.0%  21.0%
State income tax, net of federal effect   0.7   1.0   1.4 
Audit settlements & change in reserve   3.7   1.6   12.1 
Differential arising from foreign earnings (1)   2.2   2.0   14.9 
Valuation allowance   2.1   (0.5)   2.5 
Intercompany loan adjustment   0.6       6.1 
Tax credits   (3.3)   (2.6)   (29.2)
Foreign derived intangible income   (2.7)   (1.3)     
Stock compensation   (0.8)   (1.5)   (1.7)
Remeasurement of deferred tax assets and liabilities   (0.1)       (13.2)
Legal entity rationalization           (2.2)
Non-deductible expenses       1.4   6.9 
Global intangible low-taxed income       0.2   (0.5)
Other items, net   (0.5)   (1.1)   (0.6)
Effective tax rate   22.9%  20.2%  17.5%
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 22.2 ([8] CORNING_2022_10K FY2022 p.23)
- **Claim:** This is consistent with the rounded figures of 23% in FY2022 versus 20% in FY2021 shown in the segment table [8].
- **Cited Chunk Text:**
```text
Year ended December 31,   % change  
  2022   2021   22 vs. 21  
             
Net sales  $ 14,189  $ 14,082   1%
             
Gross margin  $ 4,506  $ 5,063   (11%)
(gross margin %)   32%  36%    
             
Selling, general and administrative expenses  $ 1,898  $ 1,827   4%
(as a % of net sales)   13%  13%    
             
Research, development and engineering expenses  $ 1,047  $ 995   5%
(as a % of net sales)   7%  7%    
             
Translated earnings contract gain, net  $ 351  $ 354   (1%)
(as a % of net sales)   2%  3%    
             
Income before income taxes  $ 1,797  $ 2,426   (26%)
(as a % of net sales)   13%  17%    
             
Provision for income taxes  $ (411)  $ (491)   16%
Effective tax rate   23%  20%    
             
Net income attributable to Corning Incorporated  $ 1,316  $ 1,906   (31%)
(as a % of net sales)   9%   14%    
             
Comprehensive income attributable to Corning Incorporated  $ 661  $ 1,471   (55%)
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 23. `financebench_id_04854` (General Mills)
- **Question:** According to the information provided in the statement of cash flows, what is the FY2020 free cash flow (FCF) for General Mills? FCF here is defined as: (cash from operations - capex). Answer in USD millions.
- **Predicted Answer:**

> Based on the provided excerpts, FY2020 free cash flow is **$3,215.4 million**.
> 
> This is calculated as net cash provided by operating activities of $3,676.2 million minus purchases of land, buildings, and equipment of $460.8 million, which the filing explicitly reconciles to free cash flow of $3,215.4 million [5]. The same $3,215.4 million free cash flow figure is also reported in the selected financial data [3], and the filing notes free cash flow was $3.2 billion at a conversion rate of 143 percent of adjusted net earnings [2].

### Pair 23.1 (NO CITATION)
- **Claim:** Based on the provided excerpts, FY2020 free cash flow is **$3,215.4 million**.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 23.2 ([5] GENERALMILLS_2020_10K FY2020 p.36)
- **Claim:** This is calculated as net cash provided by operating activities of $3,676.2 million minus purchases of land, buildings, and equipment of $460.8 million, which the filing explicitly reconciles to free cash flow of $3,215.4 million [5].
- **Cited Chunk Text:**
```text
Product recall, net of tax (d) 17.1 
CPW restructuring costs, net of tax (e) 5.0 
Investment activity, net, net of tax (f) 3.0 
Adjusted net earnings, including earnings attributable to redeemable and noncontrolling interests $2,241.8 
  
Net cash provided by operating activities 3,676.2 
Purchases of land, buildings, and equipment (460.8) 
Free cash flow $3,215.4 
  
Net cash provided by operating activities conversion rate 166% 
Free cash flow conversion rate 143% 
Note: Table may not foot due rounding. 
(a) Discrete tax benefit related to the reorganization of certain wholly owned subsidiaries. Please see Note 15 to the Consolidated Financial Statements 
in Item 8 of this report. 
(b) Restructuring and project-related charges for previously announced restructuring actions. Please see Note 4 to the Consolidated Financial 
Statements in Item 8 of this report.  
(c) Net mark-to-market valuation of certain commodity positions recognized in unallocated corporate items. Please see Note 8 to the Consolidated 
Financial Statements in Item 8 of this report.  
(d) Product recall costs related to our international Green Giant business. 
(e) CPW restructuring charges related to initiatives designed to improve profitability and growth that were approved in fiscal 2018 and 2019. 
(f) Valuation adjustments and the loss on sale of certain corporate investments. 
 
See our reconciliation below of the effective income tax rate as reported to the adjusted effective income tax rate for the tax impact of 
each item affecting comparability. 
 
Constant-currency After-Tax Earnings from Joint Ventures Growth Rate 
 
We believe that this measure provides useful information to investors because it provides transparency to underlying performance of 
our joint ventures by excluding the effect that foreign currency exchange rate fluctuations have on year-to-year comparability given 
volatility in foreign currency exchange markets. 
 
After-tax earnings from joint ventures growth rates on a constant-currency basis are calculated as follows: 
 
  Fiscal 2020
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 23.3 ([3] GENERALMILLS_2020_10K FY2020 p.16)
- **Claim:** The same $3,215.4 million free cash flow figure is also reported in the selected financial data [3], and the filing notes free cash flow was $3.2 billion at a conversion rate of 143 percent of adjusted net earnings [2].
- **Cited Chunk Text:**
```text
Capital expenditures 460.8 537.6 622.7 684.4 729.3 
Free cash flow (b) 3,215.4 2,269.4 2,218.3 1,730.8 2,034.9 
Share data:      
Cash dividends per common share $ 1.96 $ 1.96 $ 1.96 $ 1.92 $ 1.78 
(a) Fiscal 2020 was a 53-week year; all other fiscal years were 52 weeks. 
(b) See “Glossary” in Item 8 of this report for definition. 
(c) See “Non-GAAP Measures” in Item 7 of this report for our discussion of this measure not defined by generally accepted accounting 
principles. 
(d) In fiscal 2019, we retrospectively adopted new accounting requirements related to the presentation of net periodic defined benefit 
pension expense, net periodic postretirement benefit expense, and net periodic postemployment benefit expense. Please see Note 2 
to the Consolidated Financial Statements in Item 8 of this report. 
(e) In fiscal 2018, we adopted new requirements for the accounting and presentation of stock-based payments. This resulted in the 
reclassification of realized windfall tax benefits and employee tax withholdings in our Consolidated Statements of Cash Flows. 
Please see Note 2 to the Consolidated Financial Statements in Item 8 of this report.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 23.4 ([2] GENERALMILLS_2020_10K FY2020 p.17)
- **Claim:** The same $3,215.4 million free cash flow figure is also reported in the selected financial data [3], and the filing notes free cash flow was $3.2 billion at a conversion rate of 143 percent of adjusted net earnings [2].
- **Cited Chunk Text:**
```text
increased 12 percent on a constant-currency basis (See the “Non-GAAP Measures” section below for a description of our use of measures 
not defined by generally accepted accounting principles (GAAP)). 
 
Net cash provided by operations totaled $3.7 billion in fiscal 2020 representing a conversion rate of 166 percent of net earnings, including 
earnings attributable to redeemable and noncontrolling interests. This cash generation supported capital investments totaling $461 
million, and our resulting free cash flow was $3.2 billion at a conversion rate of 143 percent of adjusted net earnings, including earnings
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 24. `financebench_id_01351` (American Express)
- **Question:** How much has the effective tax rate of American Express changed between FY2021 and FY2022?
- **Predicted Answer:**

> The effective tax rate was 21.6 percent in 2022 and 24.6 percent in 2021, a decrease of 3.0 percentage points [1].

### Pair 24.1 ([1] AMERICANEXPRESS_2022_10K FY2022 p.48)
- **Claim:** The effective tax rate was 21.6 percent in 2022 and 24.6 percent in 2021, a decrease of 3.0 percentage points [1].
- **Cited Chunk Text:**
```text
volumes.
Card Member services expense increased, primarily due to higher usage of travel-related benefits.
Marketing expense increased, primarily due to business investments to drive growth momentum and accelerate new card acquisitions.
Salaries and employee benefits expense increased, primarily driven by higher compensation costs, reflecting an increase in our colleague base to support
business growth as well as compensation decisions made.
Other expenses increased, primarily driven by net losses on Amex Ventures investments in the current year, as compared to net gains in the prior year.
INCOME TAXES
The effective tax rate was 21.6 percent and 24.6 percent for 2022 and 2021, respectively. The reduction in the effective tax rate primarily reflected discrete tax
benefits in the current year related to the resolution of prior-year tax items. The tax rates in both years reflected the level of pretax income in relation to
recurring permanent tax benefits and the geographic mix of business.
46
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 25. `financebench_id_01482` (PepsiCo)
- **Question:** At the Pepsico AGM held on May 3, 2023, what was the outcome of the shareholder vote on the shareholder proposal for a congruency report by Pepsico on net-zero emissions policies?
- **Predicted Answer:**

> The shareholder proposal regarding a congruency report on net-zero emissions policies was defeated, with 19,718,780 votes for, 977,228,788 votes against, 23,200,321 abstentions, and 172,969,325 broker non-votes [2].

### Pair 25.1 ([2] PEPSICO_2023_8K_dated-2023-05-05 FY2023 p.3)
- **Claim:** The shareholder proposal regarding a congruency report on net-zero emissions policies was defeated, with 19,718,780 votes for, 977,228,788 votes against, 23,200,321 abstentions, and 172,969,325 broker non-votes [2].
- **Cited Chunk Text:**
```text
(4) The shareholders approved, on an advisory basis, the holding of an advisory vote on the compensation of PepsiCo’s named executive officers every
year:
One Year 994,856,204
Two Years 4,331,004
Three Years 17,603,165
Abstain 3,357,516
Broker Non-Votes 172,969,325
In light of the voting results on this advisory vote, and consistent with its recommendation to shareholders, PepsiCo’s Board of Directors has decided that
PepsiCo will hold an advisory vote on the compensation of PepsiCo’s named executive officers every year.
(5) The shareholder proposal regarding independent Board Chair was defeated:
For 250,838,697
Against 746,982,272
Abstain 22,326,920
Broker Non-Votes 172,969,325
(6) The shareholder proposal regarding a global transparency report was defeated:
For 185,034,699
Against 814,416,953
Abstain 20,696,237
Broker Non-Votes 172,969,325
(7) The shareholder proposal regarding a report on impacts of reproductive healthcare legislation was defeated:
For 158,917,578
Against 830,627,354
Abstain 30,602,957
Broker Non-Votes 172,969,325
(8) The shareholder proposal regarding a congruency report on net-zero emissions policies was defeated:
For 19,718,780
Against 977,228,788
Abstain 23,200,321
Broker Non-Votes 172,969,325
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 26. `financebench_id_04254` (American Water Works)
- **Question:** Basing your judgments off of the cash flow statement and the income statement, what is American Water Works's FY2021 unadjusted operating income + depreciation and amortization from the cash flow statement (unadjusted EBITDA) in USD millions?
- **Predicted Answer:**

> Based on the provided excerpts:
> 
> - FY2021 operating income was $1,196 million [3].
> - FY2021 depreciation and amortization from the cash flow statement was $636 million [1].
> 
> Unadjusted EBITDA = $1,196 + $636 = **$1,832 million**.
> 
> (Note: The excerpts do not explicitly label this figure as "unadjusted EBITDA"; the calculation is derived from the two stated line items.)

### Pair 26.1 ([3] AMERICANWATERWORKS_2021_10K FY2021 p.85)
- **Claim:** FY2021 operating income was $1,196 million [3].
- **Cited Chunk Text:**
```text
Table of Contents
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Statements of Operations
(In millions, except pe
r share data) 
For the Years Ended December 31,  
2021 2020 2019 Operating revenues
$ 3,930 $ 3,777 $ 3,610 Operating expenses:
   Operation and maintenance
1,777 1,622 1,544 Depreciation and amortization
636 604 582 General taxes
321 303 280 Other
— — (10) Total operating expenses, net
2,734 2,529 2,396 Operating income
1,196 1,248 1,214 Other income (expense):
   Interest expense
(403) (397) (386) Interest income
4 2 4 Non-operating benefit costs, n
et78 49 16 Gain or (loss) on sale of businesses
747 — (44) Other, net
18 22 29 Total other income (exp
ense)444 (324) (381) Income before income taxes
1,640 924 833 Provision for income taxes
377 215 212 Net income attributab
le to common shareholders$ 1,263 $ 709 $ 621 Basic earnings per share: 
(a)       Net income attributab
le to common shareholders$ 6.96 $ 3.91 $ 3.44 Diluted earnings per share
: (a)       Net income attributab
le to common shareholders$ 6.95 $ 3.91 $ 3.43 Weighted average com
mon shares outstanding:   Basic
182 181 181 Diluted
182 182 181 (a)
Amounts may not calculate due to rounding. The accompanying notes are 
an integral part of these Consolidated Financial Statements.84
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 26.2 ([1] AMERICANWATERWORKS_2021_10K FY2021 p.87)
- **Claim:** FY2021 depreciation and amortization from the cash flow statement was $636 million [1].
- **Cited Chunk Text:**
```text
Table of Contents
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Statements of Cash Flows
(In millions)
 
For the Years Ended December 31,  
2021 2020 2019 CASH FLOWS FROM OPERATING ACTIVITIES
   Net income
$ 1,263 $ 709 $ 621 Adjustments to reconcile to net cash flows provided by operating activities:
   Depreciation and amortization
636 604 582 Deferred income taxes and amortization of investment tax credits
230 207 208 Provision for losses on accounts receivable
37 34 28 (Gain) or loss on sale of businesses
(747) — 34 Pension and non-pension postretirement benefits
(41) (14) 17 Other non-cash, net
(23) (20) (41) Changes in assets and liabilities:
   Receivables and unbilled revenues
(74) (97) (25) Pension and non-pension postretirement benefit contributions
(40) (39) (31) Accounts payable and accrued liabilities
66 (2) 66 Other assets and liabilities, net
134 44 (76) Net cash provided by operating activities
1,441 1,426 1,383 CASH FLOWS FROM INVESTING ACTIVITIES
   Capital expenditures
(1,764) (1,822) (1,654) Acquisitions, net of cash acquired
(135) (135) (235) Proceeds from sale of assets, net of cash on hand
472 2 48 Removal costs from property, plant and equipment retirements, net
(109) (106) (104) Net cash used in investing activities
(1,536) (2,061) (1,945) CASH FLOWS FROM FINANCING ACTIVITIES
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 26.3 (NO CITATION)
- **Claim:** Unadjusted EBITDA = $1,196 + $636 = **$1,832 million**.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 26.4 (NO CITATION)
- **Claim:** (Note: The excerpts do not explicitly label this figure as "unadjusted EBITDA"; the calculation is derived from the two stated line items.)
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 27. `financebench_id_00540` (AES Corporation)
- **Question:** Roughly how many times has AES Corporation sold its inventory in FY2022? Calculate inventory turnover ratio for the FY2022; if conventional inventory management is not meaningful for the company then state that and explain why.
- **Predicted Answer:**

> Based on the provided excerpts, I cannot calculate a conventional inventory turnover ratio for FY2022.
> 
> **What the excerpts do provide:**
> - Total inventory of $1,055 million as of December 31, 2022, and $604 million as of December 31, 2021 [3].
> - Total cost of sales of $10,069 million for FY2022 [9].
> 
> **What is missing:**
> - The excerpts do not explicitly state an inventory turnover ratio or a "cost of goods sold" figure labeled as such (only "Total cost of sales" is given) [9], and they do not provide enough information to determine whether conventional inventory turnover is meaningful for AES.
> 
> **Why a conventional calculation is not meaningful here (per the excerpts):**
> - AES's inventory consists primarily of fuel and other raw materials used to generate power, plus operational spare parts and supplies used to maintain power generation and distribution facilities [1]. This is not a typical merchandising/retail inventory that is "sold" to customers; fuel is consumed to generate electricity, and spare parts are consumed in maintenance. The filing notes that spare parts and supplies carrying amounts are typically reduced only when items are considered obsolete [1], which is inconsistent with a conventional "sell-through" turnover concept.
> 
> Because the excerpts do not explicitly provide an inventory turnover figure or confirm that conventional inventory management applies, I cannot state a turnover multiple based solely on the provided context.

### Pair 27.1 (NO CITATION)
- **Claim:** Based on the provided excerpts, I cannot calculate a conventional inventory turnover ratio for FY2022.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.2 (NO CITATION)
- **Claim:** **What the excerpts do provide:**
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.3 ([3] AES_2022_10K FY2022 p.148)
- **Claim:** Total inventory of $1,055 million as of December 31, 2022, and $604 million as of December 31, 2021 [3].
- **Cited Chunk Text:**
```text
2. INVENTORY
Inventory is valued primarily using the average-cost method. The following table summarizes the Company's inventory balances as of the
dates indicated (in millions):
December 31, 2022 2021
Fuel and other raw materials $ 733 $ 366 
Spare parts and supplies 322 238 
Total $ 1,055 $ 604 
3. PROPERTY, PLANT AND EQUIPMENT
The following table summarizes the components of the electric generation and distribution assets and other property, plant and equipment
(in millions) with their estimated useful lives (in years). The amounts are stated net of all prior asset impairment losses recognized.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.4 ([9] AES_2022_10K FY2022 p.131)
- **Claim:** Total cost of sales of $10,069 million for FY2022 [9].
- **Cited Chunk Text:**
```text
129    
Consolidated Statements of Operations
Years ended December 31, 2022, 2021, and 2020
2022 2021 2020
(in millions, except per share amounts)
Revenue:
Regulated $ 3,538 $ 2,868 $ 2,661 
Non-Regulated 9,079 8,273 6,999 
Total revenue 12,617 11,141 9,660 
Cost of Sales:
Regulated (3,162) (2,448) (2,235)
Non-Regulated (6,907) (5,982) (4,732)
Total cost of sales (10,069) (8,430) (6,967)
Operating margin 2,548 2,711 2,693 
General and administrative expenses (207) (166) (165)
Interest expense (1,117) (911) (1,038)
Interest income 389 298 268 
Loss on extinguishment of debt (15) (78) (186)
Other expense (68) (60) (53)
Other income 102 410 75 
Loss on disposal and sale of business interests (9) (1,683) (95)
Goodwill impairment expense (777) — — 
Asset impairment expense (763) (1,575) (864)
Foreign currency transaction gains (losses) (77) (10) 55 
Other non-operating expense (175) — (202)
INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE TAXES AND EQUITY IN EARNINGS OF AFFILIATES (169) (1,064) 488 
Income tax benefit (expense) (265) 133 (216)
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.5 ([9] AES_2022_10K FY2022 p.131)
- **Claim:** The excerpts do not explicitly state an inventory turnover ratio or a "cost of goods sold" figure labeled as such (only "Total cost of sales" is given) [9], and they do not provide enough information to determine whether conventional inventory turnover is meaningful for AES.
- **Cited Chunk Text:**
```text
129    
Consolidated Statements of Operations
Years ended December 31, 2022, 2021, and 2020
2022 2021 2020
(in millions, except per share amounts)
Revenue:
Regulated $ 3,538 $ 2,868 $ 2,661 
Non-Regulated 9,079 8,273 6,999 
Total revenue 12,617 11,141 9,660 
Cost of Sales:
Regulated (3,162) (2,448) (2,235)
Non-Regulated (6,907) (5,982) (4,732)
Total cost of sales (10,069) (8,430) (6,967)
Operating margin 2,548 2,711 2,693 
General and administrative expenses (207) (166) (165)
Interest expense (1,117) (911) (1,038)
Interest income 389 298 268 
Loss on extinguishment of debt (15) (78) (186)
Other expense (68) (60) (53)
Other income 102 410 75 
Loss on disposal and sale of business interests (9) (1,683) (95)
Goodwill impairment expense (777) — — 
Asset impairment expense (763) (1,575) (864)
Foreign currency transaction gains (losses) (77) (10) 55 
Other non-operating expense (175) — (202)
INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE TAXES AND EQUITY IN EARNINGS OF AFFILIATES (169) (1,064) 488 
Income tax benefit (expense) (265) 133 (216)
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.6 (NO CITATION)
- **Claim:** **Why a conventional calculation is not meaningful here (per the excerpts):**
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.7 ([1] AES_2022_10K FY2022 p.139)
- **Claim:** AES's inventory consists primarily of fuel and other raw materials used to generate power, plus operational spare parts and supplies used to maintain power generation and distribution facilities [1].
- **Cited Chunk Text:**
```text
income. Interest and dividends on investments are reported in Interest income and Other income, respectively. Gains and losses on sales of
investments are determined using the specific identification method.
ACCOUNTS AND NOTES RECEIVABLE AND ALLOWANCE FOR DOUBTFUL ACCOUNTS — Accounts and notes receivable are
carried at amortized cost. The Company periodically assesses the collectability of accounts receivable, considering factors such as historical
collection experience, the age of accounts receivable and other currently available evidence supporting collectability, and records an allowance
for doubtful accounts in accordance with ASC 326 for the estimated uncollectible amount as appropriate. Credit losses on accounts and notes
receivable are generally recognized in Cost of Sales. Certain of our businesses charge interest on accounts receivable. Interest income is
recognized on an accrual basis. When collection of such interest is not reasonably assured, interest income is recognized as cash is received.
Individual accounts and notes receivable are written off when they are no longer deemed collectible.
INVENTORY — Inventory primarily consists of fuel and other raw materials used to generate power, and operational spare parts and
supplies used to maintain power generation and distribution facilities. Inventory is carried at lower of cost or net realizable value. Cost is the sum
of the purchase price and expenditures incurred to bring the inventory to its existing location. Inventory is primarily valued using the average cost
method. Generally, if it is expected fuel inventory will not be recovered through revenue earned from power generation, an impairment is
recognized to reflect the fuel at net realizable value. The carrying amount of spare parts and supplies is typically reduced only in instances where
the items are considered obsolete.
LONG-LIVED ASSETS — Long-lived assets include property, plant and equipment, assets under finance leases and intangible assets
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.8 (NO CITATION)
- **Claim:** This is not a typical merchandising/retail inventory that is "sold" to customers; fuel is consumed to generate electricity, and spare parts are consumed in maintenance.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.9 ([1] AES_2022_10K FY2022 p.139)
- **Claim:** The filing notes that spare parts and supplies carrying amounts are typically reduced only when items are considered obsolete [1], which is inconsistent with a conventional "sell-through" turnover concept.
- **Cited Chunk Text:**
```text
income. Interest and dividends on investments are reported in Interest income and Other income, respectively. Gains and losses on sales of
investments are determined using the specific identification method.
ACCOUNTS AND NOTES RECEIVABLE AND ALLOWANCE FOR DOUBTFUL ACCOUNTS — Accounts and notes receivable are
carried at amortized cost. The Company periodically assesses the collectability of accounts receivable, considering factors such as historical
collection experience, the age of accounts receivable and other currently available evidence supporting collectability, and records an allowance
for doubtful accounts in accordance with ASC 326 for the estimated uncollectible amount as appropriate. Credit losses on accounts and notes
receivable are generally recognized in Cost of Sales. Certain of our businesses charge interest on accounts receivable. Interest income is
recognized on an accrual basis. When collection of such interest is not reasonably assured, interest income is recognized as cash is received.
Individual accounts and notes receivable are written off when they are no longer deemed collectible.
INVENTORY — Inventory primarily consists of fuel and other raw materials used to generate power, and operational spare parts and
supplies used to maintain power generation and distribution facilities. Inventory is carried at lower of cost or net realizable value. Cost is the sum
of the purchase price and expenditures incurred to bring the inventory to its existing location. Inventory is primarily valued using the average cost
method. Generally, if it is expected fuel inventory will not be recovered through revenue earned from power generation, an impairment is
recognized to reflect the fuel at net realizable value. The carrying amount of spare parts and supplies is typically reduced only in instances where
the items are considered obsolete.
LONG-LIVED ASSETS — Long-lived assets include property, plant and equipment, assets under finance leases and intangible assets
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 27.10 (NO CITATION)
- **Claim:** Because the excerpts do not explicitly provide an inventory turnover figure or confirm that conventional inventory management applies, I cannot state a turnover multiple based solely on the provided context.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 28. `financebench_id_08135` (Amazon)
- **Question:** What is Amazon's year-over-year change in revenue from FY2016 to FY2017 (in units of percents and round to one decimal place)? Calculate what was asked by utilizing the line items clearly shown in the statement of income.
- **Predicted Answer:**

> Based on the consolidated statements of operations [6], total net sales were $135,987 million in FY2016 and $177,866 million in FY2017.
> 
> Year-over-year change = ($177,866 − $135,987) / $135,987 = $41,879 / $135,987 ≈ 30.8%.
> 
> Amazon's year-over-year revenue change from FY2016 to FY2017 was approximately **30.8%** [6].

### Pair 28.1 ([6] AMAZON_2017_10K FY2017 p.37)
- **Claim:** Based on the consolidated statements of operations [6], total net sales were $135,987 million in FY2016 and $177,866 million in FY2017.
- **Cited Chunk Text:**
```text
Table of Contents
AMAZON.COM, INC.
CONSOLIDATED STATEMENTS OF
 OPERATIONS(in millions, except per share data)
 
  
 Year Ended December 31,  
2015  2016  2017 Net product sales
$ 79,268  $ 94,665  $ 118,573 Net service sales
27,738  41,322  59,293 Total net sales
107,006  135,987  177,866 Operating expenses:
     Cost of sales
71,651  88,265  111,934 Fulfillment
13,410  17,619  25,249 Marketing
5,254  7,233  10,069 Technology and content
12,540  16,085  22,620 General and administrative
1,747  2,432  3,674 Other operating expense, net
171  167  214 Total operating expenses
104,773  131,801  173,760 Operating income
2,233  4,186  4,106 Interest income
50  100  202 Interest expense
(459 )  (484 )  (848 ) Other income (expense), net
(256 )  90  346 Total non-operating incom
e (expense)(665 )  (294 )  (300 ) Income before income taxes
1,568  3,892  3,806 Provision for income taxes
(950 )  (1,425 )  (769 ) Equity-method investment 
activity, net of tax(22 )  (96 )  (4 ) Net income
$ 596  $ 2,371  $ 3,033 Basic earnings per share
$ 1.28  $ 5.01  $ 6.32 Diluted earnings per share
$ 1.25  $ 4.90  $ 6.15 Weighted-average sha
res used in computation of earnings per share:     Basic
467  474  480 Diluted
477  484  493 See accompanying notes to consol
idated financial statements.38
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 28.2 (NO CITATION)
- **Claim:** Year-over-year change = ($177,866 − $135,987) / $135,987 = $41,879 / $135,987 ≈ 30.8%.
- **Cited Chunk Text:**
```text
[NO CITATION EMITTED FOR CLAIM]
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 28.3 ([6] AMAZON_2017_10K FY2017 p.37)
- **Claim:** Amazon's year-over-year revenue change from FY2016 to FY2017 was approximately **30.8%** [6].
- **Cited Chunk Text:**
```text
Table of Contents
AMAZON.COM, INC.
CONSOLIDATED STATEMENTS OF
 OPERATIONS(in millions, except per share data)
 
  
 Year Ended December 31,  
2015  2016  2017 Net product sales
$ 79,268  $ 94,665  $ 118,573 Net service sales
27,738  41,322  59,293 Total net sales
107,006  135,987  177,866 Operating expenses:
     Cost of sales
71,651  88,265  111,934 Fulfillment
13,410  17,619  25,249 Marketing
5,254  7,233  10,069 Technology and content
12,540  16,085  22,620 General and administrative
1,747  2,432  3,674 Other operating expense, net
171  167  214 Total operating expenses
104,773  131,801  173,760 Operating income
2,233  4,186  4,106 Interest income
50  100  202 Interest expense
(459 )  (484 )  (848 ) Other income (expense), net
(256 )  90  346 Total non-operating incom
e (expense)(665 )  (294 )  (300 ) Income before income taxes
1,568  3,892  3,806 Provision for income taxes
(950 )  (1,425 )  (769 ) Equity-method investment 
activity, net of tax(22 )  (96 )  (4 ) Net income
$ 596  $ 2,371  $ 3,033 Basic earnings per share
$ 1.28  $ 5.01  $ 6.32 Diluted earnings per share
$ 1.25  $ 4.90  $ 6.15 Weighted-average sha
res used in computation of earnings per share:     Basic
467  474  480 Diluted
477  484  493 See accompanying notes to consol
idated financial statements.38
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 29. `financebench_id_01474` (PepsiCo)
- **Question:** As of FY2023Q1, why did Pepsico raise full year guidance for FY2023?
- **Predicted Answer:**

> PepsiCo raised its full-year FY2023 guidance because of its strong start to the year and business momentum, with categories and geographies remaining resilient during the first quarter [1]. Specifically, the company now expects full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and core constant currency EPS to increase 9 percent (previously 8 percent) [1][2].

### Pair 29.1 ([1] PEPSICO_2023Q1_EARNINGS FY2023 p.0)
- **Claim:** PepsiCo raised its full-year FY2023 guidance because of its strong start to the year and business momentum, with categories and geographies remaining resilient during the first quarter [1].
- **Cited Chunk Text:**
```text
PepsiCo Reports First-Quarter 2023 Results; Raises Full-Year 
Guidance
Reported (GAAP) First-Quarter 2023 Results
First-Quarter
Net revenue growth 10.2%
Foreign exchange impact on net revenue (2.5)%
Earnings per share (EPS) $1.40
EPS change (54)%
Foreign exchange impact on EPS (2)%
Organic/Core (non-GAAP)1 First-Quarter 2023 Results
First-Quarter
Organic revenue growth 14.3%
Core EPS $1.50
Core constant currency EPS change 18%
PURCHASE, N.Y. - April 25, 2023 - PepsiCo, Inc. (NASDAQ: PEP) today reported results for 
the first quarter 2023. 
“We are very pleased with our performance and business momentum as our categories and 
geographies remained resilient during the first quarter. Given our strong start to the year, we 
now expect our full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and 
core constant currency EPS to increase 9 percent (previously 8 percent),” said Chairman and 
CEO Ramon Laguarta.
Laguarta continued, “Our results demonstrate that the investments we have made to become an 
even Faster, even Stronger, and even Better organization by Winning with pep+ are laying the 
foundation for durable and sustainable growth. We remain committed to our strategic agenda 
and will continue to invest in our people, brands, supply chain, go-to-market systems, and 
digitization initiatives to build competitive advantages and win in the marketplace.”
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 29.2 ([1] PEPSICO_2023Q1_EARNINGS FY2023 p.0)
- **Claim:** Specifically, the company now expects full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and core constant currency EPS to increase 9 percent (previously 8 percent) [1][2].
- **Cited Chunk Text:**
```text
PepsiCo Reports First-Quarter 2023 Results; Raises Full-Year 
Guidance
Reported (GAAP) First-Quarter 2023 Results
First-Quarter
Net revenue growth 10.2%
Foreign exchange impact on net revenue (2.5)%
Earnings per share (EPS) $1.40
EPS change (54)%
Foreign exchange impact on EPS (2)%
Organic/Core (non-GAAP)1 First-Quarter 2023 Results
First-Quarter
Organic revenue growth 14.3%
Core EPS $1.50
Core constant currency EPS change 18%
PURCHASE, N.Y. - April 25, 2023 - PepsiCo, Inc. (NASDAQ: PEP) today reported results for 
the first quarter 2023. 
“We are very pleased with our performance and business momentum as our categories and 
geographies remained resilient during the first quarter. Given our strong start to the year, we 
now expect our full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and 
core constant currency EPS to increase 9 percent (previously 8 percent),” said Chairman and 
CEO Ramon Laguarta.
Laguarta continued, “Our results demonstrate that the investments we have made to become an 
even Faster, even Stronger, and even Better organization by Winning with pep+ are laying the 
foundation for durable and sustainable growth. We remain committed to our strategic agenda 
and will continue to invest in our people, brands, supply chain, go-to-market systems, and 
digitization initiatives to build competitive advantages and win in the marketplace.”
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

### Pair 29.3 ([2] PEPSICO_2023Q1_EARNINGS FY2023 p.2)
- **Claim:** Specifically, the company now expects full-year 2023 organic revenue to increase 8 percent (previously 6 percent) and core constant currency EPS to increase 9 percent (previously 8 percent) [1][2].
- **Cited Chunk Text:**
```text
Guidance and Outlook
The Company provides guidance on a non-GAAP basis as we cannot predict certain elements which are 
included in reported GAAP results, including the impact of foreign exchange translation and commodity 
mark-to-market net impacts. 
For fiscal year 2023, the Company now expects to deliver 8 percent organic revenue growth (previously 6 
percent), and 9 percent core constant currency EPS growth (previously 8 percent).
Consistent with its previous guidance for 2023, the Company continues to expect:
• A core annual effective tax rate of 20 percent; and
• Total cash returns to shareholders of approximately $7.7 billion, comprised of dividends of $6.7 
billion and share repurchases of $1.0 billion.
In addition, the Company continues to expect an approximate 2-percentage-point foreign exchange 
translation headwind to impact reported net revenue and core EPS growth based on current market 
consensus rates.
This assumption and the guidance above imply 2023 core EPS of $7.27 (previously $7.20), a 7 percent 
increase (previously 6 percent) compared to 2022 core EPS of $6.79.
Prepared Management Remarks and Live Question and Answer Webcast
At approximately 6:30 a.m. (Eastern time) on April 25, 2023, the Company will post prepared 
management remarks (in pdf format) of its first quarter 2023 results and business update, including its 
outlook for 2023, at www.pepsico.com/investors. At 8:15 a.m. (Eastern time) on April 25, 2023, the 
Company will host a live question and answer session with investors and financial analysts. Further 
details will be accessible on the Company’s website at www.pepsico.com/investors.
Contacts: Investor Relations Communications
investor@pepsico.com pepsicomediarelations@pepsico.com
3
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________

## 30. `financebench_id_01490` (Johnson & Johnson)
- **Question:** What is the amount of the gain accruing to JnJ as a result of the separation of its Consumer Health business segment, as of August 30, 2023?
- **Predicted Answer:**

> The gain accruing to Johnson & Johnson as a result of the Consumer Health (Kenvue) separation is approximately **$20 billion**, recognized in the third quarter of 2023 [2].

### Pair 30.1 ([2] JOHNSON_JOHNSON_2023_8K_dated-2023-08-30 FY2023 p.3)
- **Claim:** The gain accruing to Johnson & Johnson as a result of the Consumer Health (Kenvue) separation is approximately **$20 billion**, recognized in the third quarter of 2023 [2].
- **Cited Chunk Text:**
```text
“The completion of this transaction uniquely positions Johnson & Johnson as a Pharmaceutical and MedTech company focused on delivering
transformative healthcare solutions to patients,” said Joaquin Duato, Chairman of the Board and Chief Executive Officer. “We are incredibly
proud of the focus and dedication of our employees worldwide to achieve this milestone, which we are confident will unlock near- and long-
term value for all of our stakeholders.”
As previously announced, the Company recently completed an exchange offer to finalize the separation of Kenvue Inc., formerly Johnson &
Johnson’s Consumer Health business. As a result of the completion of the exchange offer, Johnson & Johnson will now present its
Consumer Health business financial results as discontinued operations, including a gain of approximately $20 billion in the third quarter of
2023.
```
- **Support Check:** `[ ] Supported`  `[ ] Partial`  `[ ] Unsupported`  Notes: ______________
