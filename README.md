# Real Estate Investment Guide for Foreign Investors
![REP Diagram](https://raw.githubusercontent.com/ntran0429/REP/main/images/REP_Diagram.png)



## Table of Contents

* [Problem Statement](#problem-statement)
* [Context](#context)
  * [Investor's Requirements](#investors-requirements)
  * [Business Question](#business-question)
  * [Frame the Business Problem into a Data Question](#frame-the-business-problem-into-a-data-question)
  * [Components to Answer the Question](#components-to-answer-the-question)
    * [State-to-State Migration](#state-to-state-migration)
    * [Housing Analysis](#housing-analysis)
* [Deliverable](#deliverable)
* [Next steps / Improvements](#next-steps--improvements)

## Problem Statement

This report/dashboard serves as a guide for a foreign investor looking to invest into the US rental market, particularly multiple-unit properties (duplex, triplex, etc.).

**Potential Extra Features**
* Homebuyer: recommend states/cities to live based on personal preferences
* House price prediction

## Context

### Investor's Requirements

* Fund: $500,000 cash
* Ideal states: no particular preference
* Property types: duplex, triplex, quadplex, condo, townhouse
* Investment strategies: **long-term**, mid-term, **house hacking**
* Define the best state(s): cashflow (cash on cash return) and property quality
* Expected insights: recommended areas with reasons, within each recommended state

### Business Question

1. What are the best states/areas to invest in the US rental market?
2. Once identified a state, which metro areas / neighborhoods are best to invest?

### Frame the Business Problem into a Data Question

* What are the states/areas that currently deliver the best cashflow and property quality?
	+ **Cashflow is gauged by supply & demand (employment, resources, location)**
	+ **Property quality is measured by property value over time**
* What are the most likely states/areas to deliver the best cashflow and property quality over the next 5 years? (analytical and predictive)
	+ **Migration trends:** rate at which people are moving in, factors for movers
	+ **Housing:** employment, growing or stable job market?, resources, property value over time, supply: # rental properties available, demand: # people looking to rent

### Components to Answer the Question

These are the factors that determine the "best" state for rental property investing

#### State-to-State Migration

* State GDP growth
* Employment rates
* Can we predict the next up and coming inbound and outbound states?
* Where are people leaving from and going to?
* What are the factors driving people away from, or towards, a certain location?
* What are the effects of state to state migration and how does it affect the country as a whole?

#### Housing Analysis

* Housing analysis
	+ Analyze factors influencing housing market trends
	+ High or low homeownership rates
	+ Cashflow vs property quality
	+ How to find quality tenants?


## Deliverable

The report pages include State-to-State Migration and Housing Analysis.

Here is the Minimum Viable Product (MVP) for the PBI report:

**State-to-State Migration**, where the investor can have an overview look at how and why people move from/to different states:

![migration](https://raw.githubusercontent.com/ntran0429/REP/main/images/migration-trends-page.PNG)

**Housing Analysis**, where the investor can drill down into each state and its respective metro areas with important metrics that help her determine which area to invest into:

![housing](https://raw.githubusercontent.com/ntran0429/REP/main/images/housing-page.PNG)


## Next steps / Improvements

* Currently, the Azure map is used for State-to-State Migration page, which is not supported for Publish to Web. Need to convert it to Bing map to make the report usable when embedded
* Dynamically change the [selected state] for State-to-State Migration page
* Format the report to be presentation ready
* Include appreciation metric (to create DAX measure for listing price YoY; data sourced from Realtor)
* Include household income from Census to calculate household income to rent ratio
* Include metro population over time to calculate population growth
* Include data at the county level for Housing Analysis page
