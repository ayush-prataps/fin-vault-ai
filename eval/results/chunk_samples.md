# Verbatim Table-Heavy Chunk Samples

5 table chunks from retrieval HITS and 5 table chunks from retrieval MISSES alongside ground truth evidence.

---

## Section 1: 5 Table Chunks from Pages That Were HIT

### Hit Sample 1: Adobe (ADOBE_2015_10K, Page 62)
- **Question ID:** `financebench_id_04735`
- **Question:** You are an investment banker and your only resource(s) to answer the following question is (are): the statement of financial position and the cash flow statement. Here's the question: what is the FY2015 operating cash flow ratio for Adobe? Operating cash flow ratio is defined as: cash from operations / total current liabilities. Round your answer to two decimal places.

#### Stored Chunk Text (Verbatim):
```text
63 adobe systems incorporated consolidated statements of cash flows ( in thousands ) years ended november 27, 2015 november 28, 2014 november 29, 2013 cash flows from operating activities : net income..................................................................................................................... $ 629, 551 $ 268, 395 $ 289, 985 adjustments to reconcile net income to net cash provided by operating activities : depreciation, amortization and accretion................................................................. 339, 473 313, 590 321, 227 stock - based compensation....................................................................................... 335, 859 333, 701 328, 987 deferred income taxes..........................
```

#### Gold Evidence Text (Verbatim):
```text
59
 ADOBE SYSTEMS INCORPORATED
 CONSOLIDATED BALANCE SHEETS
(In thousands, except par value)
 
November 27,
2015
November 28,
2014
ASSETS
Current assets:
 
 
Cash and cash equivalents.................................................................................................................... $
876,560
$
1,117,400
Short-term investments ........................................................................................................................
3,111,524
2,622,091
Trade receivables, net of allowances for doubtful accounts of $7,293 and $7,867, respectively........
672,006
591,800
Deferred income taxes..........................................................................................................................

95,279
Prepaid expenses and other current assets ...........................................................................................
161,802
175,758
Total current assets..........................................................................................................................
4,821,892
4,602,328
Property and equipment, net...................................................................................................................
787,421
785,123
Goodwill .................................................................................................................................................
5,366,881
4,721,962
Purchased and other intangibles, net.......................................................................................................
510,007
469,662
Investment in lease receivable................................................................................................................
80,439
80,439
Other assets.............................................................................................................................................
159,832
126,315
Total assets...................................................................................................................................... $
11,726,472
$
10,785,829
LIABILITIES AND STOCKHOLDERS EQUITY
Current liabilities:
 
 
Trade payables...................................................................................................................................... $
93,307
$
68,377
Accrued expenses.................................................................................................................................
678,364
683,866
Debt and capital lease obligations........................................................................................................

603,229
Accrued restructuring...........................................................................................................................
1,520
17,120
Income taxes payable...........................................................................................................................
6,165
23,920
Deferred revenue..................................................................................................................................
1,434,200
1,097,923
Total current liabilities....................................................................................................................
2,213,556
2,494,435
Long-term liabilities:
 
 
Debt and capital lease obligations........................................................................................................
1,907,231
911,086
Deferred revenue..................................................................................................................................
51,094
57,401
Accrued restructuring...........................................................................................................................
3,214
5,194
Income taxes payable...........................................................................................................................
256,129
125,746
Deferred income taxes..........................................................................................................................
208,209
342,315
Other liabilities.....................................................................................................................................
85,459
73,747
Total liabilities................................................................................................................................
4,724,892
4,009,924
Commitments and contingencies
Stockholders equity:
 
 
Preferred stock, $0.0001 par value; 2,000 shares authorized; none issued..........................................


Common stock, $0.0001 par value; 900,000 shares authorized; 600,834 shares issued; 
 497,809 and 497,484 shares outstanding, respectively......................................................................
61
61
Additional paid-in-capital ....................................................................................................................
4,184,883
3,778,495
Retained earnings.................................................................................................................................
7,253,431
6,924,294
Accumulated other comprehensive income (loss) ...............................................................................
(169,080)
(8,094)
Treasury stock, at cost (103,025 and 103,350 shares, respectively), net of reissuances......................
(4,267,715)
(3,918,851)
Total stockholders equity...............................................................................................................
7,001,580
6,775,905
Total liabilities and stockholders equity........................................................................................ $
11,726,472
$
10,785,829
See accompanying Notes to Consolidated Financial Statements.
```

---

### Hit Sample 2: Adobe (ADOBE_2017_10K, Page 60)
- **Question ID:** `financebench_id_03856`
- **Question:** What is the FY2017 operating cash flow ratio for Adobe? Operating cash flow ratio is defined as: cash from operations / total current liabilities. Round your answer to two decimal places. Please utilize information provided primarily within the balance sheet and the cash flow statement.

#### Stored Chunk Text (Verbatim):
```text
table of contents 61 adobe systems incorporated consolidated statements of cash flows ( in thousands ) years ended december 1, 2017 december 2, 2016 november 27, 2015 cash flows from operating activities : net income $ 1, 693, 954 $ 1, 168, 782 $ 629, 551 adjustments to reconcile net income to net cash provided by operating activities : depreciation, amortization and accretion 325, 997 331, 535 339, 473 stock - based compensation 451, 451 349, 912 335, 859 deferred income taxes 51, 605 24, 222 ( 69, 657 ) gain on the sale of property — — ( 21, 415 ) unrealized ( gains ) losses on investments ( 5, 494 ) 3, 145 ( 9, 210 ) excess tax benefits from stock - based compensation — ( 75, 105 ) ( 68, 153 ) other non - cash items 4, 625 2, 022 1, 216 changes in operating assets and liabilities, net of acquired assets and assumed liabilities : trade receivables, net ( 187, 173 ) ( 160, 416 ) ( 79, 502 ) prepaid expenses and other current assets 28, 040 ( 71, 021 ) ( 7, 701 ) trade payables ( 45, 186 ) ( 6, 281 ) 22, 870 accrued expenses 154, 125 64, 978 ( 22, 564 ) income taxes payable ( 34, 493 ) 43, 115 97, 934 deferred revenue 475, 402 524, 840 320, 801 net cash provided by operating activities 2, 912, 853 2, 199, 728 1, 469, 502 cash flows from investing activities : purchases of short - term investments ( 1, 931, 011 ) ( 2, 285, 222 ) ( 2, 064, 833 ) maturities of short - term investments 759,
```

#### Gold Evidence Text (Verbatim):
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
 
 
Cash and cash equivalents
$
2,306,072
$
1,011,315
Short-term investments
3,513,702
3,749,985
Trade receivables, net of allowances for doubtful accounts of $9,151 and $6,214, respectively
1,217,968
833,033
Prepaid expenses and other current assets
210,071
245,441
Total current assets
7,247,813
5,839,774
Property and equipment, net
936,976
816,264
Goodwill
5,821,561
5,406,474
Purchased and other intangibles, net
385,658
414,405
Investment in lease receivable

80,439
Other assets
143,548
139,890
Total assets
$
14,535,556
$
12,697,246
LIABILITIES AND STOCKHOLDERS EQUITY
Current liabilities:
 
 
Trade payables
$
113,538
$
88,024
Accrued expenses
993,773
739,630
Income taxes payable
14,196
38,362
Deferred revenue
2,405,950
1,945,619
Total current liabilities
3,527,457
2,811,635
Long-term liabilities:
Debt and capital lease obligations
1,881,421
1,892,200
Deferred revenue
88,592
69,131
Income taxes payable
173,088
184,381
Deferred income taxes
279,941
217,660
Other liabilities
125,188
97,404
Total liabilities
6,075,687
5,272,411
Commitments and contingencies
Stockholders equity:
 
 
Preferred stock, $0.0001 par value; 2,000 shares authorized; none issued


Common stock, $0.0001 par value; 900,000 shares authorized; 600,834 shares issued; 
 491,262 and 494,254 shares outstanding, respectively
61
61
Additional paid-in-capital
5,082,195
4,616,331
Retained earnings
9,573,870
8,114,517
Accumulated other comprehensive income (loss)
(111,821)
(173,602)
Treasury stock, at cost (109,572 and 106,580 shares, respectively), net of reissuances
(6,084,436)
(5,132,472)
Total stockholders equity
8,459,869
7,424,835
Total liabilities and stockholders equity
$
14,535,556
$
12,697,246
See accompanying Notes to Consolidated Financial Statements.
```

---

### Hit Sample 3: AMD (AMD_2022_10K, Page 42)
- **Question ID:** `financebench_id_01198`
- **Question:** What drove revenue change as of the FY22 for AMD?

#### Stored Chunk Text (Verbatim):
```text
table of contents item 7. management ’ s discussion and analysis of financial condition and results of operations the following discussion should be read in conjunction with the consolidated financial statements as of december 31, 2022 and december 25, 2021 and for each of the three years in the period ended december 31, 2022 and related notes, which are included in this annual report on form 10 - k as well as with the other sections of this annual report on form 10 - k, “ part ii, item 8 : financial statements and supplementary data. ” introduction in this section, we will describe the general financial condition and the results of operations of advanced micro devices, inc. and its wholly - owned subsidiaries ( collectively, “ us, ” “ our ” or “ amd ” ), including a discussion of our results of operations for 2022 compared to 2021, an analysis of changes in our financial condition and a discussion of our off - balance sheet arrangements. discussions of 2020 items and year - to - year comparisons between 2021 and 2020 that are not included in this form 10 - k can be found in “ management ’ s discussion and analysis of financial condition and results of operations ” in part ii, item 7 of our annual report on form 10 - k for the fiscal year ended december 25, 2021. overview 2022 was a transformative year for amd as we took several major steps that scaled and reshaped our business. in february 2022, we completed our strategic acquisition of xilinx, inc. ( xilinx ) which expanded our technology and product portfolio to include adaptable hardware platforms that enable hardware acceleration and rapid innovation across a variety of technologies and established amd in multiple embedded markets where we have traditionally not had a significant presence. we now offer field programmable gate arrays ( fpgas ), adaptive socs, and adaptive compute acceleration platform ( acap ) products. with the acquisition of xilinx, we have access to a new set of markets and customers, further strengthening and
```

#### Gold Evidence Text (Verbatim):
```text
Net
revenue for 2022 was $23.6 billion, an increase of 44% compared to 2021 net revenue of $16.4 billion. The increase in net revenue was driven by a 64%
increase in Data Center segment revenue primarily due to higher sales of our EPYC server processors, a 21% increase in Gaming segment revenue
primarily due to higher semi-custom product sales, and a significant increase in Embedded segment revenue from the prior year period driven by the inclusion
of Xilinx embedded product sales.
```

---

### Hit Sample 4: American Express (AMERICANEXPRESS_2022_10K, Page 0)
- **Question ID:** `financebench_id_00476`
- **Question:** Which debt securities are registered to trade on a national securities exchange under American Express' name as of 2022?

#### Stored Chunk Text (Verbatim):
```text
UNITED STATES
SECURITIES AND EXCHANGE COMMISSION
Washington, D.C. 20549
Form 10-K
☑ ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934
For the fiscal year ended December 31, 2022
OR
☐ TRANSITION REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934
For the transition period from            to    
         Commission File No. 1-7657
American Express Company
(Exact name of registrant as specified in its charter)
New York 13-4922250
(State or other jurisdiction of incorporation or organization) (I.R.S. Employer Identification No.)
200 Vesey Street
New York, New York 10285
(Address of principal executive offices) (Zip Code)
Registrant’s telephone number, including area code: (212) 640-2000
Securities registered pursuant to Section 12(b) of the Act:
Title of each class Trading Symbol(s) Name of each exchange on which registered
Common Shares (par value $0.20 per Share) AXP New York Stock Exchange
Securities registered pursuant to section 12(g) of the Act: None
Indicate by check mark if the registrant is a well-known seasoned issuer, as defined in Rule 405 of the Securities Act.    Yes  þ    No   o
Indicate by check mark if the registrant is not required to file reports pursuant to Section 13 or Section 15(d) of the Act.    Yes  o    No  þ
Indicate by check mark whether the registrant (1) has filed all reports required to be filed by Section 13 or 15(d) of the Securities Exchange Act of 1934 during the preceding 12 months (or
for such shorter period that the registrant was required to file such reports) and (2) has been subject to such filing requirements for the past 90 days.    Yes  þ    No  o
```

#### Gold Evidence Text (Verbatim):
```text
Registrants telephone number, including area code: (212) 640-2000
Securities registered pursuant to Section 12(b) of the Act:
Title of each class
Trading Symbol(s)
Name of each exchange on which registered
Common Shares (par value $0.20 per Share)
AXP
New York Stock Exchange
Securities registered pursuant to section 12(g) of the Act: None
```

---

### Hit Sample 5: American Water Works (AMERICANWATERWORKS_2020_10K, Page 85)
- **Question ID:** `financebench_id_05718`
- **Question:** How much (in USD billions) did American Water Works pay out in cash dividends for FY2020? Compute or extract the answer by primarily using the details outlined in the statement of cash flows.

#### Stored Chunk Text (Verbatim):
```text
table of contents american water works company, inc. and subsidiary companies consolidated statements of cash flows ( in millions ) for the years ended december 31, 2020 2019 2018 cash flows from operating activities net income $ 709 $ 621 $ 565 adjustments to reconcile to net cash flows provided by operating activities : depreciation and amortization 604 582 545 deferred income taxes and amortization of investment tax credits 207 208 195 provision for losses on accounts receivable 34 28 33 loss ( gain ) on asset dispositions and purchases — 34 ( 20 ) impairment charge — — 57 pension and non - pension postretirement benefits ( 14 ) 17 23 other non - cash, net ( 20 ) ( 41 ) 20 changes in assets and liabilities : receivables and unbilled revenues ( 97 ) ( 25 ) ( 17 ) pension and non - pension postretirement benefit contributions ( 39 ) ( 31 ) ( 22 ) accounts payable and accrued liabilities ( 2 ) 66 25 other assets and liabilities, net 44 ( 72 ) 22 impact of freedom industries settlement activities — ( 4 ) ( 40 ) net cash provided by operating activities 1, 426 1, 383 1, 386 cash flows from investing activities capital expenditures ( 1, 822 ) ( 1, 654 ) ( 1, 586 ) acquisitions, net of cash acquired ( 135 ) ( 235 ) ( 398 ) proceeds from sale of assets 2 48 35 removal costs from property, plant and equipment retirements, net ( 106 ) ( 104 ) ( 87 ) net cash used in investing activities ( 2, 061 ) ( 1, 945 ) ( 2, 036 ) cash flows from financing activities proceeds from long - term debt 1, 334 1, 530 1, 358 repayments of long - term debt ( 342 ) ( 495 ) ( 526 ) proceeds from term loan 500 — — net short - term borrowings with maturities less than
```

#### Gold Evidence Text (Verbatim):
```text
Table of Contents
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Statements of Cash Flows
(In millions)
 
For the Years Ended December 31,
 
2020
2019
2018
CASH FLOWS FROM OPERATING ACTIVITIES
 
 
 
Net income
$
709 
$
621 
$
565 
Adjustments to reconcile to net cash flows provided by operating activities:
 
 
 
Depreciation and amortization
604 
582 
545 
Deferred income taxes and amortization of investment tax credits
207 
208 
195 
Provision for losses on accounts receivable
34 
28 
33 
Loss (gain) on asset dispositions and purchases
 
34 
(20)
Impairment charge
 
 
57 
Pension and non-pension postretirement benefits
(14)
17 
23 
Other non-cash, net
(20)
(41)
20 
Changes in assets and liabilities:
 
 
 
Receivables and unbilled revenues
(97)
(25)
(17)
Pension and non-pension postretirement benefit contributions
(39)
(31)
(22)
Accounts payable and accrued liabilities
(2)
66 
25 
Other assets and liabilities, net
44 
(72)
22 
Impact of Freedom Industries settlement activities
 
(4)
(40)
Net cash provided by operating activities
1,426 
1,383 
1,386 
CASH FLOWS FROM INVESTING ACTIVITIES
 
 
 
Capital expenditures
(1,822)
(1,654)
(1,586)
Acquisitions, net of cash acquired
(135)
(235)
(398)
Proceeds from sale of assets
2 
48 
35 
Removal costs from property, plant and equipment retirements, net
(106)
(104)
(87)
Net cash used in investing activities
(2,061)
(1,945)
(2,036)
CASH FLOWS FROM FINANCING ACTIVITIES
 
 
 
Proceeds from long-term debt
1,334 
1,530 
1,358 
Repayments of long-term debt
(342)
(495)
(526)
Proceeds from term loan
500 
 
 
Net short-term borrowings with maturities less than three months
(5)
(178)
60 
Issuance of common stock
 
 
183 
Proceeds from issuances of employee stock plans and direct stock purchase plan, net of taxes paid of $17, $11
and $8 in 2020, 2019 and 2018, respectively
9 
15 
16 
Advances and contributions in aid of construction, net of refunds of $24, $30 and $22 in 2020, 2019
and 2018, respectively
28 
26 
21 
Debt issuance costs and make-whole premium on early debt redemption
(15)
(15)
(22)
Dividends paid
(389)
(353)
(319)
Anti-dilutive share repurchases
 
(36)
(45)
Net cash provided by financing activities
1,120 
494 
726 
Net increase (decrease) in cash, cash equivalents and restricted funds
485 
(68)
76 
Cash, cash equivalents and restricted funds at beginning of period
91 
159 
83 
Cash, cash equivalents and restricted funds at end of period
$
576 
$
91 
$
159 
Cash paid during the year for:
 
 
 
Interest, net of capitalized amount
$
382 
$
383 
$
332 
Income taxes, net of refunds of $2, $4 and $0 in 2020, 2019 and 2018, respectively
$
7 
$
12 
$
38 
Non-cash investing activity:
 
 
 
Capital expenditures acquired on account but unpaid as of year end
$
221 
$
235 
$
181 
The accompanying notes are an integral part of these Consolidated Financial Statements.
84
```

---

## Section 2: 5 Table Chunks from Pages That Were MISSED

### Miss Sample 1: 3M (3M_2018_10K, Target Page 85)
- **Question ID:** `financebench_id_04672`
- **Question:** Assume that you are a public equities analyst. Answer the following question by primarily using information that is shown in the balance sheet: what is the year end FY2018 net PPNE for 3M? Answer in USD billions.

#### Top Retrieved Chunk Text (Page 70) (Verbatim):
```text
4, 337 3, 916 421 net debt ( non - gaap measure ) $ 11, 650 $ 12, 023 $ ( 373 ) refer to the preceding total debt and cash, cash equivalents and marketable securities sections for additional details. balance sheet : 3m ’ s strong balance sheet and liquidity provide the company with significant flexibility to fund its numerous opportunities going forward. the company will continue to invest in its operations to drive growth, including continual review of acquisition opportunities. the company uses working capital measures that place emphasis and focus on certain working capital assets, such as accounts receivable and inventory activity. working capital ( non - gaap measure ) : ( millions ) june 30, 2023 december 31, 2022 change current assets $ 15, 754 $ 14, 688
```

#### Gold Evidence Text (Target Page) (Verbatim):
```text
Table of Contents 
3M Company and Subsidiaries
Consolidated Balance Shee t
At December 31
 
 
 
December 31,
 
December 31,
 
(Dollars in millions, except per share amount)
 
2018
 
2017
 
Assets
 
 
 
 
 
Current assets
 
 
 
 
 
Cash and cash equivalents
 
$
2,853 
$
3,053 
Marketable securities current
 
 
380 
 
1,076 
Accounts receivable net of allowances of $95 and $103
 
 
5,020 
 
4,911 
Inventories
 
 
 
 
 
Finished goods
 
 
2,120 
 
1,915 
Work in process
 
 
1,292 
 
1,218 
Raw materials and supplies
 
 
954 
 
901 
Total inventories
 
 
4,366 
 
4,034 
Prepaids
 
 
741 
 
937 
Other current assets
 
 
349 
 
266 
Total current assets
 
 
13,709 
 
14,277 
Property, plant and equipment
 
 
24,873 
 
24,914 
Less: Accumulated depreciation
 
 
(16,135) 
 
(16,048) 
Property, plant and equipment net
 
 
8,738 
 
8,866 
Goodwill
 
 
10,051 
 
10,513 
Intangible assets net
 
 
2,657 
 
2,936 
Other assets
 
 
1,345 
 
1,395 
Total assets
 
$
36,500 
$
37,987 
Liabilities
 
 
 
 
 
Current liabilities
 
 
 
 
 
Short-term borrowings and current portion of long-term debt
 
$
1,211 
$
1,853 
Accounts payable
 
 
2,266 
 
1,945 
Accrued payroll
 
 
749 
 
870 
Accrued income taxes
 
 
243 
 
310 
Other current liabilities
 
 
2,775 
 
2,709 
Total current liabilities
 
 
7,244 
 
7,687 
 
 
 
 
 
 
Long-term debt
 
 
13,411 
 
12,096 
Pension and postretirement benefits
 
 
2,987 
 
3,620 
Other liabilities
 
 
3,010 
 
2,962 
Total liabilities
 
$
26,652 
$
26,365 
Commitments and contingencies (Note 16)
 
 
 
 
 
Equity
 
 
 
 
 
3M Company shareholders equity:
 
 
 
 
 
Common stock par value, $.01 par value
 
$
 9 
$
 9 
Shares outstanding - 2018: 576,575,168
 
 
 
 
 
Shares outstanding - 2017: 594,884,237
 
 
 
 
 
Additional paid-in capital
 
 
5,643 
 
5,352 
Retained earnings
 
 
40,636 
 
39,115 
Treasury stock
 
 
(29,626) 
 
(25,887) 
Accumulated other comprehensive income (loss)
 
 
(6,866) 
 
(7,026) 
Total 3M Company shareholders equity
 
 
9,796 
 
11,563 
Noncontrolling interest
 
 
52 
 
59 
Total equity
 
$
9,848 
$
11,622 
Total liabilities and equity
 
$
36,500 
$
37,987 
 
The accompanying Notes to Consolidated Financial Statements are an integral part of this statement.
58
```

---

### Miss Sample 2: 3M (3M_2022_10K, Target Page 85)
- **Question ID:** `financebench_id_01226`
- **Question:** What drove operating margin change as of FY2022 for 3M? If operating margin is not a useful metric for a company like this, then please state that and explain why.

#### Top Retrieved Chunk Text (Page 67) (Verbatim):
```text
##2. business segment operating income margins decreased year - on - year due to due to manufacturing and supply chain headwinds, inflation impacts, investments in the business and restructuring costs partially offset by benefits from aggressive spending discipline, pricing and productivity actions. 68
```

#### Gold Evidence Text (Target Page) (Verbatim):
```text
SG&A, measured as a percent of sales, increased in 2022 when compared to the same period last year. SG&A was impacted by increased special item costs for significant
litigation primarily related to steps toward resolving Combat Arms Earplugs litigation (discussed in Note 16) resulting in a 2022 second quarter pre-tax charge of approximately
$1.2 billion, certain impairment costs related to exiting PFAS manufacturing (see Note 15), costs related to exiting Russia (see Note 15), divestiture-related restructuring
charges (see Note 5), and continued investment in key growth initiatives. These increases were partially offset by restructuring benefits and ongoing general 3M cost
management.
```

---

### Miss Sample 3: 3M (3M_2023Q2_10Q, Target Page 85)
- **Question ID:** `financebench_id_00807`
- **Question:** Does 3M have a reasonably healthy liquidity profile based on its quick ratio for Q2 of FY2023? If the quick ratio is not relevant to measure liquidity, please state that and explain why.

#### Top Retrieved Chunk Text (Page 69) (Verbatim):
```text
table of contents financial condition and liquidity the strength and stability of 3m ’ s business model and strong free cash flow capability, together with proven capital markets access, provide financial flexibility to deploy capital in accordance with the company ' s stated priorities and meet needs associated with contractual commitments and other obligations. investing in 3m ’ s business to drive organic growth and deliver strong returns on invested capital remains the first priority for capital deployment. this includes research and development, capital expenditures, and commercialization capability. the company also continues to actively manage its portfolio through acquisitions and divestitures to maximize value for shareholders. 3m expects to continue returning cash to shareholders through dividends and share repurchases. to fund cash needs in the united states, the company relies on ongoing cash flow from u. s. operations, access to capital markets and repatriation of the earnings of its foreign affiliates that are not considered to be permanently reinvested. for those international earnings still considered to be reinvested indefinitely, the company currently has no plans or intentions to repatriate these funds for u. s. operations. see note 10 in 3m ' s 2022 annual report on form 10 - k for further information on earnings considered to be reinvested indefinitely. 3m maintains a strong liquidity profile. the company ’ s primary short - term liquidity needs are met through cash on hand and u. s. commercial paper issuances. 3m believes it will have continuous access to the commercial paper market. 3m ’ s commercial paper program permits the company to have a maximum of $ 5 billion outstanding with a maximum maturity of 397 days from date of issuance. the company had $ 1. 8 billion in commercial paper outstanding at june 30, 2023, compared to no commercial paper outstanding as of december 31, 2022. total debt : the strength of 3m ’ s credit profile and significant ongoing cash flows provide 3m proven access to capital markets. additionally, the company
```

#### Gold Evidence Text (Target Page) (Verbatim):
```text
3M Company and Subsidiaries
Consolidated Balance Sheet
(Unaudited)
(Dollars in millions, except per share amount)
June 30, 2023
December 31, 2022
Assets
Current assets
Cash and cash equivalents
$
4,258 
$
3,655 
Marketable securities current
56 
238 
Accounts receivable net of allowances of $160 and $174
4,947 
4,532 
Inventories
Finished goods
2,526 
2,497 
Work in process
1,527 
1,606 
Raw materials and supplies
1,227 
1,269 
Total inventories
5,280 
5,372 
Prepaids
674 
435 
Other current assets
539 
456 
Total current assets
15,754 
14,688 
Property, plant and equipment
26,459 
25,998 
Less: Accumulated depreciation
(17,248)
(16,820)
Property, plant and equipment net
9,211 
9,178 
Operating lease right of use assets
812 
829 
Goodwill
12,869 
12,790 
Intangible assets net
4,470 
4,699 
Other assets
5,764 
4,271 
Total assets
$
48,880 
$
46,455 
Liabilities
Current liabilities
Short-term borrowings and current portion of long-term debt
$
3,033 
$
1,938 
Accounts payable
3,231 
3,183 
Accrued payroll
785 
692 
Accrued income taxes
172 
259 
Operating lease liabilities current
244 
261 
Other current liabilities
3,471 
3,190 
Total current liabilities
10,936 
9,523
```

---

### Miss Sample 4: Activision Blizzard (ACTIVISIONBLIZZARD_2019_10K, Target Page 85)
- **Question ID:** `financebench_id_02987`
- **Question:** What is the FY2019 fixed asset turnover ratio for Activision Blizzard? Fixed asset turnover ratio is defined as: FY2019 revenue / (average PP&E between FY2018 and FY2019). Round your answer to two decimal places. Base your judgments on the information provided primarily in the statement of income and the statement of financial position.

#### Top Retrieved Chunk Text (Page None) (Verbatim):
```text

```

#### Gold Evidence Text (Target Page) (Verbatim):
```text
Table of Contents
ACTIVISION BLIZZARD, INC. AND SUBSIDIARIES
CONSOLIDATED BALANCE SHEETS
(Amounts in millions, except share data)
 
At December 31, 2019
 
At December 31, 2018
Assets
 
 
Current assets:
 
 
Cash and cash equivalents
$
5,794
 $
4,225
Accounts receivable, net of allowances of $132 and $190, at December 31, 2019 and December 31, 2018, respectively
848
 
1,035
Inventories, net
32
 
43
Software development
322
 
264
Other current assets
296
 
539
Total current assets
7,292
 
6,106
Software development
54
 
65
Property and equipment, net
253
 
282
Deferred income taxes, net
1,293
 
458
Other assets
658
 
482
Intangible assets, net
531
 
735
Goodwill
9,764
 
9,762
Total assets
$
19,845
 $
17,890
 
 
 
Liabilities and Shareholders Equity
 
 
Current liabilities:
 
 
Accounts payable
$
292
 $
253
Deferred revenues
1,375
 
1,493
Accrued expenses and other liabilities
1,248
 
896
Total current liabilities
2,915
 
2,642
Long-term debt, net
2,675
 
2,671
Deferred income taxes, net
505
 
18
Other liabilities
945
 
1,167
Total liabilities
7,040
 
6,498
Commitments and contingencies (Note 23)
 
Shareholders equity:
 
 
 
Common stock, $0.000001 par value, 2,400,000,000 shares authorized, 1,197,436,644 and 1,192,093,991 shares issued at
December 31, 2019 and December 31, 2018, respectively

 

Additional paid-in capital
11,174
 
10,963
Less: Treasury stock, at cost, 428,676,471 shares at December 31, 2019 and December 31, 2018
(5,563) 
(5,563)
Retained earnings
7,813
 
6,593
Accumulated other comprehensive loss
(619) 
(601)
Total shareholders equity
12,805
 
11,392
Total liabilities and shareholders equity
$
19,845
 $
17,890
The accompanying notes are an integral part of these Consolidated Financial Statements.
F-4
```

---

### Miss Sample 5: AES Corporation (AES_2022_10K, Target Page 85)
- **Question ID:** `financebench_id_01319`
- **Question:** What is the quantity of restructuring costs directly outlined in AES Corporation's income statements for FY2022? If restructuring costs are not explicitly outlined then state 0.

#### Top Retrieved Chunk Text (Page None) (Verbatim):
```text

```

#### Gold Evidence Text (Target Page) (Verbatim):
```text
Consolidated Statements of Operations
Years ended December 31, 2022, 2021, and 2020
2022
2021
2020
(in millions, except per share amounts)
Revenue:
Regulated
$
3,538 
$
2,868 
$
2,661 
Non-Regulated
9,079 
8,273 
6,999 
Total revenue
12,617 
11,141 
9,660 
Cost of Sales:
Regulated
(3,162)
(2,448)
(2,235)
Non-Regulated
(6,907)
(5,982)
(4,732)
Total cost of sales
(10,069)
(8,430)
(6,967)
Operating margin
2,548 
2,711 
2,693 
General and administrative expenses
(207)
(166)
(165)
Interest expense
(1,117)
(911)
(1,038)
Interest income
389 
298 
268 
Loss on extinguishment of debt
(15)
(78)
(186)
Other expense
(68)
(60)
(53)
Other income
102 
410 
75 
Loss on disposal and sale of business interests
(9)
(1,683)
(95)
Goodwill impairment expense
(777)
 
 
Asset impairment expense
(763)
(1,575)
(864)
Foreign currency transaction gains (losses)
(77)
(10)
55 
Other non-operating expense
(175)
 
(202)
INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE TAXES AND EQUITY IN EARNINGS OF AFFILIATES
(169)
(1,064)
488 
Income tax benefit (expense)
(265)
133 
(216)
Net equity in losses of affiliates
(71)
(24)
(123)
INCOME (LOSS) FROM CONTINUING OPERATIONS
(505)
(955)
149 
Gain from disposal of discontinued businesses, net of income tax expense of $0, $1, and $0, respectively
 
4 
3 
NET INCOME (LOSS)
(505)
(951)
152 
Less: Net loss (income) attributable to noncontrolling interests and redeemable stock of subsidiaries
(41)
542 
(106)
NET INCOME (LOSS) ATTRIBUTABLE TO THE AES CORPORATION
$
(546)
$
(409)
$
46
```

---

